import os
import shutil
import sys

current_directory = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.dirname(current_directory)
source_dir = os.path.join(utils_dir,"1.prepareCameraInfo\model")


def delete_non_images_folders(target_dir):
    curItems = os.listdir(target_dir)
    for item in curItems:
        item_path = os.path.join(target_dir, item)

        if os.path.isdir(item_path) and item.lower() != "images":
            shutil.rmtree(item_path)

        elif os.path.isfile(item_path) and item.__contains__("database"):
            os.remove(item_path)


def copy_folder(target_dir):
    if not os.path.exists(target_dir):
        print("Target dir is not existed.")
        return

    delete_non_images_folders(target_dir)

    # 创建sparse文件夹
    sparseFolder = os.path.join(target_dir, "sparse")
    os.mkdir(sparseFolder)

    # 创建sparse/model文件夹
    target_folder = os.path.join(sparseFolder, "model")
    try:
        shutil.copytree(source_dir, target_folder)
        print(f"Copy: {source_dir} -> {target_folder}")
    except Exception as e:
        print(f"Error: {e}")

    # 创建sparse/0文件夹
    triangulateFolder = os.path.join(sparseFolder, "0")
    os.mkdir(triangulateFolder)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python prepareData.py <target dir>")
    else:
        target_dir = sys.argv[1]
        copy_folder(target_dir)
