import os
import subprocess
import sys


def _run_py(name):
    # 获取当前执行的 Python 脚本文件的路径
    script_path = os.path.abspath(__file__)
    # 获取该文件所在的目录路径
    script_directory = os.path.dirname(script_path)
    subprocess.run(["python3", f"{script_directory}{os.path.sep}{name}.py"])


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 0:
        _run_py(args[0])
