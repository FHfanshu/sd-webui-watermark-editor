import modules.scripts as scripts
import gradio as gr
import os
from modules import script_callbacks
from PIL import Image
import numpy as np
from packaging import version
import piexif
import io

class WatermarkTab:
    def __init__(self):
        self.watermark_dir = os.path.join(scripts.basedir(), "watermarks")
        if not os.path.exists(self.watermark_dir):
            os.makedirs(self.watermark_dir)

    def create_ui(self):
        with gr.Blocks(analytics_enabled=False) as ui_component:
            with gr.Tab("Watermark"):
                # 图片显示区域 - 原图和预览并排
                with gr.Row():
                    with gr.Column(scale=1):
                        input_image = gr.Image(
                            label="Original Image", 
                            type="pil",
                            tool="editor",
                            height=768
                        )
                    with gr.Column(scale=1):
                        preview_image = gr.Image(
                            label="Preview",
                            interactive=False,
                            type="pil",
                            height=768
                        )
                
                # 水印控制区域
                with gr.Row():
                    with gr.Column(scale=1):
                        watermark_file = gr.Dropdown(
                            label="Watermark Image",
                            choices=self.get_watermark_files(),
                            value="default.png"
                        )
                    with gr.Column(scale=1):
                        blend_mode = gr.Dropdown(
                            label="Blend Mode",
                            choices=["normal", "multiply", "screen", "overlay", "soft_light"],
                            value="normal"
                        )
                    
                # 透明度控制
                with gr.Row():
                    opacity = gr.Slider(
                        label="Opacity",
                        minimum=0,
                        maximum=1,
                        value=0.5,
                        step=0.1
                    )
                
                # 位置控制    
                with gr.Row():
                    with gr.Column(scale=1):
                        position_x = gr.Slider(
                            label="Position X",
                            minimum=0,
                            maximum=1,
                            value=0.5,
                            step=0.1
                        )
                    with gr.Column(scale=1):
                        position_y = gr.Slider(
                            label="Position Y",
                            minimum=0,
                            maximum=1,
                            value=0.5,
                            step=0.1
                        )
                
                # 其他设置
                with gr.Row():
                    with gr.Column(scale=1):
                        keep_metadata = gr.Checkbox(
                            label="Keep Original Metadata",
                            value=True,
                            info="Preserve EXIF, XMP, and other metadata from the original image"
                        )
                    with gr.Column(scale=1):
                        watermark_scale = gr.Slider(
                            label="Watermark Scale",
                            minimum=0.1,
                            maximum=1.0,
                            value=0.3,
                            step=0.1
                        )
                
                # 应用和保存按钮
                with gr.Row():
                    apply_button = gr.Button("Apply Watermark", variant="primary")
                    save_button = gr.Button("Save Image")
                    download_image = gr.File(label="Download", visible=False)

                # 事件处理
                # 实时预览
                input_controls = [
                    input_image,
                    watermark_file,
                    blend_mode,
                    opacity,
                    position_x,
                    position_y,
                    keep_metadata,
                    watermark_scale
                ]
                
                for control in input_controls[1:]:  # 除了input_image外的所有控件
                    control.change(
                        fn=self.apply_watermark,
                        inputs=input_controls,
                        outputs=preview_image
                    )
                
                # Apply按钮事件
                apply_button.click(
                    fn=self.apply_watermark,
                    inputs=input_controls,
                    outputs=preview_image
                )
                
                # 图片上传事件
                input_image.change(
                    fn=self.apply_watermark,
                    inputs=input_controls,
                    outputs=preview_image
                )
                
                # 保存按钮事件
                save_button.click(
                    fn=self.save_image,
                    inputs=[preview_image],
                    outputs=[download_image]
                )

        return ui_component

    def get_watermark_files(self):
        return [f for f in os.listdir(self.watermark_dir) if f.lower().endswith('.png')]

    def get_image_metadata(self, image):
        """获取图片的元数据"""
        metadata = {}
        try:
            if hasattr(image, 'info'):
                metadata = image.info
        except:
            pass
        return metadata

    def apply_blend_mode(self, base, top, mode, opacity):
        """实现不同的混合模式"""
        base = np.array(base).astype(float) / 255
        top = np.array(top).astype(float) / 255
        
        if mode == "normal":
            result = top
        elif mode == "multiply":
            result = base * top
        elif mode == "screen":
            result = 1 - (1 - base) * (1 - top)
        elif mode == "overlay":
            result = np.where(base <= 0.5,
                            2 * base * top,
                            1 - 2 * (1 - base) * (1 - top))
        elif mode == "soft_light":
            result = np.where(top <= 0.5,
                            base - (1 - 2 * top) * base * (1 - base),
                            base + (2 * top - 1) * (self.d(base) - base))
        else:
            result = top
            
        # 应用透明度
        result = base * (1 - opacity) + result * opacity
        return (result * 255).astype(np.uint8)

    def d(self, x):
        """辅助函数，用于soft_light混合模式"""
        return np.where(x <= 0.25,
                       ((16 * x - 12) * x + 4) * x,
                       np.sqrt(x))
    def apply_watermark(self, input_image, watermark_path, blend_mode, opacity, pos_x, pos_y, 
                       keep_metadata, watermark_scale):
        """应用水印到图片"""
        try:
            if input_image is None:
                return None
                
            # 打开水印图片
            watermark_full_path = os.path.join(self.watermark_dir, watermark_path)
            if not os.path.exists(watermark_full_path):
                return None
                
            watermark = Image.open(watermark_full_path)
            
            # 转换图片为RGBA模式
            if input_image.mode != 'RGBA':
                input_image = input_image.convert('RGBA')
            if watermark.mode != 'RGBA':
                watermark = watermark.convert('RGBA')
                
            # 获取原始元数据
            original_metadata = {}
            if keep_metadata:
                original_metadata = self.get_image_metadata(input_image)
                
            # 计算水印的新尺寸，保持宽高比
            # 使用较短的边作为参考来计算缩放
            input_shorter_side = min(input_image.width, input_image.height)
            watermark_aspect_ratio = watermark.width / watermark.height
            
            if watermark_aspect_ratio > 1:  # 水印是横向的
                new_width = int(input_shorter_side * watermark_scale)
                new_height = int(new_width / watermark_aspect_ratio)
            else:  # 水印是纵向的或正方形
                new_height = int(input_shorter_side * watermark_scale)
                new_width = int(new_height * watermark_aspect_ratio)
                
            # 调整水印大小
            watermark = watermark.resize((new_width, new_height), Image.LANCZOS)
            
            # 创建新图层
            result = Image.new('RGBA', input_image.size, (0, 0, 0, 0))
            
            # 计算水印位置
            x = int((input_image.width - watermark.width) * pos_x)
            y = int((input_image.height - watermark.height) * pos_y)
            
            # 创建水印图层
            watermark_layer = Image.new('RGBA', input_image.size, (0, 0, 0, 0))
            watermark_layer.paste(watermark, (x, y), watermark)
            
            # 应用混合模式
            r, g, b, a = input_image.split()
            wr, wg, wb, wa = watermark_layer.split()
            
            # 对RGB通道应用混合模式
            merged_r = Image.fromarray(self.apply_blend_mode(r, wr, blend_mode, opacity))
            merged_g = Image.fromarray(self.apply_blend_mode(g, wg, blend_mode, opacity))
            merged_b = Image.fromarray(self.apply_blend_mode(b, wb, blend_mode, opacity))
            
            # 合并通道
            result = Image.merge('RGBA', (merged_r, merged_g, merged_b, a))
            
            # 恢复元数据
            if keep_metadata:
                for key, value in original_metadata.items():
                    try:
                        result.info[key] = value
                    except:
                        pass
                        
            return result
            
        except Exception as e:
            print(f"Error applying watermark: {str(e)}")
            return None

    def save_image(self, image):
        """保存处理后的图片"""
        if image is None:
            return None
            
        try:
            # 创建一个字节流
            byte_stream = io.BytesIO()
            # 保存图片到字节流
            image.save(byte_stream, format='PNG')
            # 获取字节数据
            image_bytes = byte_stream.getvalue()
            
            # 返回文件数据，设置文件名和MIME类型
            return (image_bytes, "watermarked_image.png")
            
        except Exception as e:
            print(f"Error saving image: {str(e)}")
            return None

# 创建全局实例
watermark_tab = WatermarkTab()

def on_ui_tabs():
    return [(watermark_tab.create_ui(), "Watermark", "watermark_tab")]

script_callbacks.on_ui_tabs(on_ui_tabs)
