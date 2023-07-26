from TaskBuilder.task_builder import TaskBuilder
from ZFile import COMMON_SCHEME_INFO


def build_and_run_task_from_settings_list():
    """
    Создаёт задачу на основе схемы прототипа и списка настроек.
    :return:
    """
    z_file_src = r"E:\Aist_T\ZemaxExec\ZemaxSchemes\F_07g_04_Blenda_PI_Zern_Real.zmx"
    z_task_src = r"E:\Aist_T\ZemaxExec\ZemaxScemesSettings\schemas.json"
    z_task_dir = r"E:\Aist_T\ZemaxExec\TestTask"
    task = TaskBuilder(z_file_src, z_task_src)
    task.create_task(z_task_dir, COMMON_SCHEME_INFO)
    task.run_task()


if __name__ == "__main__":
    build_and_run_task_from_settings_list()

