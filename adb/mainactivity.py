# -*- coding: utf-8 -*-

import re

from adb.__init__ import run_adb_command, android_file_separator


def get_third_party_app_activities():
    # "adb shell pm list packages -3 -f"
    result = run_adb_command(['adb', 'shell', 'pm', 'list', 'packages', '-3', '-f'])
    if result.returncode == 0:
        # 使用正则表达式提取包名
        package_names = re.findall(r"base.apk=(\S+)", result.stdout)
        print(package_names)
        # 获取每个应用程序的主活动
        for package_name in package_names:
            activity = get_main_activity(package_name)
            if activity:
                print(f"Package: {package_name}, Main Activity: {activity}")

    else:
        print(f"Error executing ADB command:\n{result.stderr}")


def get_main_activity(package_name):
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


get_third_party_app_activities()
