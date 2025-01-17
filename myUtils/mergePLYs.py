import argparse
import re
import os


def read_ply(file_path):
    with open(file_path, "rb") as f:
        header = b""
        while True:
            line = f.readline()
            header += line
            if line.startswith(b"end_header"):
                break

        vertex_count_line = header.split(b"\n")[2]
        vertex_count = int(vertex_count_line.split(b" ")[-1])

        properties = []
        for line in header.split(b"\n"):
            if line.startswith(b"property"):
                properties.append(line)
            elif line.startswith(b"end_header"):
                break

        vertices = []
        num_floats_per_vertex = sum(1 for prop in properties if b"float" in prop)

        for i in range(vertex_count):
            vertex_data = f.read(num_floats_per_vertex * 4)
            if not vertex_data:
                break
            vertices.append(vertex_data)

    return header, vertices


def write_ply(file_path, header, vertices):
    with open(file_path, "wb") as f:
        f.write(header)
        for i, vertex in enumerate(vertices):
            f.write(vertex)
            # print(f"Wrote vertex {i}: {struct.unpack('<' + 'f' * (len(vertex) // 4), vertex)}")


def merge_plys(src_files, target_file):
    header, vertices = read_ply(src_files[0])
    merged_vertices = vertices

    for i in range(1, len(src_files)):
        cur_header, cur_vertices = read_ply(src_files[i])

        # 检查属性一致性
        if cur_header.split(b"\n")[3:] != header.split(b"\n")[3:]:
            raise ValueError("The PLY files have different vertex properties.")

        merged_vertices += cur_vertices

    # 更新顶点数量
    header_lines = header.split(b"\n")
    header_lines[2] = f"element vertex {len(merged_vertices)}".encode()
    new_header = b"\n".join(header_lines)

    # 写入新的 PLY 文件
    write_ply(target_file, new_header, merged_vertices)


def process_files(dir, src_file_ids):
    src_files = []
    target_file_ids = ""
    for id in src_file_ids:
        file_path = os.path.join(dir, "point_cloud" + id + ".ply")
        if not os.path.exists(file_path):
            raise FileExistsError("The path is not existed.")
        src_files.append(file_path)
        target_file_ids += id

    target_file = os.path.join(dir, "point_cloud" + target_file_ids + ".ply")
    merge_plys(src_files, target_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="合并指定的文件")
    parser.add_argument("dir", help="文件所在目录")
    parser.add_argument("ids", nargs="+", help="多个 ID，用空格分隔")
    args = parser.parse_args()

    process_files(args.dir, args.ids)
