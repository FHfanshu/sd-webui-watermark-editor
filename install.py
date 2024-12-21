import launch

packages = {
    "piexif": "piexif>=1.1.3",
    "packaging": "packaging>=21.3"
}

for package, version in packages.items():
    if not launch.is_installed(package):
        launch.run_pip(f"install {version}", f"{package} for watermark plugin")
