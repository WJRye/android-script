import json
import os
import sys
from itertools import groupby

import pandas as pd

from __init__ import run_gradle_command, open_file


def execute_task():
    """
    执行 task
    :return: 是否成功，true表示成功，否则失败
    """
    task_name = ':iBiliPlayer:mergeDebugNativeLibs'
    command = ['./gradlew', task_name]
    print(f"{' '.join(command)}")
    result = run_gradle_command(command)
    print(result)
    return result


def deserialize_json(json_path):
    """
    :param json_path: json 路径
    :return: ReportInfo List
    """
    if not os.path.exists(json_path):
        print(f"FileNotExists:{json_path}")
        return None
    with (open(json_path, 'r') as file):
        data = json.load(file)
        # json 反序列化
        return [ReportInfo(name=report_data.get('name'), info=[
            NativeLibInfo(lib_name=native_lib_info.get('lib_name'),
                          so_relative_path_list=native_lib_info.get('so_relative_path_list'),
                          size_info=[SizeInfo(name=size_info.get('name'), size=size_info.get('size')) for size_info in
                                     native_lib_info.get('size_info')]) for native_lib_info in
            report_data.get('info', [])
        ]) for report_data in data]


def _custom_group_key(key=''):
    """
    :param key:如 armeabi-v7a/xx.so 或 arm64-v8a/xx.so等等
    :return: armeabi-v7a 或 arm64-v8a
    """
    return key[:key.index('/')]


def format_file_size(file_size):
    """
    格式化文件大小
    :param file_size: 文件大小
    :return: x B 或 KB 或 MB 或 GB 或 TB
    """
    # 定义文件大小单位
    units = ['B', 'KB', 'MB', 'GB', 'TB']

    # 初始单位为字节
    unit_index = 0

    # 将文件大小按1024递归缩小，直到小于1024
    while file_size >= 1024 and unit_index < len(units) - 1:
        file_size /= 1024.0
        unit_index += 1

    # 格式化字符串输出
    return "{:.2f} {}".format(file_size, units[unit_index])


def format_data(data, project_name):
    """
     将data格式化为表格
    :param data: json 结果地址
    :return:表格数据和表格标题
    """
    # html 中表格数据
    table_data = {}
    max_len = 0
    for report_info in data:
        for native_lib_info in report_info.info:
            # 对结果分组
            grouped_so_relative_path_list = [list(group) for key, group in
                                             groupby(native_lib_info.so_relative_path_list, _custom_group_key)]
            new_so_relative_path_list = []
            for item in grouped_so_relative_path_list:
                new_so_relative_path_list.append(', '.join(item))
            print(native_lib_info.lib_name + ": " + str(new_so_relative_path_list))
            native_lib_info.so_relative_path_list = new_so_relative_path_list
            so_relative_path_list_size = len(native_lib_info.so_relative_path_list)
            if so_relative_path_list_size > max_len:
                max_len = so_relative_path_list_size
    # native lib 数量
    num_libs = 0
    for report_info in data:
        num_libs = num_libs + len(report_info.info)
        for native_lib_info in report_info.info:
            while len(native_lib_info.so_relative_path_list) < max_len:
                native_lib_info.so_relative_path_list.append('')
            # 添加 so 的大小
            native_lib_info.so_relative_path_list.append(
                ", ".join(
                    f"{size_info.name}: {format_file_size(size_info.size)}" for size_info in native_lib_info.size_info))
            table_data[native_lib_info.lib_name] = native_lib_info.so_relative_path_list
    title = f"{project_name} native libs: {num_libs}"
    return title, table_data


def generate_html(title, table_data, output_path):
    """
    生成 html 文档报告
    :param title: html 文档标题
    :param table_data: native libs info
    :param output_path: html 文档报告文件地址
    """
    table = pd.DataFrame.from_dict(data=table_data).set_index(list(table_data.keys())).transpose()
    styled_html = """
      <style>
        table {
          width: 50%;
          border-collapse: collapse;
          margin-top: 10px;
        }
        th, td {
          border: 1px solid black;
          padding: 8px;
          text-align: left;
        }
      </style>
      """ + table.to_html()
    if os.path.exists(output_path):
        os.remove(output_path)
    html_content = f"<H1>{title}</H1>\n{styled_html}"
    with open(output_path, 'w') as f:
        f.write(html_content)
        f.flush()
        f.close()
    print(f"Report File Path: {output_path}")
    open_file(output_path)


class SizeInfo:
    def __init__(self, name, size):
        self.name = name
        self.size = size


class NativeLibInfo:
    def __init__(self, lib_name, so_relative_path_list, size_info):
        """
        :param lib_name: native lib 名称
        :param so_relative_path_list: so 依赖的项目相对路径信息列表
        """
        self.lib_name = lib_name
        self.so_relative_path_list = so_relative_path_list
        self.size_info = size_info


class ReportInfo:
    def __init__(self, name, info):
        """
        :param name: 本项目、子项目、三方库
        :param info: 依赖 so 信息列表
        """
        self.name = name
        self.info = info


if __name__ == "__main__":
    android_project_path = ''
    args = sys.argv[1:]
    if len(args) > 0:
        android_project_path = args[0]
    if not os.path.exists(android_project_path):
        exit(1)
    # 切换到安卓项目工作目录
    os.chdir(android_project_path)
    # 结果输出目录
    report_dir = f"{android_project_path}{os.path.sep}build{os.path.sep}reports{os.path.sep}so"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    # 结果输出地址
    report_path = f"{report_dir}{os.path.sep}native_libs.html"
    # 执行 ./gradlew mergeDebugNativeLibs 后的 json 结果存储地址，与 native_libs.gradle 中的对应
    json_path = f"{report_dir}{os.path.sep}native_libs.json"
    # 项目名称，方便在输出结果html中显示
    project_name = 'My Project'
    # 第一步：执行 ./gradlew :app:mergeDebugNativeLibs
    # execute_task()
    # 第二步：反序列化json
    data = deserialize_json(json_path)
    # 第三步：将数据转换为表格
    title, table_data = format_data(data, project_name)
    # 第四步：生成表格
    generate_html(title, table_data, report_path)
