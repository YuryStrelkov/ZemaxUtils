import os.path
from typing import List, Tuple

from DocxBuilder.report import Report
from ResultBuilder import *
from TaskBuilder import *
from ZFile import COMMON_SCHEME_INFO
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
    z_file_src = r"E:\Github\ZemaxUtils\ZemaxUtils\ZemaxSchemes\F_07g_04_Blenda_PI_Zern_Real.zmx"
    z_task_src = r"E:\GitHub\ZemaxUtils\ZemaxUtils\ZemaxSchemesSettings\combined_params.json"
    z_task_dir = r"E:\Github\ZemaxUtils\ZemaxUtils\scheme_15_03_2024"
    task = TaskBuilder(z_file_src, z_task_src)
    task.create_task(z_task_dir, SCHEME_ALL_CALCULATIONS)
    # task.run_task()


def collect_and_build_reports(result_dir: str):
    result_files = collect_files_via_dir(result_dir, 'json')
    for result in result_files:
        rep = Report()
        results = ResultFile()
        results.load(result)
        rep.update(results, True)
        rep.save('.'.join(result.split('.')[:-1]))


if __name__ == "__main__":
    # TODO fix aperture issues
    build_matrices()
    #
    # merge_tasks_from_dir(r"E:\GitHub\ZemaxUtils\ZemaxUtils\ZemaxSchemesSettings\15_03_2024")
    # build_and_run_task_from_settings_list()
    # collect_and_build_reports(r"E:\GitHub\ZemaxUtils\ZemaxUtils\scheme_15_03_2024\Task\Results")
    exit()


    # ЧТО БЫ ПОСЧИТАТЬ, ЗАПУСТИ ЭТОТ КОД
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
