import os


# 读取PLY文件并返回顶点数据
def read_ply(file_path):
    vertices = []

    with open(file_path, 'r') as f:
        lines = f.readlines()

        # 跳过头部直到"end_header"
        header_end = lines.index('end_header\n')

        # 读取顶点数据
        for line in lines[header_end + 1 :]:
            # 如果该行是空行或不包含有效的顶点数据，跳过
            if not line.strip():
                continue
            # 读取顶点数据：x, y, z
            x, y, z = map(float, line.split())
            vertices.append((x, y, z))

    return vertices


# 将数据写入新的文件
def write_output_file(vertices, output_path):
    # 固定的颜色值
    R, G, B = 99, 117, 90
    ERROR = 0

    # 打开输出文件
    with open(output_path, 'w') as f:
        # 写入头部信息
        f.write("# POINT3D_ID, X, Y, Z, R, G, B, ERROR\n")
        f.write(f"# Number of points: {len(vertices)}\n")

        # 写入顶点数据
        for i, (x, y, z) in enumerate(vertices, start=1):
            f.write(f"{i} {x} {y} {z} {R} {G} {B} {ERROR}\n")


# 等间隔采样函数
def uniform_downsample(vertices, target_count):
    """
    对点云进行等间隔降采样。
    :param vertices: 原始点云数据，格式为 [(x1, y1, z1), (x2, y2, z2), ...]
    :param target_count: 目标点数
    :return: 降采样后的点云数据
    """
    total_points = len(vertices)
    if target_count >= total_points:
        return vertices

    # 计算采样间隔
    step = max(1, total_points // target_count)

    # 等间隔采样
    downsampled_vertices = vertices[::step]

    # 如果采样后的点数仍然多于目标点数，截断到目标点数
    if len(downsampled_vertices) > target_count:
        downsampled_vertices = downsampled_vertices[:target_count]

    return downsampled_vertices


# 主函数
def main():
    file_dir = r"D:\code\GS\gaussian-splatting\data\original_data_update"
    for file in os.listdir(file_dir):
        # 读取PLY文件
        vertices = read_ply(os.path.join(file_dir, file))
        print(f"{os.path.basename(file)}: {len(vertices)}")

    # file_path = r"D:\code\GS\gaussian-splatting\data\original_data_update\fiber_9.ply"
    # output_path = r"D:\code\GS\gaussian-splatting\data\test-original_data\9\sparse\0\points3D.txt"
    # target_count = 80000  # 目标点数
    # vertices = read_ply(file_path)
    # # 等间隔降采样
    # downsampled_vertices = uniform_downsample(vertices, target_count)

    # # 写入输出文件
    # write_output_file(downsampled_vertices, output_path)


if __name__ == '__main__':
    main()
