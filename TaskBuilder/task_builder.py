import json
from typing import List, Tuple, Union, Dict, Generator, Callable, Iterable

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
INCLUDE_ZMX_PROTO = 16

DEFAULT_TASK_INFO: int = COMMON_SCHEME_INFO | SCHEME_SPOT_DIAGRAM | SCHEME_MTF | SCHEME_PSF | INCLUDE_ZMX_PROTO

# PRETENDERS_FOR_ZEMAX = (r"Zemax",
#                         r"Program Files\Zemax",
#                         r"Program Files(x86)\Zemax")
#
# PRETENDERS_FOR_SCRIPT = (r"Zemax\Macros", r"Program Files\Zemax\Macros",
#                          r"Program Files(x86)\Zemax\Macros",
#                          r"Users\User\Documents\Zemax\Macros")
_FILES_EXTENSIONS = ("json", "txt", "zmx", "ses", "TXT", "ZMX", "SES")


def _replace_file(orig_src: str, test_src: str):
    if not os.path.isfile(orig_src) or not os.path.isfile(test_src):
        return
    try:
        with open(orig_src, 'rt', encoding='utf-8') as orig_file:
            with open(test_src, 'rt', encoding='utf-8') as test_file:
                equals = any(line1 != line2 for line1, line2 in zip(orig_file, test_file))
    except UnicodeDecodeError as _:
        print(f"decoding error while comparing files \"{orig_src}\" and \"{test_src}\"")
        return 
    if equals:
        print(f"script      : {test_src}\nis equal to : {orig_src}\n")
    else:
        shutil.copyfile(orig_src, test_src)
        print(f"current script  : {test_src}\nwere updated by : {orig_src}")


def _get_zemax_exe():
    available_discs = (f'{d}:' for d in string.ascii_uppercase if os.path.exists(f'{d}:'))
    for disk in available_discs:
        for root, dirs, files in os.walk(disk):
            for file in files:
                if file == "zemax.exe":
                    return file, os.path.join(root, file)
    return "", ""


def _get_zemax_scripts():
    available_discs = (f'{d}:' for d in string.ascii_uppercase if os.path.exists(f'{d}:'))

    def _get_dir():
        for disk in available_discs:
            for root, dirs, files in os.walk(disk):
                if "Macros" not in root:
                    continue
                for file in files:
                    if "ZPL" in file or "zpl" in file:
                        return root
        return ""
    folder = _get_dir()
    if folder:
        return {(n, os.path.join(folder, n)) for n in os.listdir(folder)}
    else:
        return {}


def _update_scripts(zmx_scripts_dst: Dict[str, str]):
    abs_path = os.path.dirname(__file__)
    zpl_scripts_src = {}  # (file name, absolute file path)
    for root, dirs, files in os.walk(abs_path):
        for file in files:
            if file.endswith(("zpl", "ZPL")):
                zpl_scripts_src.update({file: os.path.join(root, file)})
    for src, dst in zip(zpl_scripts_src.values(), zmx_scripts_dst.values()):
        _replace_file(src, dst)


def _load_settings():
    file_location = os.path.join(os.path.dirname(__file__), "zSettings.json")
    try:
        with open(file_location, "rt") as input_file:
            raw_json = json.load(input_file)
            zemax_exe = raw_json["zemaxExe"]
            zemax_scripts = {k: v for k, v in raw_json["zemaxScripts"]}
            return zemax_exe, zemax_scripts
    except KeyError as ex:
        os.remove(file_location)
        print(ex)
    except FileNotFoundError as ex:
        print(ex)
    return None, None


def _save_settings(zemax_exe: str, zemax_scripts: Dict[str, str] ):
    file_location = os.path.join(os.path.dirname(__file__), "zSettings.json")

    def _str_2_dict(scripts: Dict[str, str]) -> str:
        return ',\n'.join(f'\t\t[\"{k}\", \"{v}\"]'.replace('\\', '/') for k, v in scripts)

    with open(file_location, "wt") as input_file:
        zemax_exe = zemax_exe.replace('\\', '/')
        print(f"{{\n"
              f"\t\"zemaxExe\": \"{zemax_exe}\",\n"
              f"\t\"zemaxScripts\": [\n{_str_2_dict(zemax_scripts)}\n\t]"
              f"\n}}", file=input_file)


def _search_zemax_dirs() -> Tuple[str, Dict[str, str]]:
    zemax_exe, zemax_scripts = _load_settings()
    if all((zemax_exe, zemax_scripts)):
        return zemax_exe, zemax_scripts
    zemax_exe, absolute_zemax_exe = _get_zemax_exe()
    zemax_scripts = _get_zemax_scripts()
    _save_settings(absolute_zemax_exe, zemax_scripts)
    return os.path.join(zemax_exe, absolute_zemax_exe), zemax_scripts


class TaskBuilder:
    def __init__(self, z_file_proto_src: str = None, task_file_scr: str = None):
        self._z_file_proto_src: str = ""
        self._task_file_src: str = ""
        self._task_working_directory: str = ""
        self._task_results_directory: str = ""
        self._z_file: Union[ZFile, None] = None
        self._task_args: Union[Dict[int, SchemeParams], None] = None
        if z_file_proto_src:
            self.z_file_proto_src = z_file_proto_src
        if task_file_scr:
            self.task_file_src = task_file_scr

    @property
    def has_tasks(self) -> bool:
        return bool(self._task_args)

    @property
    def has_zemax_file(self) -> bool:
        return bool(self._z_file)

    @property
    def task_working_directory(self) -> str:
        return self._task_working_directory

    @property
    def task_results_directory(self) -> str:
        return self._task_results_directory

    @property
    def tasks(self) -> Generator[SchemeParams, None, None]:
        if self.has_tasks:
            for item in self._task_args.values():
                yield item

    @property
    def z_file(self) -> ZFile:
        return self._z_file

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
        return self._task_file_src

    @task_file_src.setter
    def task_file_src(self, value: Union[str, List[str]]) -> None:
        if isinstance(value, str):
            self._task_file_src = value
            self._task_args = {i: v for i, v in enumerate(SchemeParams.read(self._task_file_src))}
        elif isinstance(value, List):
            self._task_file_src = value
            self._task_args = {i: v for i, v in enumerate(SchemeParams.read_and_merge(self._task_file_src))}
        else:
            raise ValueError("task file src should be list or single string")

    @property
    def is_valid(self) -> bool:
        return all((self._z_file_proto_src, self._task_file_src, self._z_file, self._task_args))

    def remove_task_by_id(self, task_id: int) -> bool:
        if task_id in self._task_args:
            del self._task_args[task_id]
            return True
        return False

    def filter_task(self, predicate: Callable[[SchemeParams], bool]) -> None:
        self._task_args = {i: v for i, v in enumerate(self._task_args.values()) if predicate(v)}

    def _init_paths(self, task_dir: str) -> None:
        if task_dir is None:
            raw_path = '\\'.join(v for v in self.z_file_proto_src.split("\\")[:-1])
            self._task_working_directory = os.path.join(raw_path, "Task")
            self._task_results_directory = os.path.join(raw_path, r"Task\Results")
        else:
            self._task_working_directory = os.path.join(task_dir, "Task")
            self._task_results_directory = os.path.join(task_dir, r"Task\Results")
        if not os.path.exists(task_dir):
            os.mkdir(task_dir)

    @staticmethod
    def _clear_dir(dir_path: str):
        for file in os.listdir(dir_path):
            if file.endswith(_FILES_EXTENSIONS):
                os.remove(os.path.join(dir_path, file))

    @staticmethod
    def _create_dir(dir_path: str):
        if os.path.exists(dir_path):
            return
        os.mkdir(dir_path)

    @staticmethod
    def _create_valid_file_name(file_name: str):
        file_name = file_name.split("\\")[-1]
        return ('.'.join(v for v in file_name.split('.')[:-1])).replace(" ", "_").replace(",", "")

    def _create_result_json(self, task: Union[SchemeParams, str]) -> str:
        if isinstance(task, str):
            self._z_file.save(os.path.join(self.task_working_directory, f"{task}.zmx"))
            name_of_file = TaskBuilder._create_valid_file_name(f"{task}.zmx")
            with open(os.path.join(self.task_results_directory, f"{name_of_file}.json"), "wt"):
                ...
            return f"{task}.zmx"
        if isinstance(task, SchemeParams):
            self._z_file.apply_settings(task)
            self._z_file.save(os.path.join(self.task_working_directory,  f"{task.description_short}.zmx"))
            name_of_file = TaskBuilder._create_valid_file_name(f"{task.description_short}.zmx")
            with open(os.path.join(self.task_results_directory, f"{name_of_file}.json"), "wt"):
                ...
            return f"{task.description_short}.zmx"

    def _init_tasks_dir(self) -> None:
        TaskBuilder._create_dir(self.task_working_directory)
        TaskBuilder._clear_dir(self.task_working_directory)

    def _init_results_dir(self) -> None:
        TaskBuilder._create_dir(self.task_results_directory)
        TaskBuilder._clear_dir(self.task_results_directory)

    def _crate_task_settings_file(self, task_info: int, task_files: Iterable[str]):
        with open(os.path.join(self.task_working_directory, "SCHEMES_LIST.TXT"), "wt") as task_list:
            #  print(r"call script \"READ_AND_COMPUTE.ZMX\"", file=task_list)
            #  print(f"with arg {self._task_working_directory}SCHEMES_LIST.TXT", file=task_list)
            print(f'root: {self.task_working_directory}\\', file=task_list)
            print(f'compute_settings: {" ".join("1" if task_info & v == v else "0" for v in (1, 2, 4, 8))}',
                  file=task_list)
            print('\n'.join(f"file: {v}" for v in task_files), file=task_list)

    def create_task(self, task_directory: str = None, *,
                    task_info: int = DEFAULT_TASK_INFO,
                    tasks_ids: Tuple[int, ...] = None) -> bool:
        if not self.is_valid:
            return False
        self._init_paths(task_directory)
        self._init_tasks_dir()
        self._init_results_dir()
        task_files = []
        if task_info & INCLUDE_ZMX_PROTO == INCLUDE_ZMX_PROTO:
            task_files.append(self._create_result_json('original_zemax_file'))
        for task in (tuple(self._task_args[t] for t in tasks_ids) if tasks_ids else self._task_args.values()):
            task_files.append(self._create_result_json(task))  ##f"{task.description_short}.zmx"))
        self._crate_task_settings_file(task_info, task_files)
        return True

    def run_task(self) -> bool:
        # TODO start up zemax.exe
        if not self.is_valid:
            return False
        zmx_exe, zmx_scripts = _search_zemax_dirs()
        state = all(map(bool, (zmx_exe, zmx_scripts)))
        if state:
            _update_scripts(zmx_scripts)
            subprocess.run([zmx_exe, self._z_file_proto_src])
        return state

# root: D:\Github\ZemaxUtils\Tasks\MonochromeDeformed\Task\
# compute_settings: 1 0 0 0
# file: zemax_proto_file.zmx
# file: deformed_scheme_monochrome_angle_y_=_1.07.zmx
# file: deformed_scheme_monochrome_angle_y_=_1.072.zmx
# file: deformed_scheme_monochrome_angle_y_=_1.074.zmx
# file: deformed_scheme_monochrome_angle_y_=_1.076.zmx
# file: deformed_scheme_monochrome_angle_y_=_1.078.zmx
