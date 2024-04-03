from typing import Tuple
import sys

NUMERICAL_ACCURACY = 1e-9
NUMERICAL_FORMAT_4F = ">10.4f"
NUMERICAL_FORMAT_8F = ">10.8f"
NUMERICAL_MAX_VALUE = 1e12
NUMERICAL_MIN_VALUE = -1e12
PI = 3.141592653589793
TWO_PI = 2.0 * PI
HALF_PI = 0.5 * PI
DEG_TO_RAD = PI / 180.0
RAD_TO_DEG = 180.0 / PI


def assert_version(version_major: int, version_minor: int) -> bool:
    # '''
    #     Сравнение необходимой версии интерпретатора Python с текущей
    # '''
    if sys.version_info.major < version_major:
        return False
    if sys.version_info.minor < version_minor:
        return False
    return True


def pyton_version() -> Tuple[int, int]:
    # '''
    #     Текущая версия интерпретатора Python
    #     @return: [Мажорная версия: int, Минорная версия: int]
    # '''
    return sys.version_info.major, sys.version_info.minor


DATA_CLASS_INSTANCE_ARGS = {'slots': True} if assert_version(3, 10) else {}

