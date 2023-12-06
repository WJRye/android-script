# -*- coding: utf-8 -*-
import os
import time

from adb.__init__ import run_adb_command, open_file, android_file_separator


def screen_cap():
    # Screenshot_20220502_175425.png
    current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    screen_shot_name = 'Screenshot_' + current_time + '.png'
    # 获取手机外部存储目录
    external_result = run_adb_command(['adb', 'shell', "'echo'", '$EXTERNAL_STORAGE'])
    external_dir = external_result.stdout.strip()
    screen_shot_file_dir = external_dir + android_file_separator + 'Pictures' + android_file_separator + 'Screenshots'
    screen_shot_file_path = screen_shot_file_dir + android_file_separator + screen_shot_name
    screen_cap_result = run_adb_command(['adb', 'shell', 'screencap', '-p', screen_shot_file_path])
    if screen_cap_result.returncode == 0:
        return [screen_shot_file_path, screen_shot_name]
    else:
        print(screen_cap_result.stderr)
        return ["", ""]


def pull_screen_shot(src_file_path, des_file_path):
    pull_screen_shot_result = run_adb_command(['adb', 'pull', src_file_path, des_file_path])
    return pull_screen_shot_result.returncode == 0


screen_cap_result = screen_cap()
file_path = screen_cap_result[0]
if file_path != "":
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    des_file_path = desktop_path + android_file_separator + screen_cap_result[1]
    result = pull_screen_shot(file_path, des_file_path)
    if result:
        print("Success")
        print("From: " + file_path + ", To: " + des_file_path)
        open_file(des_file_path)
else:
    print("Failed")
