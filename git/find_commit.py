import os
import re
import sys

from __init__ import run_git_command, open_file


def find_commit(commit_id):
    """
    查找包含 commit id 的所有分支名称
    :param commit_id: commit id 值
    :return: 分支列表
    """
    result = run_git_command(
        ['git', 'branch', '--contains', commit_id, '--all'])
    if result is not None:
        return result.splitlines()
    return []


def compare_versions(version1, version2):
    """
    比较版本号
    :param version1: 7.63.0
    :param version2: 7.64.0
    :return: 如果 version1<version2，返回-1；如果version1>version2，返回1；如果version1=version2，返回0
    """
    # 如果 version1 或 version2 含有字母，则认为无效，返回0
    if not version1.isdigit():
        return 0
    if not version2.isdigit():
        return 0

    parts1 = list(map(int, version1.split('.')))
    parts2 = list(map(int, version2.split('.')))

    length = max(len(parts1), len(parts2))

    for i in range(length):
        part1 = parts1[i] if i < len(parts1) else 0
        part2 = parts2[i] if i < len(parts2) else 0

        if part1 < part2:
            return -1
        elif part1 > part2:
            return 1

    return 0


def find_min_release_branch(branch_list):
    """
    筛选出版本最低的 release branch，也就是找到 commit id 第一次出现的 release branch
    :param branch_list: 分支列表
    :return: 版本最低的 release branch
    """
    min_version_name = None
    min_branch = None
    release_prefix = 'remotes/origin/release/'
    for branch in branch_list:
        index = branch.find(release_prefix)
        if index >= 0:
            version_name = branch[index + len(release_prefix):]
            if min_version_name is None:
                min_version_name = version_name
                min_branch = branch
            else:
                if compare_versions(min_version_name, version_name) > 0:
                    min_version_name = version_name
                    min_branch = branch
    if min_branch is None:
        return None
    return min_branch.strip()


def get_commit_info(commit_id):
    """
    获取提交的信息
    :param commit_id: commit id值
    :return: author 作者 和 commit 信息
    """
    author = run_git_command(['git', 'log', '-n', '1', '--format=%an', commit_id]).strip()
    commit_info = run_git_command(
        ['git', 'show', commit_id])
    return author, commit_info


def find_last_version(current_version):
    # 定义版本号的正则表达式
    version_pattern = re.compile(r'(\d+)\.(\d+)\.0')

    # 使用正则表达式匹配版本号
    match = version_pattern.match(current_version)

    if match:
        # 提取主版本号和次版本号
        major_version = int(match.group(1))
        minor_version = int(match.group(2))

        # 判断是否需要增加主版本号
        if minor_version == 00:
            next_major_version = major_version - 1
            next_minor_version = 99
        else:
            next_major_version = major_version
            next_minor_version = minor_version - 1

        # 构造下一个版本号字符串，去掉前导零
        next_version = f'{next_major_version:0}.{next_minor_version:02d}.0'
        return next_version
    else:
        return current_version


def get_branch_commit_list(current_branch, last_branch, author):
    return run_git_command(['git', 'log', f"{current_branch}...{last_branch}", f"--author={author}",
                            '--pretty=format:"%H - %an, %ar : %s"', '--stat'])


def make_html_file(project_path, commit_id, title, content):
    """
    生成 html 文件报告
    :param project_path: 项目路径
    :param commit_id: commit id值
    :param title: html 文档标题
    :param content: html 文档内容
    :return: html 文件报告路径
    """
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
    html_report_dir = f"{project_path}{os.path.sep}build{os.path.sep}reports{os.path.sep}diff{os.path.sep}commit_id"
    if not os.path.exists(html_report_dir):
        os.mkdir(html_report_dir)
    html_file_path = f"{html_report_dir}{os.path.sep}{commit_id}.html"
    if os.path.exists(html_file_path):
        # 如果文件存在，删除文件
        os.remove(html_file_path)
    with open(html_file_path, 'w') as html_file:
        html_file.write(html_content)
        html_file.close()
    print(f"Html Report Path: {html_file_path}")
    return html_file_path


if __name__ == "__main__":
    project_path = ''
    commit_id = ''

    args = sys.argv[1:]
    if len(args) > 0 and os.path.exists(args[0]):
        project_path = args[0]
    if len(args) and len(args[1]) > 1:
        commit_id = args[1]

    os.chdir(project_path)
    # 第一步：查找包含 commit id 的所有分支名称
    branch_list = find_commit(commit_id)
    # 第二步：找到 commit id 第一次出现的 release 分支
    min_release_branch = find_min_release_branch(branch_list)
    if min_release_branch is None:
        print(f"Can't find commit id: {commit_id} in release branch.")
        exit(1)

    # 第三步：获取 commit 信息
    author, commit_info = get_commit_info(commit_id)
    last_release_branch = min_release_branch[0:min_release_branch.rfind('/') + 1:] + find_last_version(
        min_release_branch[min_release_branch.rfind('/') + 1:])
    branch_commit_list = get_branch_commit_list(min_release_branch, last_release_branch, author)
    branch_commit_list_content = f"<hr><h2>在 {min_release_branch} 中 {author} 还有以下提交：</h2><p>{branch_commit_list}</p>"

    content = commit_info + branch_commit_list_content

    title = f"<p>Project: {project_path}</p>The commit id: {commit_id} first appears in the release branch: {min_release_branch}"
    # 第四步：生成 html 文档报告
    html_file_path = make_html_file(project_path, commit_id, title, content)
    # 第五步：打开 html 文档报告
    open_file(html_file_path)
