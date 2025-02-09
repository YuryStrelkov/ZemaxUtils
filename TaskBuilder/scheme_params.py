from .fields_params import FieldsParams, load_fields_params
from typing import Dict, List, Union, Iterable, Tuple
from .waves_params import Wave, read_waves
from .surface_params import SurfaceParams
from .surface_params import read_surfaces
import json
import os


def _collect_files_via_dir(directory: str, ext: str = '*') -> Tuple[str]:
    assert isinstance(directory, str)
    directories = [directory]
    directory_files = []
    while len(directories) != 0:
        c_dir = directories.pop()
        for file in os.listdir(c_dir):
            c_path = os.path.join(c_dir, file)
            if os.path.isdir(c_path):
                directories.append(c_path)
            if ext == '*':
                directory_files.append(c_path)
                continue
            if os.path.isfile(c_path) and c_path.endswith(ext):
                directory_files.append(c_path)
    separator = '\\'
    return tuple(f"{v.replace(separator, '/')}" for v in directory_files)


class SchemeParams:
    def __init__(self, params: Tuple[SurfaceParams, ...],
                 remap: Union[Dict[int, int], None],
                 desc_short: str = "No description",
                 desc_lng: str = "No description",
                 fields: FieldsParams = None,
                 waves: Tuple[Wave, ...] = None):
        self.description_short = desc_short
        self.description_long = desc_lng
        self.surf_params = params
        self.surf_remap = remap
        self.fields = fields
        self.waves = waves

    def __str__(self):
        def remap_items():
            return "\n" + ",\n".join(f"\t\t{{\"table_index\": {k},"
                                     f" \"scheme_index\":  {v}}}" for k, v in self.surf_remap.items())

        def surf_items():
            return "\n" + ",\n".join(str(k) for k in self.surf_params)

        return f"\t{{\n" \
               f"\t\t\"description_short\": \"{self.description_short}\",\n" \
               f"\t\t\"description_long\": \"{self.description_long}\",\n" \
               f"\t\t\"remap_surfs\": {'[]' if self.surf_remap is None else f'[{remap_items()}]'},\n" \
               f"\t\t\"scheme\": {'[]' if self.surf_params is None else f'[{surf_items()}]'}\n" \
               f"\t}}"

    def __add__(self, other: 'SchemeParams') -> 'SchemeParams':
        assert isinstance(other, SchemeParams)
        return SchemeParams(tuple(s1 + s2 for s1, s2 in zip(self.surf_params, other.surf_params)), self.surf_remap,
                            self.description_short, self.description_long)

    def __sub__(self, other: 'SchemeParams') -> 'SchemeParams':
        assert isinstance(other, SchemeParams)
        return SchemeParams(tuple(s1 - s2 for s1, s2 in zip(self.surf_params, other.surf_params)), self.surf_remap,
                            self.description_short, self.description_long)

    def __mul__(self, other: Union['SchemeParams', float, int]) -> 'SchemeParams':
        if isinstance(other, float) or isinstance(other, int):
            return SchemeParams(tuple(s * other for s in self.surf_params), self.surf_remap,
                                self.description_short, self.description_long)
        assert isinstance(other, SchemeParams)
        return SchemeParams(tuple(s1 * s2 for s1, s2 in zip(self.surf_params, other.surf_params)), self.surf_remap,
                            self.description_short, self.description_long)

    def __rtruediv__(self, other: Union['SchemeParams', float, int]) -> 'SchemeParams':
        if isinstance(other, float) or isinstance(other, int):
            return SchemeParams(tuple(s / other for s in self.surf_params), self.surf_remap,
                                self.description_short, self.description_long)
        assert isinstance(other, SchemeParams)
        return SchemeParams(tuple(s1 / s2 for s1, s2 in zip(self.surf_params, other.surf_params)), self.surf_remap,
                            self.description_short, self.description_long)

    @classmethod
    def _read_scheme(cls, json_node) -> 'SchemeParams':
        surfaces = read_surfaces(json_node)
        waves = read_waves(json_node)
        fields = load_fields_params(json_node)
        remap_surf = None
        description_short = "no description"
        description_long = "no description"
        if "description_long" in json_node:
            description_long = json_node["description_long"]

        if "description_short" in json_node:
            description_short = json_node["description_short"]

        if "remap_surfs" in json_node:
            remap_surf = {}
            for node in json_node["remap_surfs"]:
                try:
                    remap_surf.update({int(node["table_index"]): int(node["scheme_index"])})
                except ValueError as _:
                    continue
                except KeyError as _:
                    continue

        return cls(surfaces, remap_surf, description_short, description_long, fields, waves)

    @staticmethod
    def _read_fields(cls, json_node) -> 'SchemeParams':
        surfaces = read_surfaces(json_node)
        remap_surf = None
        description_short = "no description"
        description_long = "no description"
        if "description_long" in json_node:
            description_long = json_node["description_long"]

        if "description_short" in json_node:
            description_short = json_node["description_short"]

        if "remap_surfs" in json_node:
            remap_surf = {}
            for node in json_node["remap_surfs"]:
                try:
                    remap_surf.update({int(node["table_index"]): int(node["scheme_index"])})
                except (ValueError, KeyError) as _:
                    continue
        return cls(surfaces, remap_surf, description_short, description_long)

    @staticmethod
    def read(file_path: str) -> Tuple['SchemeParams', ...]:
        if not os.path.exists(file_path):
            return ()
        if os.path.isdir(file_path):
            return SchemeParams.read_and_merge(_collect_files_via_dir(file_path, 'json'))
        with open(file_path, "rt") as output_file:
            json_file = json.load(output_file)
            if json_file is None:
                return ()
            if 'schemas' in json_file:
                return tuple(SchemeParams._read_scheme(node) for node in json_file['schemas'])
            if 'scheme' in json_file:
                return SchemeParams._read_scheme(json_file),
            raise RuntimeError(f"Incorrect scheme file definition : {file_path}")

    @staticmethod
    def read_and_merge(file_paths: Iterable[str]) -> Tuple['SchemeParams', ...]:
        params_list = []
        # reading each scheme in list
        for f_path in file_paths:
            try:
                params_list.extend(SchemeParams.read(f_path))
            except RuntimeError as er:
                print(f"SchemeParams::read_and_merge error::\n{er.args}")
        # make unique name for each scheme in list
        name_occurs: Dict[str, int] = {}
        for params in params_list:
            if params.description_short in name_occurs:
                name_occurs[params.description_short] += 1
                params.description_short = '_'.join(str(v) for v in (params.description_short,
                                                                     name_occurs[params.description_short]))
            else:
                name_occurs[params.description_short] = 0
        return tuple(params_list)

    @staticmethod
    def write_params_list(file_name: str, params: Iterable['SchemeParams']):
        with open(file_name, 'wt') as out_file:
            sep = ',\n'
            print(f"{{\n"
                  f"\t\"schemas\":[\n{sep.join(str(p) for p in params)}]"
                  f"\n}}", file=out_file, end='')

    def shuffle(self, scale: float) -> 'SchemeParams':
        return SchemeParams(tuple(s.shuffle(scale) for s in self.surf_params),
                            self.surf_remap,
                            self.description_short,
                            self.description_long)


