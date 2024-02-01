import difflib
import os
import subprocess
import sys

from __init__ import run_git_command, open_file, check_branch, get_git_user


def get_commit_file_path_set(target_branch, current_branch, author):
    """
    比对 branch，获取提交的文件相对路径列表
    :param target_branch: 要比对的分支
    :param current_branch: 当前分支
    :param author: git user.name
    :return: 提交的文件相对路径列表
    """
    try:
        # 如果当前开发分支与master或release分支比对，使用 git log master..feature
        if (target_branch == 'master' or target_branch.startswith('release')) and not current_branch.startswith(
                'release'):
            branch_command = f"{target_branch}..{current_branch}"
        else:
            # 否则都是用 git log branch1...branch2
            branch_command = f"{current_branch}...{target_branch}"

        command = ['git', 'log', branch_command, f"--author={author}",
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
                    # 重命名文件
                    if output.strip().startswith('R'):
                        rename_file_path = output.strip().split('\t')[1]
                        rename_file_path_list.add(rename_file_path)
        if len(file_path_list) == 0:
            print(f"{' '.join(command)}: No commit files")
            return None
        for rename_file_path in rename_file_path_list:
            file_path_list.remove(rename_file_path)
        return file_path_list
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None


def get_commit_content(commit_file_path_set, target_branch, current_branch):
    """
    获取提交的内容
    :param commit_file_path_set: 提交的文件相对路径列表
    :param target_branch: 要比对的分支
    :param current_branch: 当前分支
    :return: 要比对的分支内容，当前分支内容
    """
    target_content_lines = []
    current_content_lines = []
    for file_path in commit_file_path_set:
        try:
            file_in_target_branch = run_git_command(['git', 'ls-tree', target_branch, file_path])
            if file_in_target_branch.find('blob') >= 0:
                target_content = run_git_command(
                    ['git', 'show', target_branch + ":" + file_path])
                if target_content is not None:
                    target_content_lines += target_content.splitlines()
        except UnicodeDecodeError as e:
            target_content_lines += [file_path + '\n']
        try:
            file_in_current_branch = run_git_command(['git', 'ls-tree', current_branch, file_path])
            if file_in_current_branch.find('blob') >= 0:
                current_content = run_git_command(
                    ['git', 'show', current_branch + ":" + file_path])
                if current_content is not None:
                    current_content_lines += current_content.splitlines()
        except UnicodeDecodeError as e:
            current_content_lines += [file_path + '\n']
    return target_content_lines, current_content_lines


def make_html_file(project_path, target_branch_content, current_branch_content, target_branch, current_branch, author):
    """
    生成 html 文件报告
    :param project_path: 项目路径
    :param target_branch_content: 要比对的分支内容
    :param current_branch_content:  当前分支内容
    :param target_branch: 要比对的分支
    :param current_branch: 当前分支
    :param author: git user.name
    :return: html 文件报告路径
    """
    html_report_dir = f"{project_path}{os.path.sep}build{os.path.sep}reports{os.path.sep}diff{os.path.sep}{author}"
    if not os.path.exists(html_report_dir):
        os.makedirs(html_report_dir)
    html_file_path = f"{html_report_dir}{os.path.sep}{current_branch.replace('/', '_')}-diff-{target_branch.replace('/', '_')}.html"
    d = difflib.HtmlDiff(wrapcolumn=120)
    diff_html = d.make_file(target_branch_content, current_branch_content, target_branch, current_branch, context=True)
    if os.path.exists(html_file_path):
        os.remove(html_file_path)
    with open(html_file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(diff_html)
        html_file.close()
    print(f"{project_path} Html Report Path: {html_file_path}")
    return html_file_path


if __name__ == "__main__":
    project_path = '/Users/wangjiang/Public/software/android-workplace/andruid'
    target_branch = 'master'
    current_branch = 'feature/upper/7.6x.0_game_factory_v1.0'

    args = sys.argv[1:]
    if len(args) > 0:
        project_path = args[0]
    if len(args) > 1:
        current_branch = args[1]
    if len(args) > 2:
        target_branch = args[2]

    os.chdir(project_path)
    # 第一步：同步目标分支
    if not check_branch(target_branch, current_branch):
        exit(1)
    # 第二步：获取自己的git账户名称
    author = get_git_user()
    if author is None:
        exit(1)
    # 第三步：比较 current_branch 和 target_branch，获取提交的文件列表
    commit_file_path_set = get_commit_file_path_set(target_branch, current_branch, author)
    if commit_file_path_set is None or len(commit_file_path_set) == 0:
        exit(0)
    # 第四步：根据文件列表获取文件内容
    target_branch_content, current_branch_content = get_commit_content(commit_file_path_set, target_branch,
                                                                       current_branch)
    # 第五步：生成 html 报告文件
    report_html_file_path = make_html_file(project_path, target_branch_content, current_branch_content, target_branch,
                                           current_branch, author)
    # 第六步：打开 html 报告文件
    open_file(report_html_file_path)
