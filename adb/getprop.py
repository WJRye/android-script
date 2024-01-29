# -*- coding: utf-8 -*-

from __init__ import run_adb_command


def getprop(category):
    result = run_adb_command(['adb', 'shell', 'getprop', '|', 'grep', category])
    print(result.stdout)


if __name__ == "__main__":
    getprop("dalvik.vm")
    getprop("ro.system.build")
    getprop("ro.product")
