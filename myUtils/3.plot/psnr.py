import matplotlib.pyplot as plt

# 打开并读取txt文件
file_path = 'D:\code\gaussian-splatting\output\8\log_evaluating.txt'  # 请确保文件路径正确

epochs = []
l1_values = []
psnr_values = []

# 读取文件内容
with open(file_path, 'r') as file:
    # 跳过表头
    next(file)

    # 逐行读取数据并解析
    for line in file:
        epoch, l1, psnr = line.strip().split(', ')
        epochs.append(int(epoch))
        l1_values.append(float(l1))
        psnr_values.append(float(psnr))

# 创建两个子图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# 绘制L1损失图
ax1.plot(epochs, l1_values, marker='o', color='r')
ax1.set_xlabel('Epoch')
ax1.set_ylabel('L1 Loss')
ax1.set_title('Epoch vs L1 Loss')
ax1.grid(True)

# 绘制PSNR图
ax2.plot(epochs, psnr_values, marker='o', color='b')
ax2.set_xlabel('Epoch')
ax2.set_ylabel('PSNR (dB)')
ax2.set_title('Epoch vs PSNR')
ax2.grid(True)

# 显示图形
plt.tight_layout()
plt.show()