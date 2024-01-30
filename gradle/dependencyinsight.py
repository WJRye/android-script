import os
import sys

from __init__ import run_gradle_command, open_file, save_result_to_file


def execute_task_dependency_insight(dependency):
    task_name = ':app:dependencyInsight'
    command = ['./gradlew', task_name, '--configuration', 'releaseRuntimeClasspath', '--dependency',
               f"{dependency}"]
    print(' '.join(command))
    result = run_gradle_command(command)
    print(result)
    return task_name, result


if __name__ == "__main__":
    android_project_path = ''
    # 例如 io.reactivex.rxjava3:rxjava
    dependency = ''
    args = sys.argv[1:]
    if len(args) > 0:
        android_project_path = args[0]
    if len(args) > 1:
        dependency = args[1]
    if not os.path.exists(android_project_path):
        exit(1)
    # 切换到安卓项目工作目录
    os.chdir(android_project_path)
    # 第一步：执行 ./gradlew :app:dependencies 任务
    task_name, task_result = execute_task_dependency_insight(dependency)
    # 第二步：保存任务结果到文件
    report_dir = f"{android_project_path}{os.path.sep}build{os.path.sep}reports"
    file_name = task_name[1:].replace(':', '-')
    file_path = save_result_to_file(report_dir, file_name, task_name, task_result)
    # 第三步：打开结果文件
    print(f"Report File Path: {file_path}")
    open_file(file_path)
