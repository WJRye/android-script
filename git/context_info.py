# -*- coding: utf-8 -*-

import subprocess

from git import run_git_command


def get_git_user():
    try:
        git_user_name = run_git_command(['git', 'config', '--get', 'user.name']).strip()

        git_user_email = run_git_command(['git', 'config', '--get', 'user.email']).strip()

        return git_user_name, git_user_email
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None, None
