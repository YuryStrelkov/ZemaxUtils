from typing import Dict, List, Tuple
from collections import namedtuple
import os


class ZFileRaw(namedtuple('ZFileRaw', 'header_params, footer_params, surfaces')):
    """
    Репрезентация zemax файла в виде двух списков:
    1. Список параметров схемы (например, длины волн, поля, свойства окружения)
       header_params - параметры до начала определения поверхностей
       footer_params - параметры после определения всех поверхностей
    2. Список поверхностей
    """
    _Z_FILE_SURF_PAR_INDENT = '  '

    _FOOTER_PARAM = {'BLNK', 'TOL', 'MNUM', 'MOFF'}

    def __new__(cls, file_path: str):
        assert isinstance(file_path, str)
        return ZFileRaw.read(file_path)
    
    def __str__(self):
        return self.write_zmx()
    
    @property
    def is_valid(self) -> bool:
        return len(self.header_params) != 0 and len(self.footer_params) != 0 and len(self.surfaces) != 0

    @classmethod
    def read(cls, zmx_file_path: str):
        assert isinstance(zmx_file_path, str)
        if not os.path.exists(zmx_file_path):
            return super().__new__(cls, dict(), dict(), dict())

        with open(zmx_file_path, mode='r', encoding='utf-16') as _file:
            lines_raw = [line for line in _file]

        if len(lines_raw) == 0:
            return super().__new__(cls, dict(), dict(), dict())

        surfaces_raw      = dict()
        header_params_raw = dict()
        footer_params_raw = dict()
        last_surf          = None

        for line in lines_raw:
            if line.startswith('SURF'):
                line = line.split(' ')
                _id = int(line[1])
                surfaces_raw.update({_id: {}})
                last_surf = surfaces_raw[_id]
                continue
            if line.startswith(ZFileRaw._Z_FILE_SURF_PAR_INDENT):
                line = line[2:]
                beginning_id = line.find(' ')
                beginning = line[0: beginning_id]
                data_line = line[beginning_id + 1:-1].replace('"', '\\"')
                if beginning in last_surf:
                    last_surf[beginning].append(data_line)
                else:
                    last_surf.update({beginning: [data_line]})
                continue
            beginning_id = line.find(' ')
            beginning = line[0: beginning_id]
            data_line = line[beginning_id + 1:-1].replace('"', '\\"')
            if len(surfaces_raw) == 0:
                if beginning in header_params_raw:
                    header_params_raw[beginning].append(data_line)
                else:
                    header_params_raw.update({beginning: [data_line]})
            else:
                if beginning in footer_params_raw:
                    footer_params_raw[beginning].append(data_line)
                else:
                    footer_params_raw.update({beginning: [data_line]})

        return super().__new__(cls, header_params_raw, footer_params_raw, surfaces_raw)

    def write_json(self):
        separator = ',\n\t\t'
        separator_1 = ',\n'

        def _comas(v):
            return f"\"{v}\""

        def _write_param(param: Tuple[str, List[str]]):
            key, values = param
            if len(values) == 1:
                return f"\t\"{key}\" :[{_comas(values[0])}]"
            return f"\t\"{key}\" :\n\t\t[\n\t\t{separator.join(_comas(v) for v in values)}\n\t\t]"

        def _write_surf(surf: Tuple[int, Dict[str, List[str]]]):
            surf_id, surf_params = surf
            return f"\t{{\n" \
                   f"\t\"SURF\": {surf_id},\n{separator_1.join( _write_param(p) for p in surf_params.items())}" \
                   f"\n\t}}"

        return f"{{\n" \
               f"{separator_1.join(_write_param(p) for p in self.params.items() if p[0] not in ZFileRaw._FOOTER_PARAM)},\n" \
               f"\t\"SURFACES\": [\n{separator_1.join(_write_surf(s)for s in self.surfaces.items())}\n\t],\n" \
               f"{separator_1.join(_write_param((p, self.params[p])) for p in ZFileRaw._FOOTER_PARAM if p in self.params)}" \
               f"\n}}"

    def write_zmx(self):
        def _replace(v):
            return v.replace('\\"', '"')

        def _write_param(param: Tuple[str, List[str]]):
            name, args = param
            return '\n'.join(f"{name} {_replace(arg_i)}" for arg_i in args)

        nl_ind = '\n  '

        def _write_surf(surf: Tuple[int, Dict[str, List[str]]]):
            surf_id, surf_params = surf
            return f"SURF {surf_id}\n" \
                   f"  {nl_ind.join(nl_ind.join(f'{key} {_replace(arg)}' for arg in args) for key, args in surf_params.items())}"

        nl = '\n'
        return f"" \
               f"{nl.join(_write_param(p) for p in self.params.items() if p[0] not in ZFileRaw._FOOTER_PARAM)}\n" \
               f"{nl.join(_write_surf(s)for s in self.surfaces.items())}\n" \
               f"{nl.join(_write_param((p, self.params[p])) for p in ZFileRaw._FOOTER_PARAM if p in self.params)}" \
               f""

    def save_zmx(self, zmx_file_path: str):
        with open(zmx_file_path, mode='w', encoding='utf-16') as out:
            print(self.write_zmx(), file=out)

    def save_json(self, zmx_file_path: str):
        with open(zmx_file_path, 'wt') as out:
            print(self.write_json(), file=out)


