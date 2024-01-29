# -*- coding: utf-8 -*-
import sys

from __init__ import run_adb_command


def proc_info(category):
    """
    获取关于系统和进程的信息
    :param category: 系统的版本信息、CPU 信息、内存信息、当前运行的进程信息、文件系统信息
    :return: 信息结果
    """
    return run_adb_command(['adb', 'shell', 'cat', category]).stdout


def print_info(name, info):
    # 定义分割线长度
    line_length = 50
    # 输出分割线
    print(name)
    print(info)
    print("{}".format("-" * line_length))


def print_version():
    # 系统的版本信息
    version = proc_info("/proc/version")
    print_info("系统的版本信息：", version)


def print_cpuinfo():
    # CPU 信息
    cpuinfo = proc_info("/proc/cpuinfo")
    print_info("CPU 信息：", cpuinfo)


def print_meminfo():
    # 内存信息
    meminfo = proc_info("/proc/meminfo")
    print_info("内存信息：", meminfo)


def print_self_status():
    # 当前运行的进程信息
    status = proc_info("/proc/self/status")
    print_info("当前运行的进程信息：", status)


def print_self_mountinfo():
    # 文件系统信息
    mountinfo = proc_info("/proc/self/mountinfo")
    print_info("文件系统信息：", mountinfo)


if __name__ == "__main__":
    args = sys.argv[1:]
    for arg in args:
        if arg == "version":
            print_version()
            exit(0)
        if arg == "cpuinfo":
            print_cpuinfo()
            exit(0)
        if arg == "meminfo":
            print_meminfo()
            exit(0)
        if arg == "status":
            print_self_status()
            exit(0)
        if arg == "mountinfo":
            print_self_mountinfo()
            exit(0)
    print_version()
    print_cpuinfo()
    print_meminfo()
    print_self_status()
    print_self_mountinfo()
