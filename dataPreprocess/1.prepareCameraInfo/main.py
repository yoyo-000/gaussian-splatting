import re
import os
from colmap_loader import (
    read_extrinsics_binary,
    read_intrinsics_binary,
)
import shutil

base_dir = r"D:\code\GS\gaussian-splatting\data\350_1920-1080\9"

current_directory = os.path.dirname(os.path.abspath(__file__))
utils_dir = os.path.dirname(current_directory)

# 自动重建并验证过的数据
cameras_extrinsic_file = base_dir + r"\sparse\0\images.bin"
cameras_intrinsic_file = base_dir + r"\sparse\0\cameras.bin"
imageNamePath = base_dir + r"\images"

# 暂存的RT信息
rotateVecPath = utils_dir + r"\1.prepareCameraInfo\rotateVec.txt"
translationVecPath = utils_dir + r"\1.prepareCameraInfo\translationVec.txt"
# 目标文件路径
tagetCamerasPath = utils_dir + r"\1.prepareCameraInfo\model\cameras.txt"
tagetImagesPath = utils_dir + r"\1.prepareCameraInfo\model\images.txt"

# 将要固定的相机外参复制过来
dst_path = os.path.join(utils_dir, r"1.prepareCameraInfo\images.bin")
shutil.copy(cameras_extrinsic_file, dst_path)


# 读取相机内外参，暂存RT信息
def readColmapCameras(cam_extrinsics, cam_intrinsics):
    intr = cam_intrinsics[1]
    print("The focal length is ", intr.params[0])
    print("The width and height is ", intr.width, intr.height)

    rotateVec = {}
    translationVec = {}
    for idx, key in enumerate(cam_extrinsics):
        extr = cam_extrinsics[key]
        match = re.search(r"images(\d{4})", extr.name)
        number = int(match.group(1))
        rotateVec[number] = extr.qvec.tolist()
        translationVec[number] = extr.tvec.tolist()

    rotateVec = {key: rotateVec[key] for key in sorted(rotateVec.keys())}
    translationVec = {key: translationVec[key] for key in sorted(translationVec.keys())}

    with open(rotateVecPath, "w") as file:
        for key, value in rotateVec.items():
            file.write(f"{key}:{value}\n")

    with open(translationVecPath, "w") as file:
        for key, value in translationVec.items():
            file.write(f"{key}:{value}\n")

    return intr.params[0], rotateVec, translationVec


# 写相机外参
def writeCamerasInfo(focalLength, width, height):
    with open(tagetCamerasPath, "w") as f:
        f.write("# Camera list with one line of data per camera:\n")
        f.write("# CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[fx,fy,cx,cy]\n")
        f.write("# Number of cameras: 1\n")

        data_line = f"1 SIMPLE_PINHOLE {width} {height} {focalLength:.6f} {width/2} {height/2}"
        f.write(data_line)


def readImagesName():
    # 读取ID和对应的图像名
    parsedImagesName = {}
    filenames = os.listdir(imageNamePath)
    for filename in filenames:
        match = re.search(r"images(\d{4})", filename)
        key = int(match.group(1))
        parsedImagesName[key] = filename
    return parsedImagesName


# 写相机内参
def writeImagesInfo(qVec, tVec, imagesName):
    data_lines = []
    for i in range(1, len(qVec) + 1):
        data_line = f"{i} {qVec[i][0]:.6f} {qVec[i][1]:.6f} {qVec[i][2]:.6f} {qVec[i][3]:.6f} {tVec[i][0]:.6f} {tVec[i][1]:.6f} {tVec[i][2]:.6f} 1 {imagesName[i]}"
        data_lines.append(data_line)
        data_lines.append("")  # 空行

    with open(tagetImagesPath, "w") as f:
        f.write("# Image list with two lines of data per image:\n")
        f.write("# IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME\n")
        f.write("# POINTS2D[] as (X, Y, POINT3D_ID)\n")

        for line in data_lines:
            f.write(line + "\n")


cam_extrinsics = read_extrinsics_binary(cameras_extrinsic_file)
cam_intrinsics = read_intrinsics_binary(cameras_intrinsic_file)
focalLength, rotateVec, translationVec = readColmapCameras(cam_extrinsics, cam_intrinsics)
imagesName = readImagesName()

# 写入内外参数信息
writeCamerasInfo(focalLength, cam_intrinsics[1].width, cam_intrinsics[1].height)
writeImagesInfo(rotateVec, translationVec, imagesName)
