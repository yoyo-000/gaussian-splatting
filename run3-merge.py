import subprocess
import os
import shutil
import argparse

parser = argparse.ArgumentParser(description="Merge ply files and render merged res.")
parser.add_argument("root_dir", type=str, help="Path to the root directory.")
args = parser.parse_args()
root_dir = args.root_dir


def run_commands(command_list):
    for command in command_list:
        try:
            print(f"Running command: {command}")
            # 使用 subprocess.run 运行命令
            subprocess.run(command, shell=True, check=True)
            print(f"Command completed successfully: {command}")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running command: {command}")
            print(f"Error message: {e}")
            break  # 如果某个命令失败，停止执行后续命令


def myCopy(p1, p2):
    if os.path.exists(p1):
        shutil.copy(p1, p2)
        print(f"Copied {p1} to {p2}")
    else:
        print(f"Source file not found: {p1}")


# 1. 收集文件
merge_dir = os.path.join(root_dir, "merge")
os.makedirs(merge_dir, exist_ok=True)

for i in range(1, 10):
    source_file = os.path.join(root_dir, str(i), "point_cloud", "iteration_30000", "point_cloud.ply")
    target_file = os.path.join(merge_dir, f"point_cloud{i}.ply")

    if os.path.exists(source_file):
        shutil.copy(source_file, target_file)
        print(f"Copied {source_file} to {target_file}")
    else:
        print(f"Source file not found: {source_file}")
print("All files processed.")

# 2. 合并点云文件
commands = [fr'python D:\code\GS\gaussian-splatting\myUtils\mergePLYs.py {merge_dir} 1 2 3 4 5 6 7 8 9']
run_commands(commands)

# 3. 构建mergeRes文件夹
mergePLY_dir = os.path.join(root_dir, "mergeRes", "point_cloud", "iteration_30000")
os.makedirs(mergePLY_dir, exist_ok=True)

source_file = os.path.join(merge_dir, "point_cloud123456789.ply")
target_file = os.path.join(mergePLY_dir, "point_cloud.ply")
myCopy(source_file, target_file)

source_file = os.path.join(root_dir, "9", "cameras.json")
target_file = os.path.join(root_dir, "mergeRes", "cameras.json")
myCopy(source_file, target_file)

source_file = os.path.join(root_dir, "9", "cfg_args")
target_file = os.path.join(root_dir, "mergeRes", "cfg_args")
myCopy(source_file, target_file)

# 4. 计算指标
commands = [
    fr'python renderMergeRes.py --skip_test -r 1 --calculate_image_w -m {root_dir}/mergeRes',
    fr'python metrics.py -w -m {root_dir}/mergeRes',
]
run_commands(commands)
