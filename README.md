# Stable Diffusion WebUI 水印扩展

一个简单的水印工具，让您可以直接在 Stable Diffusion WebUI 中为图片添加自定义水印。

## 功能特点

- 水印效果实时预览
- 支持多种混合模式（正常、正片叠底、滤色、叠加、柔光）
- 可调节水印透明度
- 自定义水印位置
- 水印缩放控制
- 保留原始图片元数据（可选）
- 保持水印宽高比
- 原图和预览图并排显示
- 一键下载带水印的图片

## 安装方法
1. 使用git clone 至Stable Diffusion WebUI 的扩展目录中:
```https://github.com/FHfanshu/sd-webui-watermark-editor.git```

## 使用方法

1. 在 Stable Diffusion WebUI 中打开 "Watermark" 标签页
2. 使用 "Original Image" 面板上传您的图片
3. 从下拉菜单中选择水印
4. 调整设置：
   - 混合模式：选择水印与图片的混合方式
   - 透明度：控制水印透明度（0-1）
   - 位置 X/Y：设置水印位置（0-1）
   - 缩放：调整水印大小（0.1-1.0）
   - 保留元数据：选择是否保留原始图片元数据
5. 实时查看预览效果
6. 点击 "Apply Watermark" 确认更改
7. 点击 "Save Image" 下载带水印的图片

## 支持的格式

- 输入图片：所有 PIL 支持的格式
- 水印图片：PNG 格式（支持透明）
- 输出格式：PNG

## 环境要求

- Stable Diffusion WebUI
- Python 3.x
- PIL (Pillow)
- numpy
- gradio

## 目录结构

```
extensions/
└── watermark/
    ├── scripts/
    │   └── watermark.py
    ├── watermarks/
    │   └── default.png
    └── README.md
```

## 参数说明

- **混合模式**:
  - normal: 标准叠加
  - multiply: 正片叠底（加深）
  - screen: 滤色（变亮）
  - overlay: 叠加（高对比度）
  - soft_light: 柔光（温和对比度）

- **位置控制**:
  - X: 0（左）到 1（右）
  - Y: 0（上）到 1（下）

- **缩放**:
  - 0.1: 最小尺寸
  - 1.0: 相对于图片的最大尺寸

## 注意事项

- 水印图片必须是带透明通道的 PNG 格式
- 默认显示高度设置为 768 像素
- 保持原始宽高比
- 水印会根据输入图片的较短边自动缩放

## 故障排除

- 如果水印不显示，请检查：
  1. 水印文件是否为 PNG 格式
  2. watermarks 文件夹是否存在且包含图片
  3. 文件权限是否正确
- 如果预览不更新，尝试点击 "Apply Watermark"


## 使用许可

[MIT]


## 版本历史

- 1.0.0: 首次发布
  - 基础水印功能
  - 多种混合模式
  - 实时预览
  - 元数据保留

欢迎贡献代码或报告问题！

## 更新日志

### 2024-12-21
- 修复了水印比例变形问题
- 优化了预览窗口显示
- 改进了图片保存功能

# English


# Image Watermark Extension for Stable Diffusion WebUI

A simple yet powerful watermark tool that allows you to add customized watermarks to your images directly in the Stable Diffusion WebUI.

## Features

- Real-time preview of watermark effects
- Multiple blend modes support (normal, multiply, screen, overlay, soft_light)
- Adjustable watermark opacity
- Customizable watermark position
- Watermark scale control
- Maintains original image metadata (optional)
- Preserves watermark aspect ratio
- Side-by-side display of original and preview images
- One-click download of watermarked images

## Installation

1. clone this repository into ./sd-webui/extensions/ via git
```https://github.com/FHfanshu/sd-webui-watermark-editor.git```

## Usage

1. Open the "Watermark" tab in Stable Diffusion WebUI
2. Upload your image using the "Original Image" panel
3. Select your watermark from the dropdown menu
4. Adjust the settings:
   - Blend Mode: Choose how the watermark blends with the image
   - Opacity: Control watermark transparency (0-1)
   - Position X/Y: Set watermark position (0-1)
   - Scale: Adjust watermark size (0.1-1.0)
   - Keep Metadata: Toggle original image metadata preservation
5. Preview updates in real-time
6. Click "Apply Watermark" to confirm changes
7. Click "Save Image" to download the watermarked image

## Supported Formats

- Input Images: Any format supported by PIL
- Watermark Images: PNG format (with transparency)
- Output Format: PNG

## Requirements

- Stable Diffusion WebUI
- Python 3.x
- PIL (Pillow)
- numpy
- gradio

## Directory Structure

```
extensions/
└── watermark/
    ├── scripts/
    │   └── watermark.py
    ├── watermarks/
    │   └── default.png
    └── README.md
```

## Settings

- **Blend Modes**:
  - normal: Standard overlay
  - multiply: Darkens image
  - screen: Lightens image
  - overlay: High contrast blend
  - soft_light: Gentle contrast blend

- **Position Controls**:
  - X: 0 (left) to 1 (right)
  - Y: 0 (top) to 1 (bottom)

- **Scale**:
  - 0.1: Smallest size
  - 1.0: Full size relative to image

## Notes

- Watermark images should be PNG format with transparency
- Default display height is set to 768 pixels
- Original aspect ratios are preserved
- Watermarks are automatically scaled based on the shorter side of the input image

## Troubleshooting

- If watermarks don't appear, check if:
  1. Watermark files are in PNG format
  2. Watermarks folder exists and contains images
  3. File permissions are correct
- If preview doesn't update, try clicking "Apply Watermark"
- If download fails, check browser download permissions

## License

[MIT]

## Credits

Created by [FHfanshu]

## Version History

- 1.0.0: Initial release
  - Basic watermark functionality
  - Multiple blend modes
  - Real-time preview
  - Metadata preservation

Feel free to contribute or report issues!