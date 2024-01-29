# -*- coding: utf-8 -*-
import os
import time

from __init__ import run_adb_command, open_file, android_file_separator


def screen_cap():
    """
    获取截屏文件，文件命令例如：Screenshot_20220502_175425.png
    :return: 截屏文件路径和名字
    """
    # Screenshot_20220502_175425.png
    current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    screen_shot_name = 'Screenshot_' + current_time + '.png'
    # 获取手机外部存储目录
    external_result = run_adb_command(['adb', 'shell', "'echo'", '$EXTERNAL_STORAGE'])
    external_dir = external_result.stdout.strip()
    screen_shot_file_dir = external_dir + android_file_separator + 'Pictures' + android_file_separator + 'Screenshots'
    run_adb_command(['adb', 'shell', 'mkdir', '-p', screen_shot_file_dir])
    screen_shot_file_path = screen_shot_file_dir + android_file_separator + screen_shot_name
    screen_cap_result = run_adb_command(['adb', 'shell', 'screencap', '-p', screen_shot_file_path])
    if screen_cap_result.returncode == 0:
        return [screen_shot_file_path, screen_shot_name]
    else:
        print(screen_cap_result.stderr)
        return ["", ""]


def pull_screen_shot(src_file_path, des_file_path):
    """
    将截屏文件存储到桌面
    :param src_file_path: 源文件地址
    :param des_file_path: 目标文件地址
    :return: True表示成功，否则False
    """
    pull_screen_shot_result = run_adb_command(['adb', 'pull', src_file_path, des_file_path])
    return pull_screen_shot_result.returncode == 0


if __name__ == "__main__":
    screen_cap_result = screen_cap()
    file_path = screen_cap_result[0]
    if len(file_path) > 0:
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        des_file_path = desktop_path + android_file_separator + screen_cap_result[1]
        result = pull_screen_shot(file_path, des_file_path)
        if result:
            print("From: " + file_path + ", To: " + des_file_path)
            open_file(des_file_path)
    else:
        print("Failed")
