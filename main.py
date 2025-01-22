import os.path
from typing import Tuple
from DocxBuilder.report import Report
from ResultBuilder import *
from TaskBuilder import *
from UI import UIMainWindow
from ZFile.z_file import SCHEME_ALL_CALCULATIONS
from os.path import isfile, isdir, join
from os import listdir


SEPARATOR = '\\'


def collect_files_via_dir(directory: str, ext: str = '*') -> Tuple[str]:
    assert isinstance(directory, str)
    directories = [directory]
    directory_files = []
    while len(directories) != 0:
        c_dir = directories.pop()
        for file in listdir(c_dir):
            c_path = join(c_dir, file)
            if isdir(c_path):
                directories.append(c_path)
            if ext == '*':
                directory_files.append(c_path)
                continue
            if isfile(c_path) and c_path.endswith(ext):
                directory_files.append(c_path)
    return tuple(f"{v.replace(SEPARATOR, '/')}" for v in directory_files)


def merge_tasks_from_dir(directory: str):
    '''
    Объединяет разрозненные файлы настроек в один единый файл
    '''
    settings_files = collect_files_via_dir(directory)
    params_list = SchemeParams.read_and_merge(settings_files)
    SchemeParams.write_params_list(os.path.join("E:\GitHub\ZemaxUtils\ZemaxUtils\ZemaxSchemesSettings",
                                                "combined_params.json"), params_list)


def build_polychrome_matrix():
    # Расположение Zemax файла прототипа
    z_file_src = r"\ZemaxSchemes\prototype.zmx"
    # Расположение файла с настройками, которе
    # требуется применить к прототипу
    z_task_src = r"\ZemaxScemesSettings\settings.json"
    # Директория, где будут сохранены результаты
    z_task_dir = r"\Tasks\PrototypeExample"
    task = TaskBuilder(z_file_src, z_task_src)
    task.create_task(z_task_dir)
    task.run_task()

    """
    Создаёт задачу на основе схемы прототипа и списка настроек.
    :return:
    """
    z_file_src = r"D:\Github\ZemaxUtils\ZemaxSchemes\F_07g_04_Blenda_PI_Fin.zmx"
    z_task_src = r"D:\Github\ZemaxUtils\ZemaxSchemesSettings\fields_polychrome_deformed.json"
    z_task_dir = r"D:\Github\ZemaxUtils\Tasks\PolychromeDeformed"
    task = TaskBuilder(z_file_src, z_task_src)
    task.create_task(z_task_dir)
    # task.run_task()
    z_task_src = r"D:\Github\ZemaxUtils\ZemaxSchemesSettings\fields_polychrome_ideal.json"
    z_task_dir = r"D:\Github\ZemaxUtils\Tasks\PolychromeIdeal"
    task = TaskBuilder(z_file_src, z_task_src)
    task.create_task(z_task_dir)
    task.run_task()
    z_task_src = r"D:\Github\ZemaxUtils\ZemaxSchemesSettings\fields_polychrome_real.json"
    z_task_dir = r"D:\Github\ZemaxUtils\Tasks\PolychromeReal"
    task = TaskBuilder(z_file_src, z_task_src)
    task.create_task(z_task_dir)


def build_matrices():
    """
    Создаёт задачу на основе схемы прототипа и списка настроек.
    :return:
    """
    z_file_src = r"E:\Github\ZemaxUtils\ZemaxUtils\ZemaxSchemes\F_07g_04_Blenda_PI_Fin.zmx"
    z_task_src = r"E:\Github\ZemaxUtils\ZemaxUtils\ZemaxSchemesSettings\monochrome.json"
    z_task_dir = r"E:\Github\ZemaxUtils\ZemaxUtils\Tasks\Monochrome"
    task = TaskBuilder(z_file_src, z_task_src)
    task.create_task(z_task_dir)
    # task.run_task()
    z_task_src = r"E:\Github\ZemaxUtils\ZemaxUtils\ZemaxSchemesSettings\polychrome.json"
    z_task_dir = r"E:\Github\ZemaxUtils\ZemaxUtils\Tasks\Polychrome"
    task = TaskBuilder(z_file_src, z_task_src)
    task.create_task(z_task_dir)
    # task.run_task()
    # z_task_src = r"D:\Github\ZemaxUtils\ZemaxSchemesSettings\fields_monochrome_real.json"
    # z_task_dir = r"D:\Github\ZemaxUtils\Tasks\MonochromeReal"
    # task = TaskBuilder(z_file_src, z_task_src)
    # task.create_task(z_task_dir)
    # task.run_task()


def build_and_run_task_from_settings_list():
    """
    Создаёт задачу на основе схемы прототипа и списка настроек.
    :return:
    """
    z_file_src = os.path.join(os.getcwd(), r"ZemaxSchemes/F_07g_04_Blenda_PI_Fin.zmx")
    z_task_src = os.path.join(os.getcwd(), r"TaskSettings/15_01_2025/3_5676_3.json")
    z_task_dir = os.path.join(os.getcwd(), r"TaskSettings/15_01_2025/task-3_5676_3")
    task = TaskBuilder(z_file_src, z_task_src)
    items1 = {220}  # {86, 100, 130, 160, 175, 190, 220}  # 86-220 sec
    task.filter_task(lambda v: int(v.description_short) in items1)
    task.create_task(z_task_dir, task_info=SCHEME_ALL_CALCULATIONS)  # , tasks_ids=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9))

    # task = TaskBuilder(z_file_src, z_task_src)
    # items2 = {4915, 4962, 5007, 5052, 5097, 5152, 5202, 5262, 5307, 5352}  # 4902-5676 sec
    # task.filter_task(lambda v: int(v.description_short) in items2)
    # task.create_task(z_task_dir2, task_info=SCHEME_ALL_CALCULATIONS)  # , tasks_ids=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9))

    # task.run_task()
    # for t in task.tasks:
    #     print(len(t.surf_params))
    #     for i1, i2 in t.surf_remap.items():
    #         if len(t.surf_params) >= i1:
    #             print(f"surf {i2:>3} | {1.0 /  t.surf_params[i1 - 1].curvature:>15.3f} | {t.surf_params[i1 - 1].aperture}")


def collect_and_build_reports(result_dir: str):
    result_files = collect_files_via_dir(result_dir, 'json')
    f_name = os.path.join(os.path.dirname(result_files[0]),
                          '_'.join(os.path.basename(path).split('.')[0] for path in result_files))
    report_total = Report()

    for result in result_files:
        report = Report()
        results = ResultFile()
        results.load(result)
        report.update(results, True)
        report_total.update(results, True)
        report.save('.'.join(result.split('.')[:-1]))
    report_total.save(f_name)

from Geometry import tracing_3d_test, tracing_2d_test


if __name__ == "__main__":
    # tasks = SchemeParams.read("ZemaxSchemesSettings/scheme.json")

    # build_and_run_task_from_settings_list()
    # collect_and_build_reports("26-11-2024/task/Task/Results")
    # UIMainWindow.run()

    # build_and_run_task_from_settings_list()
    collect_and_build_reports(r"TaskSettings/15_01_2025/task-3_5676_3/Task/Results")
    # collect_and_build_reports("19-12-2024/task/Task/Task/Results")
    # tracing_2d_test()
    # tracing_3d_test()
    # # TODO fix aperture issues
    # build_matrices()
    #
    # merge_tasks_from_dir(r"E:\GitHub\ZemaxUtils\ZemaxUtils\ZemaxSchemesSettings\15_03_2024")
    # build_and_run_task_from_settings_list()
    # collect_and_build_reports(r"E:\GitHub\ZemaxUtils\ZemaxUtils\scheme_15_03_2024\Task\Results")
    exit()

    # ЧТО БЫ ПОСЧИТАТЬ, НУЖНО ЗАПУСТИТЬ ЭТОТ КОД
    # build_and_run_task_from_settings_list()
    # exit()
    # А ПОСЛЕ РАСЧТЁТА ЭТОТ
    root_dir = "E:\\Github\\ZemaxUtils\\ZemaxUtils\\"
    rep = Report()
    results = ResultFile()
    results.load(f'{root_dir}\\scheme_7_03_2024\\Task\\Results\\no_description.json')
    rep.update(results, True)
    rep.save('scheme_7_03_2024')
    exit()
    # build_matrices()
    # exit()
    results = ResultFile()

    ##################################################
    root_dir = "E:\\Github\\ZemaxUtils\\ZemaxUtils\\Tasks\\"
    mono_subdir = "Monochrome\\Task\\Results\\"
    poly_subdir = "Polychrome\\Task\\Results\\"
    rep = Report()
    total_rep = Report()
    total_rep.images_count = 10
    total_rep.tables_count = 17
    results.load(f'{root_dir}{mono_subdir}ideal_scheme_monochrome_angle_x_=_-1.074.json')
    rep.update(results, True)
    total_rep.update(results, True)
    rep.save('ideal_scheme_monochrome')

    ##################################################
    rep = Report()
    results.load(f'{root_dir}{mono_subdir}real_scheme_monochrome_angle_x_=_-1.074.json')
    rep.update(results, True)
    total_rep.update(results, True)
    rep.save('real_scheme_monochrome')
    ##################################################
    rep = Report()
    results.load(f'{root_dir}{mono_subdir}deformed_scheme_monochrome_angle_x_=_-1.074.json')
    rep.update(results, True)
    total_rep.update(results, True)
    rep.save('deformed_scheme_monochrome')

    ##################################################
    rep = Report()
    results.load(f'{root_dir}{poly_subdir}ideal_scheme_polychrome_angle_x_=_1.074.json')
    rep.update(results, True)
    total_rep.update(results, True)
    rep.save('ideal_scheme_polychrome')

    ##################################################
    rep = Report()
    results.load(f'{root_dir}{poly_subdir}real_scheme_polychrome_angle_x_=_1.074.json')
    rep.update(results, True)
    total_rep.update(results, True)
    rep.save('real_scheme_polychrome')

    ##################################################
    rep = Report()
    results.load(f'{root_dir}{poly_subdir}deformed_scheme_polychrome_angle_x_=_1.074.json')
    rep.update(results, True)
    total_rep.update(results, True)
    rep.save('deformed_scheme_polychrome')
    total_rep.save('total_report')

    print(results.wavelengths_weights)
    print(results.wavelengths)
