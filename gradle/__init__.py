import os
import platform
import subprocess


def run_gradle_command(command):
    """
    :param command: 实际相关命令
    :return: 执行命令结果
    """
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True, encoding='utf-8')
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None


def open_file(file_path):
    """
    在电脑上打开截屏文件
    :param file_path: 电脑上的截屏文件地址
    """
    system = platform.system().lower()
    if system == "darwin":  # macOS
        subprocess.run(["open", file_path])
    elif system == "linux":  # Linux
        subprocess.run(["xdg-open", file_path])
    elif system == "windows":  # Windows
        subprocess.run(["start", file_path], shell=True)
    else:
        print("Unsupported operating system.")


def save_result_to_file(file_dir, file_name, task_name, task_result):
    """
    保存结果到文件
    :param file_dir: 文件目录
    :param file_name: 文件名称
    :param task_name: gradle task 名称
    :param task_result: 内容¬
    :return: 文件地址
    """
    # 从 > Task 行开始截取执行结果
    start_str = "> Task " + task_name
    content = task_result[task_result.rfind(start_str):]
    if len(file_name) > 0:
        des_file_name = file_name + '.txt'
    else:
        des_file_name = task_name[1:].strip().replace(':', '-') + ".txt"
    file_path = file_dir + os.path.sep + des_file_name
    # 如果目录不存在，先创建一个目录
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    with open(file_path, 'w') as f:
        f.write(content)
        f.flush()
        f.close()
    return file_path
