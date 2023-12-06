# -*- coding: utf-8 -*-
import os
import platform
import subprocess

file_separator = os.path.sep
public_dir = os.path.join(os.path.expanduser("~"), "Public")
android_project_workplace_dir = public_dir + file_separator + 'software' + file_separator + 'workplace'
android_project_path = android_project_workplace_dir + file_separator + 'pink' + file_separator + 'andruid'
git_current_project_path = android_project_path
print("current_project_path:" + git_current_project_path)
git_command = 'git'


def run_git_command(command):
    return subprocess.check_output(command, text=True)


def run_open_file(file_path):
    system = platform.system().lower()
    if system == "darwin":  # macOS
        subprocess.run(["open", file_path])
    elif system == "linux":  # Linux
        subprocess.run(["xdg-open", file_path])
    elif system == "windows":  # Windows
        subprocess.run(["start", file_path], shell=True)
    else:
        print("Unsupported operating system.")
