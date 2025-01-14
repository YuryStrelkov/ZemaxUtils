from collections import namedtuple
from typing import List, Union
from Geometry import Vector2
import random


class SurfaceParams(namedtuple('SurfaceParams', 'surf_n, tilt, decenter, '
                               'aperture, curvature, even_asph, zernike')):

    __slots__ = ()

    def __new__(cls, surf_n: int, tilt: Union[Vector2, None], decenter: Union[Vector2, None],
                aperture: Union[float, None], curvature: Union[float, None],
                even_asph: Union[List[float], None], zernike: Union[List[float], None]):
        return super().__new__(cls, surf_n, tilt, decenter, aperture,
                               curvature, even_asph, zernike)

    def __iter__(self):
        yield "surf_n", self.surf_n
        yield ("tilt-x", self.tilt.x) if self.tilt else ("tilt-x", 0.0)
        yield ("tilt-y", self.tilt.y) if self.tilt else ("tilt-y", 0.0)
        yield ("decenter-x", self.decenter.x) if self.decenter else ("decenter-x", 0.0)
        yield ("decenter-y", self.decenter.y) if self.decenter else ("decenter-y", 0.0)
        yield ("aperture", self.aperture) if self.aperture else ("aperture", 0.0)
        yield ("curvature", 1.0 / self.curvature) if self.curvature else ("curvature", 0.0)
        if self.even_asph:
            for index, value in enumerate(self.even_asph):
                yield f"easph[{value}]", value
        else:
            for index in range(16):
                yield f"easph[{index}]", 0.0

    def __str__(self) -> str:
        def formatter(_array):
            n = len(_array)
            nl = '\n                          '
            return "".join(
                f"{str(v):<25}{', ' if i != n - 1 else ''}"
                f"{ nl if (i + 1) % 5 == 0 else ''}" for i, v in enumerate(_array))

        params = [f"\t\t\t\"surf_n\"   : {self.surf_n},\n",
                  f"\t\t\t\"tilt\"     : {self.tilt},\n" if self.tilt is not None else "",
                  f"\t\t\t\"decenter\" : {self.decenter},\n" if self.decenter is not None else "",
                  f"\t\t\t\"aperture\" : {self.aperture},\n" if self.aperture is not None else "",
                  f"\t\t\t\"curvature\": {self.curvature},\n" if self.curvature is not None else "",
                  f"\t\t\t\"even_asph\": ["
                  f"{'' if self.even_asph is None else formatter(self.even_asph)}],\n",
                  f"\t\t\t\"zernike\"  : ["
                  f"{'' if self.zernike is None else formatter(self.zernike)}]\n"]

        return f"\t\t{{\n{''.join(v for v in params)}\t\t}}"

    def __add__(self, other: 'SurfaceParams') -> 'SurfaceParams':
        assert isinstance(other, SurfaceParams)
        assert self.surf_n == other.surf_n
        return SurfaceParams(self.surf_n, Vector2.min(self.tilt, other.tilt),
                             min(self.decenter, other.decenter),
                             min(self.aperture, other.aperture),
                             min(self.curvature, other.curvature),
                             self.even_asph if other.even_asph is None else other.even_asph if self.even_asph is None
                             else [a + b for a, b in zip(self.even_asph, other.even_asph)],
                             self.zernike if other.zernike is None else other.zernike if self.zernike is None
                             else [a + b for a, b in zip(self.zernike, other.zernike)])

    def __sub__(self, other: 'SurfaceParams') -> 'SurfaceParams':
        assert isinstance(other, SurfaceParams)
        assert self.surf_n == other.surf_n
        return SurfaceParams(self.surf_n, Vector2.min(self.tilt, other.tilt),
                             min(self.decenter, other.decenter),
                             min(self.aperture, other.aperture),
                             min(self.curvature, other.curvature),
                             self.even_asph if other.even_asph is None else other.even_asph if self.even_asph is None
                             else [a - b for a, b in zip(self.even_asph, other.even_asph)],
                             self.zernike if other.zernike is None else other.zernike if self.zernike is None
                             else [a - b for a, b in zip(self.zernike, other.zernike)])

    def __mul__(self, other: Union['SurfaceParams', float, int]) -> 'SurfaceParams':
        if isinstance(other, float) or isinstance(other, int):
            return SurfaceParams(self.surf_n, self.tilt,
                                 self.decenter,
                                 self.aperture,
                                 self.curvature,
                                 self.even_asph if self.even_asph is None else [a * other for a in self.even_asph],
                                 self.even_asph if self.zernike is None else [a * other for a in self.zernike])

        if isinstance(other, SurfaceParams):
            assert self.surf_n == other.surf_n
            return SurfaceParams(self.surf_n, Vector2.min(self.tilt, other.tilt),
                                 min(self.decenter, other.decenter),
                                 min(self.aperture, other.aperture),
                                 min(self.curvature, other.curvature),
                                 self.even_asph if other.even_asph is None else other.even_asph
                                 if self.even_asph is None
                                 else [a * b for a, b in zip(self.even_asph, other.even_asph)],
                                 self.zernike if other.zernike is None else other.zernike
                                 if self.zernike is None
                                 else [a * b for a, b in zip(self.zernike, other.zernike)])
        raise ValueError()

    def __rtruediv__(self, other: Union['SurfaceParams', float, int]) -> 'SurfaceParams':
        if isinstance(other, float) or isinstance(other, int):
            return SurfaceParams(self.surf_n, self.tilt,
                                 self.decenter,
                                 self.aperture,
                                 self.curvature,
                                 self.even_asph if self.even_asph is None else [a / other for a in self.even_asph],
                                 self.even_asph if self.zernike is None else [a / other for a in self.zernike])

        if isinstance(other, SurfaceParams):
            assert self.surf_n == other.surf_n
            return SurfaceParams(self.surf_n, Vector2.min(self.tilt, other.tilt),
                                 min(self.decenter, other.decenter),
                                 min(self.aperture, other.aperture),
                                 min(self.curvature, other.curvature),
                                 self.even_asph if other.even_asph is None else other.even_asph
                                 if self.even_asph is None
                                 else [a / b for a, b in zip(self.even_asph, other.even_asph)],
                                 self.zernike if other.zernike is None else other.zernike
                                 if self.zernike is None
                                 else [a / b for a, b in zip(self.zernike, other.zernike)])
        raise ValueError()

    def shuffle(self, scale: float = 0.5) -> 'SurfaceParams':
        return SurfaceParams(self.surf_n,
                             self.tilt,
                             self.decenter,
                             self.aperture,
                             self.curvature,
                             [] if self.even_asph is None else
                             [scale * random.uniform(-abs(a) * 0.5, abs(a) * 0.5) for a in self.even_asph],
                             [] if self.zernike is None else
                             [scale * random.uniform(-abs(a) * 0.5, abs(a) * 0.5) for a in self.zernike])


def read_surfaces(scheme_node) -> List[SurfaceParams]:
    scheme = []
    if 'scheme' not in scheme_node:
        return scheme
    for node in scheme_node['scheme']:
        if 'surf_n' not in node:
            raise RuntimeError("Incomplete surface definition :: surf_n does not present in surface")
        try:
            surf_n = int(node['surf_n'])
        except ValueError as _:
            print(f'surf_n = int(node[\"surf_n\"]) value error... ')
            continue
        except KeyError as _:
            print(f'surf_n = int(node[\"surf_n\"]) parse error... ')
            continue
        curvature = None
        aperture  = None
        tilt = None
        decenter = None
        zernike = None
        even_asph = None
        if 'curvature' in node:
            try:
                curvature = float(node['curvature'])
            except ValueError as err:
                print(f'curvature = int(node[\"curvature\"]) value error...')
        if 'tilt' in node:
            try:
                _node = node['tilt']
                tilt = Vector2(float(_node['x']), float(_node['y']))
            except ValueError as err:
                _node = node['tilt']
                print(f'tilt = Vector2(float(node[\"x\"]), float(node[\"y\"])) value error... ')
        if 'decenter' in node:
            try:
                _node = node['decenter']
                decenter = Vector2(float(_node['x']), float(_node['y']))
            except ValueError as err:
                print(f'decenter = Vector2(float(node[\"x\"]), float(node[\"y\"])) value error...')
        if 'aperture' in node:
            try:
                aperture = float(node['aperture'])
            except ValueError as err:
                print(f'aperture = float(node[\"aperture\"]) value error... ')
        if 'zernike' in node:
            try:
                zernike = [float(v) for v in node['zernike']]
            except ValueError as err:
                print(f'zernike = [float(v) for v in node[\"poly\"]] value error... ')

        if 'even_asph' in node:
            try:
                even_asph = [float(v) for v in node['even_asph']]
            except ValueError as err:
                print(f'poly = [float(v) for v in node[\"poly\"]] value error... ')

        scheme.append(SurfaceParams(surf_n, tilt, decenter, aperture, curvature, even_asph, zernike))
    return scheme
