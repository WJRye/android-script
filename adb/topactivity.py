# -*- coding: utf-8 -*-


from __init__ import run_adb_command


def get_top_activity():
    """
    获取设备当前应用程序当前activity，命令：adb shell dumpsys activity top | grep ACTIVITY | tail -n 1
    :return: 设备当前应用程序当前activity
    """
    return run_adb_command(
        ['adb', 'shell', 'dumpsys', 'activity', 'top', '|', 'grep', 'ACTIVITY', '|', 'tail', '-n', '1']).stdout


if __name__ == "__main__":
    result = get_top_activity()
    print(result)
