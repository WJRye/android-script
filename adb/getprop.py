# -*- coding: utf-8 -*-

from adb.__init__ import run_adb_command


def getprop(category):
    result = run_adb_command(['adb', 'shell', 'getprop', '|', 'grep', category])
    print(result.stdout)


getprop("dalvik.vm")
getprop("ro.system.build")
getprop("ro.product")
