# -*- coding: utf-8 -*-

import os
import sys

script_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(script_directory)
sys.path.append(parent_directory)

from adb.__init__ import run_adb_command


def wm_info(command):
    result = run_adb_command(['adb', 'shell', 'wm', command])
    print(result.stdout)


wm_info("size")
wm_info("density")
