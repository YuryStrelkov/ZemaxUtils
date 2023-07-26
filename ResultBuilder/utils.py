from typing import List
import codecs
import os


def _color_code(red: int, green: int, blue: int) -> str:
    return f"#{''.join('{:02X}'.format(max(min(a, 255), 0)) for a in (red, green, blue))}"


def color_map_quad(map_amount: int = 3) -> List[str]:
    """
    Генератор цветовой схемы
    :param map_amount:
    :return:
    """
    if map_amount < 2:
        return [_color_code(0, 0, 255)]
    colors = []
    dx = 1.0 / (map_amount - 1)
    for i in range(map_amount):
        xi = i * dx
        colors.append(_color_code(int(255 * max(1.0 - (2.0 * xi - 1.0) ** 2, 0)),
                                  int(255 * max(1.0 - (2.0 * xi - 2.0) ** 2, 0)),
                                  int(255 * max(1.0 - (2.0 * xi - 0.0) ** 2, 0))))
    return colors


def color_map_lin(map_amount: int = 3) -> List[str]:
    colors = []
    if map_amount < 2:
        return [_color_code(0, 0, 255)]
    dx = 1.0 / (map_amount - 1)
    for i in range(map_amount):
        xi = i * dx
        colors.append(_color_code(int(255 * max(1.0 - 2.0 * xi, 0.0)),
                                  int(255 * (1.0 - abs(2.0 * xi - 1.0))),
                                  int(255 * max(2.0 * xi - 1, 0.0))))
    return colors


def get_encoding(file_name):
    """Detect which UTF codec was used to encode the given bytes.

    The latest JSON standard (:rfc:`8259`) suggests that only UTF-8 is
    accepted. Older documents allowed 8, 16, or 32. 16 and 32 can be big
    or little endian. Some editors or libraries may prepend a BOM.

    :param file_name: Bytes in unknown UTF encoding.
    :return: UTF encoding name
    """
    with open(file_name, "rb") as inp:
        data = inp.read(4)

        head = data[:4]

        if head[:3] == codecs.BOM_UTF8:
            return 'utf-8-sig'

        if b'\x00' not in head:
            return 'utf-8'

        if head in (codecs.BOM_UTF32_BE, codecs.BOM_UTF32_LE):
            return 'utf-32'

        if head[:2] in (codecs.BOM_UTF16_BE, codecs.BOM_UTF16_LE):
            return 'utf-16'

        if len(head) == 4:
            if head[:3] == b'\x00\x00\x00':
                return 'utf-32-be'

            if head[::2] == b'\x00\x00':
                return 'utf-16-be'

            if head[1:] == b'\x00\x00\x00':
                return 'utf-32-le'

            if head[1::2] == b'\x00\x00':
                return 'utf-16-le'

        if len(head) == 2:
            return 'utf-16-be' if head.startswith(b'\x00') else 'utf-16-le'

        return 'utf-8'


def change_encoding(filename,  encoding_to):
    f_name, f_ext = filename.split("/")[-1].split('.')[-2:]
    f_dir = '/'.join(v for v in filename.split("/")[:-1])
    f_dir += "/" if len(f_dir) != 0 else ""
    file_tmp = f_dir + "tmp" + "." + f_ext
    encoding_from = get_encoding(filename)
    if encoding_from == encoding_to:
        return
    with open(filename, 'r', encoding=encoding_from) as fr:
        with open(file_tmp, 'w', encoding=encoding_to) as fw:
            for line in fr:
                fw.write(line[:-1] + '\r')
    os.remove(filename)
    os.rename(file_tmp, filename)
