# -*- coding: utf-8 -*-


from __init__ import run_adb_command


def list_packages_third():
    """
    获取设备上的三方应用程序包名
    :return: 设备上的三方应用程序包名列表
    """
    return run_adb_command(['adb', 'shell', 'pm', 'list', 'packages', '-3']).stdout


if __name__ == "__main__":
    result = list_packages_third()
    print(result)
