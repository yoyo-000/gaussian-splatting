import matplotlib.pyplot as plt

# 打开并读取txt文件
file_path = 'D:\code\gaussian-splatting\output\8\log_training.txt'  # 请确保文件路径正确

epochs = []
losses = []

with open(file_path, 'r') as file:
    # 跳过表头
    next(file)

    # 逐行读取数据并解析
    for line in file:
        epoch, loss = line.strip().split(', ')
        epochs.append(int(epoch))
        losses.append(float(loss))

# 绘图
plt.plot(epochs, losses, marker='o',markersize = 1)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Epoch vs Loss')
plt.grid(True)
plt.show()