# -*- coding: utf-8 -*-

import os
import sys

script_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(script_directory)
sys.path.append(parent_directory)

from __init__ import run_adb_command


def wm_info(category):
    """
    获取设备屏幕信息，命令：adb shell wm size，adb shell wm density
    :param category: 屏幕大小、屏幕密度
    :return: 屏幕信息
    """
    return run_adb_command(['adb', 'shell', 'wm', category]).stdout


if __name__ == "__main__":
    size = wm_info("size")
    print(size)
    density = wm_info("density")
    print(density)
