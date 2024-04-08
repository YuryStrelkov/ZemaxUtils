from collections import namedtuple
from typing import Any, Tuple
from .z_file import ZFileRaw


class ZFields(namedtuple('ZFileRaw', 'ftyp, xfln, yfln, fwgn, vdxn, vdyn, vcxn, vcyn, vann')):
    _PARAM_NAMES = ('FTYP', 'XFLN', 'YFLN', 'FWGN', 'VDXN', 'VDYN', 'VCXN', 'VCYN', 'VANN')

    _FIELD_TYPES =\
        {0: 'Angle(deg)',
         1: 'Object',
         2: 'Paraxial Image Height',
         3: 'Real Image Height'}

    def __new__(cls, z_file: ZFileRaw):
        params = z_file.header_params
        # assert all(v in ZFields._PARAM_NAMES for v in params.keys())
        ftyp = list(map(int,   params['FTYP'][0].split(' '))) if 'FTYP' in params else [0, 0, 4, 4, 0, 0, 0]
        xfln = list(map(float, params['XFLN'][0].split(' '))) if 'XFLN' in params else \
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        yfln = list(map(float, params['YFLN'][0].split(' '))) if 'YFLN' in params else \
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        fwgn = list(map(float, params['FWGN'][0].split(' '))) if 'FWGN' in params else \
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        vdxn = list(map(float, params['VDXN'][0].split(' '))) if 'VDXN' in params else \
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        vdyn = list(map(float, params['VDYN'][0].split(' '))) if 'VDYN' in params else \
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        vcxn = list(map(float, params['VCXN'][0].split(' '))) if 'VCXN' in params else \
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        vcyn = list(map(float, params['VCYN'][0].split(' '))) if 'VCYN' in params else \
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        vann = list(map(float, params['VANN'][0].split(' '))) if 'VANN' in params else \
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        return super().__new__(cls, ftyp, xfln, yfln, fwgn, vdxn, vdyn, vcxn, vcyn, vann)

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
        return ((('Type', ZFields._FIELD_TYPES[self.ftyp[0]] if self.ftyp[0] in ZFields._FIELD_TYPES else "UNDEF"),
                ('Normalization', 'Rectangular' if self.ftyp[4] == 1 else 'Radial'),
                ('Number Of Fields', self.ftyp[2])), )

    @property
    def n_fields(self) -> int:
        return self.ftyp[2]

    def __str__(self):
        return f"FTYP {' '.join(str(v) for v in self.ftyp)}\n" \
               f"XFLN {' '.join(str(v) for v in self.xfln)}\n" \
               f"YFLN {' '.join(str(v) for v in self.yfln)}\n" \
               f"FWGN {' '.join(str(v) for v in self.fwgn)}\n" \
               f"VDXN {' '.join(str(v) for v in self.vdxn)}\n" \
               f"VDYN {' '.join(str(v) for v in self.vdyn)}\n" \
               f"VCXN {' '.join(str(v) for v in self.vcxn)}\n" \
               f"VCYN {' '.join(str(v) for v in self.vcyn)}\n" \
               f"VANN {' '.join(str(v) for v in self.vann)}\n" \
