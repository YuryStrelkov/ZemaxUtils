from typing import Union, Tuple, Iterable, Dict, Any
from itertools import zip_longest
from Geometry import Vector2
import dataclasses
import random


def _operation(operation: str,
               iterable1: Iterable[float],
               iterable2: Iterable[float]) -> Tuple[float, ...]:
    match operation:
        case "+":
            return tuple(lhs + rhs for lhs, rhs in zip_longest(iterable1, iterable2, fillvalue=0.0))
        case "-":
            return tuple(lhs - rhs for lhs, rhs in zip_longest(iterable1, iterable2, fillvalue=0.0))
        case "*":
            return tuple(lhs * rhs for lhs, rhs in zip_longest(iterable1, iterable2, fillvalue=0.0))
        case "/":
            return tuple(lhs * rhs for lhs, rhs in zip_longest(iterable1, iterable2, fillvalue=1.0))
        case _:
            raise NotImplementedError(f"Operation \"{operation}\" not implemented...")


@dataclasses.dataclass(frozen=True)
class SurfaceParams:
    EVEN_ASPHERIC_DEFAULT = tuple(0.0 for _ in range(16))
    surf_n: int
    tilt: Vector2
    decenter: Vector2
    aperture: float
    curvature: float
    even_asph: Tuple[float, ...]
    zernike: Tuple[float, ...]

    @classmethod
    def create(cls,
               surf_n: int,
               tilt: Union[Vector2, None],
               decenter: Union[Vector2, None],
               aperture: Union[float, None],
               curvature: Union[float, None],
               even_asph: Union[Tuple[float, ...], None],
               zernike: Union[Tuple[float, ...], None]) -> 'SurfaceParams':
        return cls(surf_n, tilt if tilt else Vector2(),
                   decenter if decenter else Vector2(),
                   aperture, curvature,
                   even_asph if even_asph else (),
                   zernike if zernike else ())

    def __iter__(self):
        yield "surf_n", self.surf_n
        yield "tilt-x", self.tilt.x
        yield "tilt-y", self.tilt.y
        yield "decenter-x", self.decenter.x
        yield "decenter-y", self.decenter.y
        yield "aperture", self.aperture
        yield "curvature", 1.0 / self.curvature
        for index, (a, b) in enumerate(zip_longest(self.even_asph, SurfaceParams.EVEN_ASPHERIC_DEFAULT, fillvalue=0.0)):
            yield f"easph[{index}]", a + b

    def __str__(self) -> str:
        def formatter(_array):
            n = len(_array)
            nl = '\n                          '
            return "".join(
                f"{str(v):<25}{', ' if i != n - 1 else ''}"
                f"{ nl if (i + 1) % 5 == 0 else ''}" for i, v in enumerate(_array))

        params = (f"\t\t\t\"surf_n\"   : {self.surf_n},\n",
                  f"\t\t\t\"tilt\"     : {self.tilt},\n",
                  f"\t\t\t\"decenter\" : {self.decenter},\n",
                  f"\t\t\t\"aperture\" : {self.aperture},\n",
                  f"\t\t\t\"curvature\": {self.curvature},\n",
                  f"\t\t\t\"even_asph\": [\n{formatter(self.even_asph)}],\n",
                  f"\t\t\t\"zernike\"  : [\n{formatter(self.zernike)}]\n")

        return f"\t\t{{\n{''.join(v for v in params)}\t\t}}"

    def __add__(self, other: 'SurfaceParams') -> 'SurfaceParams':
        if isinstance(other, float) or isinstance(other, int):
            return SurfaceParams(self.surf_n, self.tilt,
                                 self.decenter,
                                 self.aperture,
                                 self.curvature,
                                 _operation("+", self.even_asph, (other,)),
                                 _operation("+", self.zernike, (other,)))
        if isinstance(other, SurfaceParams):
            assert self.surf_n == other.surf_n
            return SurfaceParams(self.surf_n, Vector2.min(self.tilt, other.tilt),
                                 Vector2.min(self.decenter, other.decenter),
                                 min(self.aperture, other.aperture),
                                 min(self.curvature, other.curvature),
                                 _operation("+", self.even_asph, other.even_asph),
                                 _operation("+", self.zernike, other.zernike))

    def __sub__(self, other: Union['SurfaceParams', float, int]) -> 'SurfaceParams':
        if isinstance(other, float) or isinstance(other, int):
            return SurfaceParams(self.surf_n, self.tilt,
                                 self.decenter,
                                 self.aperture,
                                 self.curvature,
                                 _operation("-", self.even_asph, (other, )),
                                 _operation("-", self.zernike, (other, )))
        if isinstance(other, SurfaceParams):
            assert self.surf_n == other.surf_n
            return SurfaceParams(self.surf_n, Vector2.min(self.tilt, other.tilt),
                                 Vector2.min(self.decenter, other.decenter),
                                 min(self.aperture, other.aperture),
                                 min(self.curvature, other.curvature),
                                 _operation("-", self.even_asph, other.even_asph),
                                 _operation("-", self.zernike, other.zernike))
        raise ValueError()

    def __mul__(self, other: Union['SurfaceParams', float, int]) -> 'SurfaceParams':
        if isinstance(other, float) or isinstance(other, int):
            return SurfaceParams(self.surf_n, self.tilt,
                                 self.decenter,
                                 self.aperture,
                                 self.curvature,
                                 _operation("*", self.even_asph, (other, )),
                                 _operation("*", self.zernike, (other, )))

        if isinstance(other, SurfaceParams):
            assert self.surf_n == other.surf_n
            return SurfaceParams(self.surf_n, Vector2.min(self.tilt, other.tilt),
                                 Vector2.min(self.decenter, other.decenter),
                                 min(self.aperture, other.aperture),
                                 min(self.curvature, other.curvature),
                                 _operation("*", self.even_asph, other.even_asph),
                                 _operation("*", self.zernike, other.zernike))
        raise ValueError()

    def __rtruediv__(self, other: Union['SurfaceParams', float, int]) -> 'SurfaceParams':
        if isinstance(other, float) or isinstance(other, int):
            return SurfaceParams(self.surf_n, self.tilt,
                                 self.decenter,
                                 self.aperture,
                                 self.curvature,
                                 _operation("/", self.even_asph, (other,)),
                                 _operation("/", self.zernike, (other,)))

        if isinstance(other, SurfaceParams):
            assert self.surf_n == other.surf_n
            return SurfaceParams(self.surf_n, Vector2.min(self.tilt, other.tilt),
                                 Vector2.min(self.decenter, other.decenter),
                                 min(self.aperture, other.aperture),
                                 min(self.curvature, other.curvature),
                                 _operation("/", self.even_asph, other.even_asph),
                                 _operation("/", self.zernike, other.zernike))
        raise ValueError()

    def shuffle(self, scale: float = 0.5) -> 'SurfaceParams':
        return SurfaceParams(self.surf_n,
                             self.tilt,
                             self.decenter,
                             self.aperture,
                             self.curvature,
                             tuple(scale * random.uniform(-abs(a) * 0.5, abs(a) * 0.5) for a in self.even_asph),
                             tuple(scale * random.uniform(-abs(a) * 0.5, abs(a) * 0.5) for a in self.zernike))


def read_surfaces(scheme_node: Dict[str, Any]) -> Tuple[SurfaceParams, ...]:
    if 'scheme' not in scheme_node:
        return ()
    scheme = []
    for node in scheme_node['scheme']:
        try:
            surf_n = int(node['surf_n'])
        except (ValueError, KeyError) as _:
            print(f'surf_n = int(node[\"surf_n\"]) value error...\n'
                  f'Incomplete surface definition :: surf_n does not present in surface')
            continue
        curvature = None
        aperture  = None
        tilt = None
        decenter = None
        zernike = None
        even_asph = None
        try:
            curvature = float(node['curvature'])
        except (ValueError, KeyError) as _:
            print(f'curvature = int(node[\"curvature\"]) value error...')

        try:
            _node = node['tilt']
            tilt = Vector2(float(_node['x']), float(_node['y']))
        except (ValueError, KeyError) as _:
            print(f'tilt = Vector2(float(node[\"x\"]), float(node[\"y\"])) value error... ')

        try:
            _node = node['decenter']
            decenter = Vector2(float(_node['x']), float(_node['y']))
        except (ValueError, KeyError) as _:
            print(f'decenter = Vector2(float(node[\"x\"]), float(node[\"y\"])) value error...')

        try:
            aperture = float(node['aperture'])
        except (ValueError, KeyError) as _:
            print(f'aperture = float(node[\"aperture\"]) value error... ')

        try:
            zernike = tuple(float(v) for v in node['zernike'])
        except(ValueError, KeyError) as _:
            print(f'zernike = [float(v) for v in node[\"poly\"]] value error... ')

        try:
            even_asph = tuple(float(v) for v in node['even_asph'])
        except (ValueError, KeyError) as _:
            print(f'poly = [float(v) for v in node[\"poly\"]] value error... ')
        scheme.append(SurfaceParams(surf_n, tilt, decenter, aperture, curvature, even_asph, zernike))
    return tuple(scheme)
