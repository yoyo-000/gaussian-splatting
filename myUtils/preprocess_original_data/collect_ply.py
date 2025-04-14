import os
import shutil


def update_ply_vertex_count(ply_file_path, new_vertex_count):
    with open(ply_file_path, 'r') as file:
        lines = file.readlines()

    # 找到 "element vertex" 这一行，并修改顶点数量
    for i, line in enumerate(lines):
        if line.startswith("element vertex"):
            # 获取当前顶点数量
            parts = line.split()
            parts[2] = str(new_vertex_count)  # 更新顶点数量
            lines[i] = " ".join(parts) + "\n"
            break

    # 重新写入文件
    with open(ply_file_path, 'w') as file:
        file.writelines(lines)


def correct_ply_vertex_count(file_dir):
    for file in os.listdir(file_dir):
        ply_path = os.path.join(file_dir, file)
        count = 0

        with open(ply_path, 'r') as f:
            lines = f.readlines()

            # 跳过头部直到"end_header"
            header_end = lines.index('end_header\n')

            # 读取顶点数据
            for line in lines[header_end + 1 :]:
                # 如果该行是空行或不包含有效的顶点数据，跳过
                if not line.strip():
                    continue
                count += 1

        update_ply_vertex_count(ply_path, count)
        print(f"{file}: {count}")


def update_and_copy_files(src_folder, dest_folder, ply_map):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for filename in os.listdir(src_folder):
        if filename.endswith(".ply"):
            # 提取文件名和扩展名
            name, ext = os.path.splitext(filename)

            # 根据 ply_map 映射修改文件名
            for old, new in ply_map.items():
                if f"_{old}" in name:
                    new_name = name.replace(f"_{old}", f"_{new}")
                    break

            # 构建新的文件路径
            new_filepath = os.path.join(dest_folder, new_name + ext)

            # 复制文件到目标文件夹
            src_filepath = os.path.join(src_folder, filename)
            shutil.copy(src_filepath, new_filepath)


# # 1. 修改数量
# file_dir = r"D:\code\GS\gaussian-splatting\data\original_data"
# correct_ply_vertex_count(file_dir)

# # 2. 修改命名为正确的对应关系
# ply_map = {'0': '1', '1': '7', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '8', '8': '9'}
# src_folder = file_dir
# dest_folder = r"D:\code\GS\gaussian-splatting\data\original_data_update"
# update_and_copy_files(src_folder, dest_folder, ply_map)
