import os
import subprocess
import sys

from __init__ import get_git_user, check_branch, open_file


def get_commit_file_path_set(target_branch, current_branch, author):
    """
    比对 branch，获取提交的文件相对路径列表
    :param target_branch: 要比对的分支
    :param current_branch: 当前分支
    :param author: git user.name
    :return: 提交的文件相对路径列表
    """
    try:
        if (target_branch == 'master' or target_branch.startswith('release')) and not current_branch.startswith(
                'release'):
            branch_command = f"{target_branch}..{current_branch}"
        else:
            branch_command = f"{current_branch}...{target_branch}"

        command = ['git', 'log', branch_command, '--author=' + author,
                   '--name-status', '--oneline']
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        file_path_list = set()
        rename_file_path_list = set()
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                process.kill()
                break
            if output:
                text = output.strip().replace("\t", "")
                if text.startswith('M') or text.startswith('A') or text.startswith('D'):
                    file_path = text[1:]
                    file_path_list.add(file_path)
                else:
                    # 记录重命名文件，需要移除
                    if output.strip().startswith('R'):
                        rename_file_path = output.strip().split('\t')[1]
                        rename_file_path_list.add(rename_file_path)
        if len(file_path_list) == 0:
            print(f"{' '.join(command)}: No commit files")
            return None
        for rename_file_path in rename_file_path_list:
            try:
                file_path_list.remove(rename_file_path)
            except KeyError:
                pass
        return file_path_list
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None


def get_commit_file_full_path_list(project_path, file_path_list):
    """
    获取提交的文件的全路径列表，并以,分割
    :param project_path: 项目路径
    :param file_path_list: 提交的文件的相对路径列表
    :return: kotlin_file_list 表示 kotlin 文件的全路径列表，以 , 分割；java_file_list 表示 java 文件的全路径列表，以 , 分割
    """
    kotlin_file_list = []
    java_file_list = []
    for index in range((len(file_path_list))):
        if file_path_list[index].endswith('.kt'):
            kotlin_file_list.append(project_path + os.path.sep + file_path_list[index])
        if file_path_list[index].endswith('.java'):
            java_file_list.append(project_path + os.path.sep + file_path_list[index])
    return ','.join(kotlin_file_list), ','.join(java_file_list)


def make_report(project_path, kotlin_file_list, java_file_list):
    result = []
    result.append(make_detekt_report(project_path, kotlin_file_list))
    result.append(make_pmd_report(project_path, "java", java_file_list))
    return result


def make_detekt_report(project_path, kotlin_file_list):
    """
    生成 detekt html 文件报告
    :param project_path: 项目路径
    :param kotlin_file_list: kotlin 文件路径列表
    :return: detekt 静态代码分析结果报告地址
    """
    if len(kotlin_file_list) == 0:
        return ""
    report_dir = f"{project_path}{os.path.sep}build{os.path.sep}reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    report_path = f"{report_dir}{os.path.sep}detekt.html"
    if os.path.exists(report_path):
        os.remove(report_path)
    detekt_cli_path = get_detekt_cli_path()
    detekt_cli_arg_config = f"-c {get_detekt_config_path()}"
    detekt_cli_arg_report = f"-r html:{report_path}"
    detekt_cli_arg_input = f"-i {kotlin_file_list}"

    args = f"{detekt_cli_path} {detekt_cli_arg_config} {detekt_cli_arg_report} {detekt_cli_arg_input}"
    try:
        subprocess.run(args, shell=True, stdout=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError:
        pass
    return report_path


def make_pmd_report(project_path, language, file_list):
    """
    生成 pmd html 文件报告
    :param project_path: 项目路径
    :param language: java 或 kotlin
    :param file_list: java 或 kotlin 文件路径列表
    :return: pmd 静态代码分析结果报告地址
    """
    if len(file_list) == 0:
        return ""
    report_dir = f"{project_path}{os.path.sep}build{os.path.sep}reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    report_path = f"{report_dir}{os.path.sep}pmd-{language}.html"
    if os.path.exists(report_path):
        os.remove(report_path)
    pmd_cli_path = f"{get_pmd_cli_path()} check"
    pmd_cli_arg_rule = f"-R {get_pmd_config_path()}"
    pmd_cli_arg_format = f"-f html"
    pmd_cli_arg_language = f"--force-language {language}"
    pmd_cli_arg_report = f"-r {report_path}"
    pmd_cli_arg_input = f"-d {file_list}"

    args = f"{pmd_cli_path} {pmd_cli_arg_rule} {pmd_cli_arg_format} {pmd_cli_arg_language} {pmd_cli_arg_report} {pmd_cli_arg_input}"
    try:
        subprocess.run(args, shell=True, stdout=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError:
        pass
    return report_path


def get_pmd_cli_path():
    # or pmd.bat
    return get_cli_path('pmd')


def get_pmd_config_path():
    return get_cli_path('rulesets.xml')


def get_detekt_cli_path():
    # or detekt-cli.bat
    return get_cli_path('detekt-cli')


def get_detekt_config_path():
    return get_cli_path('detekt.yml')


def get_cli_path(target):
    """
      获取 pmd或detekt cli 路径
      :return: pmd或detekt cli 路径
      """
    # 获取当前执行的 Python 脚本文件的路径
    script_path = os.path.abspath(__file__)
    # 获取该文件所在的目录路径
    py_project_path = os.path.dirname(os.path.dirname(script_path))
    py_lint_cli_path = f"{py_project_path}{os.path.sep}resources{os.path.sep}cli"
    for root, dirs, files in os.walk(py_lint_cli_path):
        for file in files:
            pmd_cli_path = os.path.join(root, file)
            if os.path.basename(pmd_cli_path) == target:
                return pmd_cli_path
    return None


if __name__ == "__main__":
    root_project_path = '/Users/wangjiang/Public/software/android-workplace/andruid'
    current_branch = 'release/7.63.0'
    target_branch = 'release/7.62.0'

    args = sys.argv[1:]
    if len(args) > 0:
        root_project_path = args[0]
    if len(args) > 1:
        current_branch = args[1]
    if len(args) > 2:
        target_branch = args[2]

    # 获取提交作者名字 user.name
    author = get_git_user()
    if author is None:
        exit(1)

    os.chdir(root_project_path)
    print(f"\ncd project: {root_project_path}")
    # 第一步：同步目标分支
    if not check_branch(target_branch, current_branch):
        exit(1)
    # 第二步：比较 current_branch 和 target_branch，获取提交的文件相对路径列表
    commit_file_path_set = get_commit_file_path_set(target_branch, current_branch, author)
    if commit_file_path_set is None or len(commit_file_path_set) == 0:
        exit(0)
    # 第三步：获取提交的文件全路径，并以,分割
    kotlin_file_list, java_file_list = get_commit_file_full_path_list(root_project_path, list(commit_file_path_set))
    # 第四步：将提交的文件全路径传给 detekt 和 pmd cli，生成 对应的 java 和 kotlin 静态代码检查 html 报告
    report_path_list = make_report(root_project_path, kotlin_file_list, java_file_list)
    for report_path in report_path_list:
        if len(report_path) > 0:
            print(f"Report File Path: {report_path}")
            open_file(report_path)
