import os

# 输出某个路径下所有文件的大小

def format_size(size_bytes):
    # 将字节转换为更易读的单位
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"  # 如果超过 TB，显示 PB


def list_file_sizes(directory):
    if not os.path.isdir(directory):
        print("错误：指定的路径不是一个目录。")
        return

    print(f"目录 '{directory}' 下的文件大小：")
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            file_size = os.path.getsize(filepath)
            readable_size = format_size(file_size)
            print(f"{filename}: {readable_size}")


def main():
    directory = r"Z:\VTData\Users\siyan.han\CollectedData\Raw\HealthAdult\ZhangHuiXinHead_default"
    list_file_sizes(directory)


if __name__ == "__main__":
    main()
