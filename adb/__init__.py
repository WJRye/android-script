# -*- coding: utf-8 -*-
import platform
import subprocess

android_file_separator = '/'


def run_adb_command(command):
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None


def open_file(file_path):
    system = platform.system().lower()
    if system == "darwin":  # macOS
        subprocess.run(["open", file_path])
    elif system == "linux":  # Linux
        subprocess.run(["xdg-open", file_path])
    elif system == "windows":  # Windows
        subprocess.run(["start", file_path], shell=True)
    else:
        print("Unsupported operating system.")
