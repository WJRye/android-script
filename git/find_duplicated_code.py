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


def make_cpd_report(project_path, pmd_cli_path, java_src_path):
    """
    生成重复代码报告
    :param project_path: 项目路径
    :param pmd_cli_path: detekt 和 pmd cli 路径
    :param java_src_path: java 文件路径地址
    :return: html 报告地址
    """
    report_dir = f"{project_path}{os.path.sep}build{os.path.sep}reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    report_path = f"{report_dir}{os.path.sep}pmd-cpd.html"
    if os.path.exists(report_path):
        os.remove(report_path)
    cpd_cli_arg_cpd = f"{pmd_cli_path} cpd"
    cpd_cli_arg_token = "--minimum-tokens=120"
    cpd_cli_arg_dir = f"--dir={java_src_path}"
    cpd_cli_arg_language = "--language=java"
    cpd_cli_arg_format = "-f text"
    cpd_cli_arg_no_fail = "--no-fail-on-violation"
    cpd_cli_arg_encoding = "--encoding=UTF-8"
    cpd_cli_arg_ignore_ignore_annotation = "--ignore-annotations"
    args = f"{cpd_cli_arg_cpd} {cpd_cli_arg_token} {cpd_cli_arg_dir} {cpd_cli_arg_language} {cpd_cli_arg_format} {cpd_cli_arg_no_fail} {cpd_cli_arg_encoding} {cpd_cli_arg_ignore_ignore_annotation}"
    try:
        output = subprocess.run(args, shell=True, stdout=subprocess.PIPE, text=True)
        lines = output.stdout.split('\n')
        content = ""
        count = 0
        for line in lines:
            if line.startswith('='):
                count += 1
                content += "<hr>"
                continue
            content += line + "</br>"
        if count > 0:
            count += 2
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


def get_java_src_path(project_path):
    """
    获取项目src文件夹下的java文件路径列表，以,分割
    :param project_path: 项目路径
    :return: java 文件路径列表
    """
    java_src_path_dict = {}
    src_main_dir_dict = {}
    for root, dirs, files in os.walk(project_path):
        dirname = os.path.dirname(root)
        suffix = f"{os.path.sep}src"
        if dirname.endswith(suffix):
            sub_project_path = dirname[0:len(dirname) - len(suffix)]
            src_main_dir_dict[sub_project_path] = dirname

    for sub_project_path, src_main_dir in src_main_dir_dict.items():
        java_src_path_list = []
        for root, dirs, files in os.walk(src_main_dir):
            for file in files:
                if os.path.abspath(file).endswith(".java"):
                    java_src_path_list.append(os.path.join(root, file))
        if len(java_src_path_list) > 0:
            java_src_path_dict[sub_project_path] = ','.join(java_src_path_list)

    return java_src_path_dict


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
    root_project_path = '/Users/wangjiang/Public/software/android-workplace/andruid/common/editor'
    current_branch = ''

    args = sys.argv[1:]
    if len(args) > 0:
        root_project_path = args[0]
    if len(args) > 1:
        current_branch = args[1]

    pmd_cli_path = get_pmd_cli_path()
    if pmd_cli_path is None:
        print("Can't find pmd cli path")
        exit(1)

    # 第一步：同步分支
    os.chdir(root_project_path)
    if len(current_branch) > 0 and not check_branch(current_branch):
        exit(1)
    # 第二步：获取 java 文件
    java_src_path_dict = get_java_src_path(root_project_path)
    for project_path, java_src_path in java_src_path_dict.items():
        report_path = make_cpd_report(project_path, pmd_cli_path, java_src_path)
        print(f"Report File Path: {report_path}")
        open_file(report_path)
