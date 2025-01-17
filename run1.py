import subprocess

# 定义要运行的 Python 脚本及其参数（字符串形式）
commands = [
    r'python train.py -s D:\code\GS\gaussian-splatting\data\350_1920-1080\1 -i images-w -w',
    r'python train.py -s D:\code\GS\gaussian-splatting\data\350_1920-1080\2 -i images-w -w',
    r'python train.py -s D:\code\GS\gaussian-splatting\data\350_1920-1080\3 -i images-w -w',
    r'python train.py -s D:\code\GS\gaussian-splatting\data\350_1920-1080\4 -i images-w -w',
    r'python train.py -s D:\code\GS\gaussian-splatting\data\350_1920-1080\5 -i images-w -w',
    r'python train.py -s D:\code\GS\gaussian-splatting\data\350_1920-1080\6 -i images-w -w',
    r'python train.py -s D:\code\GS\gaussian-splatting\data\350_1920-1080\7 -i images-w -w',
    r'python train.py -s D:\code\GS\gaussian-splatting\data\350_1920-1080\8 -i images-w -w',
    r'python train.py -s D:\code\GS\gaussian-splatting\data\350_1920-1080\9 -i images-w -w',
]

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

if __name__ == "__main__":
    run_commands(commands)