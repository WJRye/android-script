# -*- coding: utf-8 -*-


from adb.__init__ import run_adb_command


def list_packages_third():
    result = run_adb_command(['adb', 'shell', 'pm', 'list', 'packages', '-3'])
    print(result.stdout)


list_packages_third()
