# -*- coding: utf-8 -*-


from adb.__init__ import run_adb_command


def get_top_activity():
    result = run_adb_command(
        ['adb', 'shell', 'dumpsys', 'activity', 'top', '|', 'grep', 'ACTIVITY', '|', 'tail', '-n', '1'])
    print(result.stdout)


get_top_activity()
