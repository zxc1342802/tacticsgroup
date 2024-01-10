import os
import zipfile

source_directory = "/Users/leijm/fsdownload"  # 替换为包含ZIP文件的源目录路径
destination_directory = "/Users/leijm/fsdownload/directory"  # 替换为解压缩后文件的目标目录路径

# 遍历源目录下的文件
for filename in os.listdir(source_directory):
    if filename.startswith("opay-egypt-pos-web-2023-08-20") and filename.endswith(".zip"):
        file_path = os.path.join(source_directory, filename)

        # 创建目标文件夹路径
        target_folder = os.path.join(destination_directory, os.path.splitext(filename)[0])
        os.makedirs(target_folder, exist_ok=True)

        # 解压缩ZIP文件到目标文件夹
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(target_folder)

        print("解压缩完成:", filename)