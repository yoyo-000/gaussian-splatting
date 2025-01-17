import cv2
import os
import numpy as np

gt_mask_dir = r"D:\code\GS\gaussian-splatting\data\350_1920-1080\3\masks-1"
black_bg_training_dir = r"D:\code\GS\gaussian-splatting\output\350_1920-1080\3-1280-maskV1-phase-1\train\ours_30000\renders"
redidual_dir = r"D:\code\GS\gaussian-splatting\data\350_1920-1080\3\masks"

gt_masks = os.listdir(gt_mask_dir)
training_res = os.listdir(black_bg_training_dir)

for item in gt_masks:
    image_name = item.split('.')[0]
    image_id = int(image_name[-3:]) - 1
    training_res_name = str(image_id).zfill(5) + ".png"

    gt_mask_path = os.path.join(gt_mask_dir, item)
    training_res_path = os.path.join(black_bg_training_dir, training_res_name)

    A = cv2.imread(gt_mask_path)
    B = cv2.imread(training_res_path)

    # 转换为灰度图
    A_gray = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)
    B_gray = cv2.cvtColor(B, cv2.COLOR_BGR2GRAY)

    mask = (A_gray == 0) & (B_gray <= 245)
    new_image = np.full(A_gray.shape, 255, dtype=np.uint8)
    new_image[mask] = 0

    res_path = os.path.join(redidual_dir, "images" + str(image_id + 1).zfill(4) + ".png")
    cv2.imwrite(res_path, new_image)
