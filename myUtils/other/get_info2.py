import os

# 输出指定路径的文件大小


def format_size(size_bytes):
    # 将字节转换为更易读的单位
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"  # 如果超过 TB，显示 PB


def main():
    # gs的结果
    dir = r"D:\code\GS\gaussian-splatting\output\350-1600-w_b"
    print("dir: ", dir)
    for folder_name in [str(i) for i in range(1, 10)] + ["mergeRes"]:
        filepath = os.path.join(dir, folder_name, r"point_cloud\iteration_30000\point_cloud.ply")
        file_size = os.path.getsize(filepath)
        readable_size = format_size(file_size)
        print(f"{folder_name}: {readable_size}")

    # 压缩后的结果
    dir = r"D:\code\GS\c3dgs\output"
    print("dir: ", dir)
    
    for folder_name in [str(i) for i in range(1, 10)] + ["mergeRes"]:
        filepath = os.path.join(dir, folder_name, r"point_cloud\iteration_35000\point_cloud.npz")
        file_size = os.path.getsize(filepath)
        readable_size = format_size(file_size)
        print(f"{folder_name}: {readable_size}")


if __name__ == "__main__":
    main()
