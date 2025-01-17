import subprocess

# 定义要运行的 Python 脚本及其参数（字符串形式）
commands = [
    r'python render.py --skip_test -r 1 -i images --calculate_image_w -m D:\code\GS\gaussian-splatting\output\350-1600-baseline-GSwhite\1',
    r'python metrics.py -w -m D:\code\GS\gaussian-splatting\output\350-1600-baseline-GSwhite\1',
    r'python render.py --skip_test -r 1 -i images --calculate_image_w -m D:\code\GS\gaussian-splatting\output\350-1600-baseline-GSwhite\2',
    r'python metrics.py -w -m D:\code\GS\gaussian-splatting\output\350-1600-baseline-GSwhite\2',
    r'python render.py --skip_test -r 1 -i images --calculate_image_w -m D:\code\GS\gaussian-splatting\output\350-1600-baseline-GSwhite\3',
    r'python metrics.py -w -m D:\code\GS\gaussian-splatting\output\350-1600-baseline-GSwhite\3',
    r'python render.py --skip_test -r 1 -i images --calculate_image_w -m D:\code\GS\gaussian-splatting\output\350-1600-baseline-GSwhite\4',
    r'python metrics.py -w -m D:\code\GS\gaussian-splatting\output\350-1600-baseline-GSwhite\4',
    r'python render.py --skip_test -r 1 -i images --calculate_image_w -m D:\code\GS\gaussian-splatting\output\350-1600-baseline-GSwhite\5',
    r'python metrics.py -w -m D:\code\GS\gaussian-splatting\output\350-1600-baseline-GSwhite\5',
    r'python render.py --skip_test -r 1 -i images --calculate_image_w -m D:\code\GS\gaussian-splatting\output\350-1600-baseline-GSwhite\6',
    r'python metrics.py -w -m D:\code\GS\gaussian-splatting\output\350-1600-baseline-GSwhite\6',
    r'python render.py --skip_test -r 1 -i images --calculate_image_w -m D:\code\GS\gaussian-splatting\output\350-1600-baseline-GSwhite\7',
    r'python metrics.py -w -m D:\code\GS\gaussian-splatting\output\350-1600-baseline-GSwhite\7',
    r'python render.py --skip_test -r 1 -i images --calculate_image_w -m D:\code\GS\gaussian-splatting\output\350-1600-baseline-GSwhite\8',
    r'python metrics.py -w -m D:\code\GS\gaussian-splatting\output\350-1600-baseline-GSwhite\8',
    r'python render.py --skip_test -r 1 -i images --calculate_image_w -m D:\code\GS\gaussian-splatting\output\350-1600-baseline-GSwhite\9',
    r'python metrics.py -w -m D:\code\GS\gaussian-splatting\output\350-1600-baseline-GSwhite\9',
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