import math
import numpy as np
from scipy.spatial.transform import Rotation as RT


def quaternion_to_rotation_matrix(quaternion):
    """将四元数转换为旋转矩阵"""
    w, x, y, z = quaternion
    R = np.array(
        [
            [1 - 2 * (y**2 + z**2), 2 * (x * y - w * z), 2 * (x * z + w * y)],
            [2 * (x * y + w * z), 1 - 2 * (x**2 + z**2), 2 * (y * z - w * x)],
            [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x**2 + y**2)],
        ]
    )
    return R


def rotmat2qvec(R):
    Rxx, Ryx, Rzx, Rxy, Ryy, Rzy, Rxz, Ryz, Rzz = R.flat
    K = (
        np.array(
            [
                [Rxx - Ryy - Rzz, 0, 0, 0],
                [Ryx + Rxy, Ryy - Rxx - Rzz, 0, 0],
                [Rzx + Rxz, Rzy + Ryz, Rzz - Rxx - Ryy, 0],
                [Ryz - Rzy, Rzx - Rxz, Rxy - Ryx, Rxx + Ryy + Rzz],
            ]
        )
        / 3.0
    )
    eigvals, eigvecs = np.linalg.eigh(K)
    qvec = eigvecs[[3, 0, 1, 2], np.argmax(eigvals)]
    if qvec[0] < 0:
        qvec *= -1
    return qvec


def transform_to_world_coordinates(R, T):
    R_T = R.T  # 旋转矩阵的转置
    t_prime = -np.dot(R_T, T)  # 新的平移向量
    return R_T, t_prime

# 适应COLMAP坐标系的转换 (调整旋转矩阵)
def adjust_for_colmap_coordinate_system(R):
    R_colmap = R.copy()
    R_colmap[:3, 1:3] *= -1  # 反转Y-Z轴以适应COLMAP坐标系
    return R_colmap

def calculate_rotation_matrix(curPosition):
    target = np.array([0.0, 0.0, 0.0])
    worldUp = np.array([0.0, 0.0, 1.0])

    lookDir = target - curPosition
    lookDir = lookDir / np.linalg.norm(lookDir)

    # 计算右向量
    right = np.cross(lookDir, worldUp)
    right = right / np.linalg.norm(right)
    newUp = np.cross(right, lookDir)
    newUp = newUp / np.linalg.norm(newUp)

    # 构造旋转矩阵
    R = np.array([[right[0], right[1], right[2]], [newUp[0], newUp[1], newUp[2]], [-lookDir[0], -lookDir[1], -lookDir[2]]])

    qw, qx, qy, qz = rotmat2qvec(R)
    qw = -qw
    print("Blender: ",qw,qx,qy,qz)

    R = adjust_for_colmap_coordinate_system(R)

    qw, qx, qy, qz = rotmat2qvec(R)
    print("New: ",qw,qx,qy,qz)

    # 取反后blender里面看起来正确
    # 再次调整 和sxl的一致

    # return -qx, qw, qz, -qy
    return qw, -qx, qy, qz


index = 1
data_lines = []

# 摄像机参数
cameraDist = 200
photoDistribution = {-80: 10, -60: 30, -30: 60, 0: 150, 30: 60, 60: 30, 80: 10}

# 打印相机参数和四元数
for pitchAngle, numPhotos in photoDistribution.items():
    for i in range(1, numPhotos + 1):
        # 计算相机位置
        curRadians = 2 * math.pi / numPhotos * i
        x = cameraDist * math.cos(curRadians) * math.cos(math.radians(pitchAngle))
        y = cameraDist * math.sin(curRadians) * math.cos(math.radians(pitchAngle))
        z = cameraDist * math.sin(math.radians(pitchAngle))
        curPosition = np.array([x, y, z])

        quaternion = calculate_rotation_matrix(curPosition)

        print(f"Index: {index}, Position: {curPosition}, Quaternion: {quaternion}")

        R = quaternion_to_rotation_matrix(quaternion)
        T = np.array([x, y, z])
        R_T, t_prime = transform_to_world_coordinates(R, T)
        quaternion_prime = RT.from_matrix(R_T).as_quat(scalar_first=True)

        fileName = f"images{index:04d}.ToneMapper.dst.1.RGBA.png"

        # 输出结果
        data_line = f"{index} {quaternion_prime[0]} {quaternion_prime[1]} {quaternion_prime[2]} {quaternion_prime[3]} {t_prime[0]} {t_prime[1]} {t_prime[2]} 1 {fileName}"
        data_lines.append(data_line)
        data_lines.append("")  # 空行

        index += 1

tagetImagesPath = r"D:\code\GS\gaussian-splatting\data\5-test\sparse\0\images.txt"
with open(tagetImagesPath, "w") as f:
    f.write("# Image list with two lines of data per image:\n")
    f.write("# IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME\n")
    f.write("# POINTS2D[] as (X, Y, POINT3D_ID)\n")

    for line in data_lines:
        f.write(line + "\n")
