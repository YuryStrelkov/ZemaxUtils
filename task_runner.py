import sys

from TaskBuilder import *
from ZFile.z_file import SCHEME_ALL_CALCULATIONS, COMMON_SCHEME_INFO,\
    SCHEME_SPOT_DIAGRAM, SCHEME_MTF, SCHEME_PSF, INCLUDE_ZMX_PROTO
from typing import Dict, Any, Union, Tuple
from DocxBuilder.report import Report
from ResultBuilder import *


ANSI_GREEN = "\033[32m"
ANSI_RED   = "\033[31m"
ANSI_ESC   = "\033[0m"


def _eval_calc_options(options: Tuple[str, ...]) -> int:
    option = 0
    for opt in options:
        match opt:
            case 'common': option |= COMMON_SCHEME_INFO
            case 'spot': option |= SCHEME_SPOT_DIAGRAM
            case 'mtf': option |= SCHEME_MTF
            case 'psf': option |= SCHEME_PSF
            case 'proto_file': option |= INCLUDE_ZMX_PROTO
    return option


def _collect_files_via_dir(directory: str, ext: str = '*') -> Tuple[str, ...]:
    assert isinstance(directory, str)
    from os.path import isfile, isdir, join
    from os import listdir
    SEPARATOR = '\\'
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


def _build_reports(result_dir: str) -> None:
    import os
    result_files = _collect_files_via_dir(result_dir, 'json')
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


def read_task(file_path: str) -> Dict[str, Any]:
    info = {}
    with open(file_path, 'rt') as input_file:
        data = json.load(input_file)
        for key, args in data.items():
            try:
                match key:
                    case "file_src" | "task_src" | "task_dst": info.update({key: args})
                    case "task_items": info.update({key: tuple(int(v) for v in args)})
                    case "compute_options": info.update({key: _eval_calc_options(tuple(v for v in args))})
            except ValueError as ex:
                print(f"read_task error:[{','.join(str(a)for a in ex.args)}]")
    return info


def eval_task(*, file_src: str = None,
              task_src: str = None,
              task_dst: str = None,
              task_items: Union[None, Tuple[int, ...]] = None,
              compute_options: int = SCHEME_ALL_CALCULATIONS) -> str:
    if not all((file_src, task_src)):
        return f"{ANSI_RED}file_src or task_src is not assigned...{ANSI_ESC}"
    task_dst = task_dst if task_dst else ""
    task = TaskBuilder(file_src, task_src)
    if task_items:
        task.filter_task(lambda v: int(v.description_short) in task_items)
    task.create_task(task_dst, task_info=compute_options)
    task_path = f"{ANSI_GREEN}{os.path.join(task.task_working_directory, 'SCHEMES_LIST.TXT')}{ANSI_ESC}"
    print(f"Now in Zemax press \"{ANSI_GREEN}Macros{ANSI_ESC}\" ->\"{ANSI_GREEN}READ_AND_COMPUTE{ANSI_ESC}\"\nthen use \"{task_path}\" as script argument...")
    task.run_task()
    print(f"Calculations done. Now building \"{ANSI_GREEN}*.docx{ANSI_ESC}\" report files...")
    _build_reports(task.task_results_directory)
    return f"Results may be found within folder \"{ANSI_GREEN}{task.task_working_directory}/Results{ANSI_ESC}\""


def _compute_task(task_location: str) -> None:
    os.system('color')
    try:
        info = read_task(task_location)
        print(eval_task(**info))
    except FileNotFoundError as _:
        print(f"Task file at path \"{ANSI_RED}{task_location}{ANSI_ESC}\" does not exists...")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for location in sys.argv[1:]:
            _compute_task(task_location=location)
    else:
        _compute_task(task_location="task.json")

