# -*- coding: utf-8 -*-

import re

from __init__ import run_adb_command, android_file_separator


def get_third_party_app_activities():
    """
    获取设备三方应用程序的 main activity
    :return: 返回设备上所有的三方应用程序的 main activity， key 是 应用程序包名，value 是 main activity
    """
    result = run_adb_command(['adb', 'shell', 'pm', 'list', 'packages', '-3', '-f'])
    app_activities = {}
    if result.returncode == 0:
        # 使用正则表达式提取包名
        package_names = re.findall(r"base.apk=(\S+)", result.stdout)
        print(package_names)
        # 获取每个应用程序的主活动
        for package_name in package_names:
            activity = get_main_activity(package_name)
            if activity:
                app_activities[package_name] = activity
    else:
        print(f"Error executing ADB command:\n{result.stderr}")
    return app_activities


def get_main_activity(package_name):
    """
    根据应用程序包名获取main activity
    :param package_name: 应用程序包名
    :return:应用程序 main activity
    """
    try:
        result = run_adb_command(['adb', 'shell', 'dumpsys', 'package', package_name, '|', 'grep', '-A', '1', 'MAIN'])
        if result.returncode == 0:
            # 使用正则表达式提取主活动
            text = result.stdout.strip()
            endIndex = text.index("filter")
            startIndex = text.index(package_name + android_file_separator, 0, endIndex)
            main_activity = text[startIndex:endIndex]
            # print("startIndex=" + str(startIndex) + ";endIndex=" + str(endIndex) + "main_activity=" + main_activity)
            if main_activity.startswith(package_name):
                return main_activity
            else:
                print("Error extracting main activity: index-" + package_name)
                return None
        else:
            print("Error extracting main activity: code-" + package_name)
            return None
    except AttributeError:
        print("Error extracting main activity: caught-" + package_name)


if __name__ == "__main__":
    app_activities = get_third_party_app_activities()
    if len(app_activities) > 0:
        for package_name, activity in app_activities.items():
            print(f"Package: {package_name}, Main Activity: {activity}")
