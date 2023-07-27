from .surface_params import SurfaceParams
from .surface_params import read_surfaces
from .fields_params import FieldsParams, load_fields_params
from typing import Dict, List, Union
from .waves_params import Wave, read_waves
import json
import os


class SchemeParams:

    def __init__(self, params: List[SurfaceParams], remap: Union[Dict[int, int], None],
                 desc_short: str = "No description", desc_lng: str = "No description",
                 fields: FieldsParams = None, waves: List[Wave] = None):
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

    def __add__(self, other):
        assert isinstance(other, SchemeParams)
        return SchemeParams([s1 + s2 for s1, s2 in zip(self.surf_params, other.surf_params)], self.surf_remap,
                            self.description_short, self.description_long)

    def __sub__(self, other):
        assert isinstance(other, SchemeParams)
        return SchemeParams([s1 - s2 for s1, s2 in zip(self.surf_params, other.surf_params)], self.surf_remap,
                            self.description_short, self.description_long)

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return SchemeParams([s * other for s in self.surf_params], self.surf_remap,
                                self.description_short, self.description_long)
        assert isinstance(other, SchemeParams)
        return SchemeParams([s1 * s2 for s1, s2 in zip(self.surf_params, other.surf_params)], self.surf_remap,
                            self.description_short, self.description_long)

    def __rtruediv__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return SchemeParams([s / other for s in self.surf_params], self.surf_remap,
                                self.description_short, self.description_long)
        assert isinstance(other, SchemeParams)
        return SchemeParams([s1 / s2 for s1, s2 in zip(self.surf_params, other.surf_params)], self.surf_remap,
                            self.description_short, self.description_long)

    @classmethod
    def _read_scheme(cls, json_node):
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
    def _read_fields(cls, json_node):
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
                except ValueError as _:
                    continue
                except KeyError as _:
                    continue
        return cls(surfaces, remap_surf, description_short, description_long)

    @staticmethod
    def read(file_path: str):
        if not os.path.exists(file_path):
            return []
        with open(file_path, "rt") as output_file:
            json_file = json.load(output_file)
            if json_file is None:
                return []
            if 'schemas' in json_file:
                return [SchemeParams._read_scheme(node) for node in json_file['schemas']]
            if 'scheme' in json_file:
                return [SchemeParams._read_scheme(json_file)]
            raise RuntimeError(f"Incorrect scheme file definition : {file_path}")

    def shuffle(self, scale: float):
        return SchemeParams([s.shuffle(scale) for s in self.surf_params], self.surf_remap,
                            self.description_short, self.description_long)


