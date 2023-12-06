# -*- coding: utf-8 -*-


from adb.__init__ import run_adb_command


def proc_info(command):
    result = run_adb_command(['adb', 'shell', 'cat', command])
    print(result.stdout)


proc_info("/proc/meminfo")
proc_info("/proc/cpuinfo")
