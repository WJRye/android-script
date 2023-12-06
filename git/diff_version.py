# -*- coding: utf-8 -*-
import difflib
import os
import subprocess

from git import git_current_project_path, run_git_command, file_separator
from git.__init__ import run_open_file
from git.context_info import get_git_user
from git.diff_model import DiffModel


def _get_commit_file_path_set(command):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        file_path_list = []
        # 实时打印命令的输出
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                process.kill()
                break
            if output:
                text = output.strip().replace("\t", "")
                if text.startswith('M'):
                    file_path = text[1:]
                    file_path_list.append(file_path)

        return set(file_path_list)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None


def _get_commit_file_diff_content(last_branch, cur_branch, author):
    diff_models = []
    diff_model = DiffModel()
    repo_dir = git_current_project_path
    diff_model.repo = repo_dir
    os.chdir(repo_dir)
    commit_file_path_set = _get_commit_file_path_set(
        ['git', 'log', cur_branch + '...' + last_branch, '--author=' + author,
         '--name-status', '--oneline'])
    diff_model.commit_files = commit_file_path_set
    diff_model.diff_output = ""
    for file_path in commit_file_path_set:
        diff_result = run_git_command(
            ['git', 'diff', last_branch + '..' + cur_branch, '--', repo_dir + file_separator + file_path])
        diff_model.diff_output += (diff_result + "\n")
        diff_models.append(diff_model)
    return diff_models


def _save_diff_result(output, last_branch, cur_branch, author):
    txt_file_path = git_current_project_path + file_separator + _getFileName(last_branch, cur_branch, author, ".txt")

    text = ""
    for model in output:
        text += model.repo
        text += "\n"
        for commit_file in model.commit_files:
            text += commit_file
            text += "\n"
        text += "\n"
        text += model.diff_output
        text += "\n"

    with open(txt_file_path, 'w') as txt_file:
        txt_file.write(text)

    print("Report Text Path: " + txt_file_path)

    body = ""
    for model in output:
        body += f"""<div class="bordered-div">"""
        body += f"""<font size="6" color="blue" style="bold">{model.repo}:</font>"""
        body += "</br>"
        body += "</br>"
        for commit_file in model.commit_files:
            body += f"""<font color="yellow">{commit_file}</font>"""
            body += "</br>"
        body += "</br>"
        body += model.diff_output
        body += "</br>"
        body += f"""</div>"""

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Git Diff Output</title>
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
        <pre>
           {body}
        </pre>
    </body>
    </html>
    """
    html_file_path = git_current_project_path + file_separator + _getFileName(last_branch, cur_branch, author, ".html")

    if os.path.exists(html_file_path):
        os.remove(html_file_path)
    with open(html_file_path, 'w') as html_file:
        html_file.write(html_content)

    print("Report Html Path: " + html_file_path)
    run_open_file(html_file_path)


def _getFileName(last_branch, cur_branch, author, suffix):
    return author + '-' + cur_branch.replace(file_separator, '-') + '-diff-' + last_branch.replace(file_separator,
                                                                                                   '-') + suffix


def _get_commit_file_diff_content_format(last_branch, cur_branch, author):
    last_content_lines = []
    cur_content_lines = []

    repo_dir = git_current_project_path
    os.chdir(repo_dir)
    commit_file_path_set = _get_commit_file_path_set(
        ['git', 'log', cur_branch + '...' + last_branch, '--author=' + author,
         '--name-status', '--oneline'])
    for file_path in commit_file_path_set:
        try:
            last_content = run_git_command(
                ['git', 'show', last_branch + ":" + file_path])
            last_content_lines += last_content.splitlines()
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
        cur_content = run_git_command(
            ['git', 'show', cur_branch + ":" + file_path])
        cur_content_lines += cur_content.splitlines()

    return last_content_lines, cur_content_lines


def _save_diff_result_format(last_branch, cur_branch, author, fromlines, tolines):
    file_name = _getFileName(last_branch, cur_branch, author, "-format.html")
    html_file_path = git_current_project_path + file_separator + file_name
    d = difflib.HtmlDiff()
    diff_html = d.make_file(fromlines, tolines, last_branch, cur_branch, context=True)
    if os.path.exists(html_file_path):
        os.remove(html_file_path)
    with open(html_file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(diff_html)
    print("Report Html-Format Path: " + html_file_path)
    run_open_file(html_file_path)


last_branch = "release/7.57.0"
cur_branch = "release/7.58.0"
git_user_name, git_user_email = get_git_user()
author = git_user_name


diff_output = _get_commit_file_diff_content(last_branch, cur_branch, author)
_save_diff_result(diff_output, last_branch, cur_branch, author)

# format html
diff_output_format_fromlines, diff_output_format_tolines = _get_commit_file_diff_content_format(last_branch, cur_branch,
                                                                                                author)
_save_diff_result_format(last_branch, cur_branch, author, diff_output_format_fromlines, diff_output_format_tolines)
