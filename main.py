# This is a sample Python script.
import os


# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def _print_script_info(dir, name):
    script_dir = os.path.join(dir, name)
    child_script_list = os.listdir(script_dir)
    print(f"{name} script: {', '.join(child_script_list)}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Project GitHub: https://github.com/WJRye/android-script")
    script_path = os.path.abspath(__file__)
    script_directory = os.path.dirname(script_path)
    print(f"Project Path: {script_directory}")
    _print_script_info(script_directory, 'adb')
    _print_script_info(script_directory, 'gradle')
    _print_script_info(script_directory, 'git')
