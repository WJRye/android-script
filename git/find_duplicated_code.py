import os
import subprocess
import sys

from __init__ import open_file, sync_branch


def check_branch(current_branch):
    """
    检查分支
    :param current_branch: 当前分支
    :return: 检查分支结果，True表示成功，否则失败
    """
    if sync_branch(current_branch) is None:
        print(f"Sync branch: {current_branch} Failed")
        return False
    return True


def make_cpd_report(project_path, file_list, language):
    """
    生成重复代码报告
    :param project_path: 项目路径
    :param file_list: java 文件路径地址
    :return: html 报告地址
    """
    build_dir = f"{project_path}{os.path.sep}build"
    if os.path.exists(build_dir) and os.path.isfile(build_dir):
        build_dir = f"{project_path}{os.path.sep}build-py"
    report_dir = f"{build_dir}{os.path.sep}reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    report_path = f"{report_dir}{os.path.sep}pmd-cpd-{language}.html"
    if os.path.exists(report_path):
        os.remove(report_path)
    cpd_cli_arg_cpd = f"{get_pmd_cli_path()} cpd"
    cpd_cli_arg_token = "--minimum-tokens=120"
    cpd_cli_arg_dir = f"--dir={file_list}"
    cpd_cli_arg_language = f"--language={language}"
    cpd_cli_arg_format = "-f text"
    cpd_cli_arg_no_fail = "--no-fail-on-violation"
    cpd_cli_arg_encoding = "--encoding=UTF-8"
    cpd_cli_arg_ignore_annotations = "--ignore-annotations"
    cpd_cli_arg_skip_lexical_errors = " --skip-lexical-errors"
    args = f"{cpd_cli_arg_cpd} {cpd_cli_arg_token} {cpd_cli_arg_dir} {cpd_cli_arg_language} {cpd_cli_arg_format} {cpd_cli_arg_no_fail} {cpd_cli_arg_encoding} {cpd_cli_arg_ignore_annotations} {cpd_cli_arg_skip_lexical_errors}"
    try:
        output = subprocess.run(args, shell=True, stdout=subprocess.PIPE, text=True)
        lines = output.stdout.split('\n')
        content = ""
        count = 1
        for line in lines:
            if line.startswith('='):
                count += 1
                content += "<hr>"
                continue
            content += line + "</br>"
        if count == 1:
            count = 0
        title = f"{project_path} Duplicate code: {count} found"
        html_content = f"""
           <!DOCTYPE html>
           <html lang="en">
           <head>
               <meta charset="UTF-8">
               <style>
                   body {{
                       font-family: 'Arial', sans-serif;
                       background-color: #272822;
                       color: #f8f8f2;
                       margin: 20px;
                   }}
                   pre {{
                       white-space: pre-wrap;
                       font-size: 14px;
                       line-height: 1.5;
                       background-color: #1e1e1e;
                       padding: 20px;
                       border: 1px solid #333;
                       border-radius: 5px;
                       overflow-x: auto;
                   }}
                   .header {{
                       color: #66d9ef;
                   }}
                   .bordered-div {{
                       border: 1px solid #000;
                       padding: 10px;
                   }}
               </style>
           </head>
           <body>
               <h1>{title}</h1>
               <pre>
                  {content}
               </pre>
           </body>
           </html>
           """
        with open(report_path, 'w') as html_file:
            html_file.write(html_content)
            html_file.close()
    except subprocess.CalledProcessError:
        pass
    return report_path


def get_file_path_dict(project_path, languages, exclude_file_dirs):
    """
    获取项目src文件夹下的java文件路径列表，以,分割
    :param project_path: 项目路径
    :param languages: 语言
    :param exclude_file_dirs: 不包含的目录
    :return: 文件路径列表
    """
    file_path_dict = {}
    for language in languages.keys():
        file_path_dict[language] = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            exclude = False
            for exclude_file_dir in exclude_file_dirs:
                if file_path.find(exclude_file_dir) > 0:
                    exclude = True
                    break
            if exclude:
                continue
            for language, file_suffix in languages.items():
                if file_path.endswith(file_suffix):
                    file_path_dict[language].append(file_path)
                    break

    return file_path_dict


def get_pmd_cli_path():
    """
    获取 pmd cli 路径
    :return: pmd cli 路径
    """
    # 获取当前执行的 Python 脚本文件的路径
    script_path = os.path.abspath(__file__)
    # 获取该文件所在的目录路径
    py_project_path = os.path.dirname(os.path.dirname(script_path))
    py_lint_cli_path = f"{py_project_path}{os.path.sep}resources{os.path.sep}cli"
    for root, dirs, files in os.walk(py_lint_cli_path):
        for file in files:
            pmd_cli_path = os.path.join(root, file)
            # or 'pmd.bat'
            if os.path.basename(pmd_cli_path) == 'pmd':
                return pmd_cli_path
    return None


if __name__ == "__main__":
    root_project_path = ''
    current_branch = ''

    args = sys.argv[1:]
    if len(args) > 0:
        root_project_path = args[0]
    if len(args) > 1:
        current_branch = args[1]

    # 第一步：同步分支
    os.chdir(root_project_path)
    if len(current_branch) > 0 and not check_branch(current_branch):
        exit(1)
    # 第二步：获取文件
    default_language = {'java': '.java', 'kotlin': '.kt', 'python': '.py', 'swift': '.swift'}
    exclude_file_dirs = ['venv', 'build', 'gen']
    file_path_dict = get_file_path_dict(root_project_path, default_language, exclude_file_dirs)
    if len(file_path_dict) == 0:
        exit(0)
    for language, file_path_list in file_path_dict.items():
        if len(file_path_list) == 0:
            continue
        report_path = make_cpd_report(root_project_path, file_path_list, language)
        print(f"Report File Path: {report_path}")
        open_file(report_path)
