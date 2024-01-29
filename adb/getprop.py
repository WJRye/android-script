# -*- coding: utf-8 -*-

from __init__ import run_adb_command


def getprop(category):
    """
    获取设备的属性信息
    :param category：dalvik信息、build信息、product信息
    :return:
    """
    result = run_adb_command(['adb', 'shell', 'getprop', '|', 'grep', category])
    print(result.stdout)


if __name__ == "__main__":
    getprop("dalvik.vm")
    getprop("ro.system.build")
    getprop("ro.product")
