import dataclasses
from typing import Any, Tuple, List
from .z_file import ZFileRaw


@dataclasses.dataclass(frozen=True)
class ZFields:
    _FIELD_TYPES = \
        {0: 'Angle(deg)',
         1: 'Object',
         2: 'Paraxial Image Height',
         3: 'Real Image Height'}
    _PARAM_NAMES = ('FTYP', 'XFLN', 'YFLN', 'FWGN', 'VDXN', 'VDYN', 'VCXN', 'VCYN', 'VANN')
    _KEYS = ('ftyp', 'xfln', 'yfln', 'fwgn', 'vdxn', 'vdyn', 'vcxn', 'vcyn', 'vann')
    ftyp: List[int]
    xfln: List[float]
    yfln: List[float]
    fwgn: List[float]
    vdxn: List[float]
    vdyn: List[float]
    vcxn: List[float]
    vcyn: List[float]
    vann: List[float]

    @classmethod
    def create(cls, z_file: ZFileRaw):
        params = z_file.header_params
        # assert all(v in ZFields._PARAM_NAMES for v in params.keys())
        ftyp = list(map(int, params['FTYP'][0].split(' '))) if 'FTYP' in params else (0, 0, 4, 4, 0, 0, 0)
        xfln = list(map(float, params['XFLN'][0].split(' '))) if 'XFLN' in params else tuple(0.0 for _ in range(12))
        yfln = list(map(float, params['YFLN'][0].split(' '))) if 'YFLN' in params else tuple(0.0 for _ in range(12))
        fwgn = list(map(float, params['FWGN'][0].split(' '))) if 'FWGN' in params else tuple(0.0 for _ in range(12))
        vdxn = list(map(float, params['VDXN'][0].split(' '))) if 'VDXN' in params else tuple(0.0 for _ in range(12))
        vdyn = list(map(float, params['VDYN'][0].split(' '))) if 'VDYN' in params else tuple(0.0 for _ in range(12))
        vcxn = list(map(float, params['VCXN'][0].split(' '))) if 'VCXN' in params else tuple(0.0 for _ in range(12))
        vcyn = list(map(float, params['VCYN'][0].split(' '))) if 'VCYN' in params else tuple(0.0 for _ in range(12))
        vann = list(map(float, params['VANN'][0].split(' '))) if 'VANN' in params else tuple(0.0 for _ in range(12))
        return cls(ftyp, xfln, yfln, fwgn, vdxn, vdyn, vcxn, vcyn, vann)

    @property
    def fields(self) -> Tuple[Tuple[Tuple[str, float], ...], ...]:
        return tuple((('X-Field', float(a)),
                      ('Y-Field', float(b)),
                      ('Weight', float(c)),
                      ('VDX', float(d)),
                      ('VDY', float(e)),
                      ('VCX', float(f)),
                      ('VCY', float(g)),
                      ('VAN', float(k))) for a, b, c, d, e, f, g, k
                     in zip(self.xfln, self.yfln, self.fwgn, self.vdxn, self.vdyn, self.vcxn, self.vcyn, self.vann))

    @property
    def fields_info(self) -> Tuple[Tuple[Tuple[str, Any], ...], ...]:
        return ((('Type', ZFields._FIELD_TYPES[self.field_type] if self.field_type in ZFields._FIELD_TYPES else "UNDEF"),
                 ('Normalization', 'Rectangular' if self.norm_type == 1 else 'Radial'),
                 ('Number Of Fields', self.n_fields)),)

    @property
    def n_fields(self) -> int:
        return self.ftyp[2]

    @property
    def field_type(self) -> int:
        return self.ftyp[0]

    @property
    def norm_type(self) -> int:
        return self.ftyp[4]

    def __str__(self):
        return f"FTYP {' '.join(str(v) for v in self.ftyp)}\n" \
               f"XFLN {' '.join(str(v) for v in self.xfln)}\n" \
               f"YFLN {' '.join(str(v) for v in self.yfln)}\n" \
               f"FWGN {' '.join(str(v) for v in self.fwgn)}\n" \
               f"VDXN {' '.join(str(v) for v in self.vdxn)}\n" \
               f"VDYN {' '.join(str(v) for v in self.vdyn)}\n" \
               f"VCXN {' '.join(str(v) for v in self.vcxn)}\n" \
               f"VCYN {' '.join(str(v) for v in self.vcyn)}\n" \
               f"VANN {' '.join(str(v) for v in self.vann)}\n"
