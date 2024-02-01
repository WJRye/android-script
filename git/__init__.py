import platform
import subprocess


def run_git_command(command):
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


def sync_branch(branch):
    """
    同步分支到最新代码
    :param branch: 分支名称
    :return: 检查结果
    """
    result = run_git_command(
        ['git', 'fetch', 'origin', branch])
    if result is None:
        return None
    result = run_git_command(
        ['git', 'checkout', branch])
    if result is None:
        return None
    result = run_git_command(
        ['git', 'pull', 'origin', branch])
    return result


def check_branch(target_branch, current_branch):
    """
    检查分支
    :param target_branch: 要比对的分支
    :param current_branch: 当前分支
    :return: 检查分支结果，True表示成功，否则失败
    """
    if sync_branch(target_branch) is None:
        print(f"Sync branch: {target_branch} Failed")
        return False
    if sync_branch(current_branch) is None:
        print(f"Sync branch: {current_branch} Failed")
        return False
    return True


def get_git_user():
    """
    获取自己的 git user name
    :return: git 账户名称
    """
    user_name = run_git_command(['git', 'config', '--get', 'user.name']).strip()
    if user_name is None:
        print("获取 git user.name 失败，请配置：git config user.name")
    return user_name
