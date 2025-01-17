import cv2
import numpy as np

# 加载图像
image = cv2.imread(r'D:\code\GS\Robust3DGaussians\output\3-test\train\ours_30000\renders\00107.png')
mask = cv2.imread(r'D:\code\gaussian-splatting\myUtils\108.jpg', cv2.IMREAD_GRAYSCALE)

non_white_pixels = np.any(image != [255, 255, 255], axis=-1)
mask_outside = mask == 0
# 统计第一张图中是彩色且在 mask 外的像素
outside_and_colored = np.logical_and(non_white_pixels, mask_outside)
count = np.sum(outside_and_colored)
print("Robust3DGaussians: ")
print("在 mask 外的非白色像素点数: ", count)
p = count/(image.shape[0]*image.shape[1])
print(f"误差比例为（mask外的非白色像素数/总像素数）: {p:.2f}")
# ----------------------------------------------------------------------------------------------------------

# 加载图像
image = cv2.imread(r'D:\code\gaussian-splatting\output\3\train\ours_20000\renders\00107.png')
mask = cv2.imread(r'D:\code\gaussian-splatting\myUtils\108.jpg', cv2.IMREAD_GRAYSCALE)

non_white_pixels = np.any(image != [255, 255, 255], axis=-1)
mask_outside = mask == 0
# 统计第一张图中是彩色且在 mask 外的像素
outside_and_colored = np.logical_and(non_white_pixels, mask_outside)
count = np.sum(outside_and_colored)
print("原始GS: ")
print("在 mask 外的非白色像素点数:", count)
p = count/(image.shape[0]*image.shape[1])
print(f"误差比例为（mask外的非白色像素数/总像素数）: {p:.2f}")