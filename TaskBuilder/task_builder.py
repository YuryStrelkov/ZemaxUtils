from typing import List, Tuple, Union
from .scheme_params import SchemeParams
from ZFile import ZFile
from os import path
import subprocess
import string
import shutil
import os


COMMON_SCHEME_INFO = 1
SCHEME_SPOT_DIAGRAM = 2
SCHEME_MTF = 4
SCHEME_PSF = 8

PRETENDERS_FOR_ZEMAX = ("\\Zemax\\",
                        "\\Program Files\\Zemax\\",
                        "\\Program Files(x86)\\Zemax\\")

PRETENDERS_FOR_SCRIPT = ("\\Zemax\\Macros\\", "\\Program Files\\Zemax\\Macros\\",
                         "\\Program Files(x86)\\Zemax\\Macros\\",
                         "\\Users\\User\\Documents\\Zemax\\Macros\\")


def _replace_file(orig_src: str, test_src: str):
    if not os.path.isfile(orig_src):
        return
    if not os.path.isfile(test_src):
        return
    equals = True
    with open(orig_src, 'rt', encoding='utf-8') as orig_file:
        with open(test_src, 'rt', encoding='utf-8') as test_file:
            for line1, line2 in zip(orig_file, test_file):
                if line1 == line2:
                    continue
                equals = False
                break
    if equals:
        print(f"script      : {test_src}\nis equal to : {orig_src}\n")
        return
    shutil.copyfile(orig_src, test_src)
    print(f"current script  : {test_src}\nwere updated by : {orig_src}")


def _update_scripts(zmx_scripts: str):
    _replace_file(os.path.abspath('TaskBuilder\\ZPLScripts\\READ_AND_COMPUTE.ZPL'), zmx_scripts + "READ_AND_COMPUTE.ZPL")
    subdir = "\\COMPUTE_UTILS\\"
    for f in os.listdir(path='TaskBuilder\\ZPLScripts' + subdir):
        _replace_file(os.path.abspath('TaskBuilder\\ZPLScripts' + subdir + f), zmx_scripts + subdir + f)


def _search_zemax_dirs() -> Tuple[str, str]:
    available_drives = ['%s:' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]
    zemax_exe = ""
    zemax_scripts = ""
    for disk in available_drives:
        for zmx in PRETENDERS_FOR_ZEMAX:
            path_to_zemax = disk + zmx + "zemax.exe"
            if os.path.isfile(path_to_zemax):
                zemax_exe = path_to_zemax
                break

    for disk in available_drives:
        for zmx in PRETENDERS_FOR_SCRIPT:
            path_to_zemax = disk + zmx
            if os.path.isdir(path_to_zemax):
                zemax_scripts = path_to_zemax
                break

    return zemax_exe, zemax_scripts


class TaskBuilder:
    def __init__(self, z_file_proto_src: str = None, task_file_scr: str = None):
        self._z_file_proto_src: str = ""
        self._task_file_src: str = ""
        self._z_file: Union[ZFile, None] = None
        self._task_args: Union[List[SchemeParams], None] = None
        self._task_working_directory: str = ""
        self._task_results_directory: str = ""
        self.z_file_proto_src = z_file_proto_src
        self.task_file_src = task_file_scr

    def _combine_task(self, other):
        if not isinstance(other, TaskBuilder):
            return


    @property
    def z_file_proto_src(self) -> str:
        return self._z_file_proto_src

    @z_file_proto_src.setter
    def z_file_proto_src(self, value: str) -> None:
        if not path.exists(value):
            return
        if value == self._z_file_proto_src:
            return
        self._z_file_proto_src = value
        self._z_file = ZFile()
        self._z_file.load(self._z_file_proto_src)

    @property
    def task_file_src(self) -> str:
        return self._z_file_proto_src

    @task_file_src.setter
    def task_file_src(self, value: str) -> None:
        if not path.exists(value):
            return
        if value == self._task_file_src:
            return
        self._task_file_src = value
        self._task_args = SchemeParams.read(self._task_file_src)

    @property
    def is_valid(self) -> bool:
        if self._z_file_proto_src == "":
            return False
        if self._task_file_src == "":
            return False
        if self._z_file is None:
            return False
        if self._task_args is None:
            return False
        return True

    def create_task(self, task_directory: str = None,
                    task_info: int = COMMON_SCHEME_INFO | SCHEME_SPOT_DIAGRAM | SCHEME_MTF | SCHEME_PSF) -> bool:
        if not self.is_valid:
            return False
        if task_directory is None:
            raw_path = '\\'.join(v for v in self.z_file_proto_src.split("\\")[:-1])
            self._task_working_directory = raw_path + "\\Task\\"
            self._task_results_directory = raw_path + "\\Task\\Results\\"
        else:
            raw_path = task_directory if task_directory.endswith("\\") else \
                '\\'.join(v for v in task_directory.split("\\"))
            self._task_working_directory = raw_path + "\\Task\\"
            self._task_results_directory = raw_path + "\\Task\\Results\\"

        if not os.path.exists(task_directory):
            os.mkdir(task_directory)

        if not os.path.exists(self._task_working_directory):
            os.mkdir(self._task_working_directory)
        else:
            for file in os.listdir(self._task_working_directory):
                if file.endswith(("json", "txt", "zmx", "ses", "TXT", "ZMX", "SES")):
                    os.remove(self._task_working_directory + file)

        if not os.path.exists(self._task_results_directory):
            os.mkdir(self._task_results_directory)
        else:
            for file in os.listdir(self._task_results_directory):
                if file.endswith(("json", "txt", "zmx", "ses", "TXT", "ZMX", "SES")):
                    os.remove(self._task_results_directory + file)

        task_files = [self._task_working_directory + "zemax_proto_file.zmx"]
        self._z_file.save(task_files[-1])
        with open(self._task_results_directory + "zemax_proto_file.json", "wt"):
            pass

        for task in self._task_args:
            task_files.append(self._task_working_directory + task.description_short.replace(" ", "_") + ".zmx")
            self._z_file.apply_settings(task)
            self._z_file.save(task_files[-1])
            with open(self._task_results_directory + task.description_short.replace(" ", "_") + ".json", "wt"):
                pass
        with open(self._task_working_directory + "SCHEMES_LIST.TXT", "wt") as task_list:
            print('\n'.join(v + " " + " ".join("1" if task_info & v == v
                                               else "0" for v in (1, 2, 4, 8)) for v in task_files), file=task_list)

        return True

    def run_task(self) -> bool:
        # TODO start up zemax.exe
        if not self.is_valid:
            return False
        zmx_exe, zmx_scripts = _search_zemax_dirs()
        if zmx_exe == "" or zmx_scripts == "":
            return False
        _update_scripts(zmx_scripts)
        subprocess.run([zmx_exe, self._z_file_proto_src])
        return True

