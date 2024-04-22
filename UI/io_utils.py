from os.path import isfile, isdir, join
from typing import Tuple
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
