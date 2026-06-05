import argostranslate.package
import argostranslate.translate

argostranslate.package.update_package_index()

available_packages = argostranslate.package.get_available_packages()

package = next(
    p for p in available_packages
    if p.from_code == "en" and p.to_code == "zh"
)

download_path = package.download()

argostranslate.package.install_from_path(
    download_path
)

package = next(
    p for p in available_packages
    if p.from_code == "zh" and p.to_code == "en"
)

download_path = package.download()

argostranslate.package.install_from_path(
    download_path
)

print("语言包安装完成")