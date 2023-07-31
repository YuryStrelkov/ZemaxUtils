import os.path

from DocxBuilder.report import Report
from Geometry import *
from ResultBuilder import *
from TaskBuilder import *
from ZFile import COMMON_SCHEME_INFO


def build_polychrome_matrix():
    """
    Создаёт задачу на основе схемы прототипа и списка настроек.
    :return:
    """
    z_file_src = r"D:\Github\ZemaxUtils\ZemaxSchemes\F_07g_04_Blenda_PI_Fin.zmx"
    z_task_src = r"D:\Github\ZemaxUtils\ZemaxScemesSettings\fields_polychrome_deformed.json"
    z_task_dir = r"D:\Github\ZemaxUtils\Tasks\PolychromeDeformed"
    task = TaskBuilder(z_file_src, z_task_src)
    task.create_task(z_task_dir)
    # task.run_task()
    z_task_src = r"D:\Github\ZemaxUtils\ZemaxScemesSettings\fields_polychrome_ideal.json"
    z_task_dir = r"D:\Github\ZemaxUtils\Tasks\PolychromeIdeal"
    task = TaskBuilder(z_file_src, z_task_src)
    task.create_task(z_task_dir)
    # task.run_task()
    z_task_src = r"D:\Github\ZemaxUtils\ZemaxScemesSettings\fields_polychrome_real.json"
    z_task_dir = r"D:\Github\ZemaxUtils\Tasks\PolychromeReal"
    task = TaskBuilder(z_file_src, z_task_src)
    task.create_task(z_task_dir)


def build_matrices():
    """
    Создаёт задачу на основе схемы прототипа и списка настроек.
    :return:
    """
    z_file_src = r"D:\Github\ZemaxUtils\ZemaxSchemes\F_07g_04_Blenda_PI_Fin.zmx"
    z_task_src = r"D:\Github\ZemaxUtils\ZemaxScemesSettings\monochrome.json"
    z_task_dir = r"D:\Github\ZemaxUtils\Tasks\Monochrome"
    task = TaskBuilder(z_file_src, z_task_src)
    task.create_task(z_task_dir)
    # task.run_task()
    z_task_src = r"D:\Github\ZemaxUtils\ZemaxScemesSettings\polychrome.json"
    z_task_dir = r"D:\Github\ZemaxUtils\Tasks\Polychrome"
    task = TaskBuilder(z_file_src, z_task_src)
    task.create_task(z_task_dir)
    # task.run_task()
    # z_task_src = r"D:\Github\ZemaxUtils\ZemaxScemesSettings\fields_monochrome_real.json"
    # z_task_dir = r"D:\Github\ZemaxUtils\Tasks\MonochromeReal"
    # task = TaskBuilder(z_file_src, z_task_src)
    # task.create_task(z_task_dir)
    # task.run_task()


def build_and_run_task_from_settings_list():
    """
    Создаёт задачу на основе схемы прототипа и списка настроек.
    :return:
    """
    z_file_src = r"E:\Github\ZemaxUtils\ZemaxSchemes\F_07g_04_Blenda_PI_Zern_Real.zmx"
    z_task_src = r"E:\Github\ZemaxUtils\ZemaxScemesSettings\schemas.json"
    z_task_dir = r"E:\Github\ZemaxUtils\TestTask"
    task = TaskBuilder(z_file_src, z_task_src)
    task.create_task(z_task_dir, COMMON_SCHEME_INFO)
    task.run_task()


if __name__ == "__main__":
    # build_matrices()
    # exit()
    rep = Report()
    results = ResultFile()
    results.load(r'D:\Github\ZemaxUtils\Tasks\Monochrome\Task\Results\ideal_scheme_monochrome_angle_y_=_-1.074.json')
    rep.update(results)
    results.load(r'D:\Github\ZemaxUtils\Tasks\Monochrome\Task\Results\real_scheme_monochrome_angle_y_=_-1.074.json')
    rep.update(results)
    results.load(r'D:\Github\ZemaxUtils\Tasks\Monochrome\Task\Results\deformed_scheme_monochrome_angle_y_=_-1.074.json')
    rep.update(results)

    results.load(r'D:\Github\ZemaxUtils\Tasks\Polychrome\Task\Results\ideal_scheme_polychrome_angle_y_=_1.074.json')
    rep.update(results)
    results.load(r'D:\Github\ZemaxUtils\Tasks\Polychrome\Task\Results\real_scheme_polychrome_angle_y_=_1.074.json')
    rep.update(results)
    results.load(r'D:\Github\ZemaxUtils\Tasks\Polychrome\Task\Results\deformed_scheme_polychrome_angle_y_=_1.074.json')
    rep.update(results)

    rep.save('report')
    print(results.wavelengths_weights)
    print(results.wavelengths)
    # build_polychrome_matrix()
    # build_monochrome_matrix()
    # build_and_run_task_from_settings_list()

