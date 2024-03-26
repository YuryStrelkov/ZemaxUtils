from collections import namedtuple
from typing import Union, List, Dict

from .z_file import ZFileRaw


class ZWaves(namedtuple('ZFileRaw', 'wavelengths, weights')):

    ZEMAX_MAX_WL_COUNT = 24

    def __new__(cls, z_file: Union[ZFileRaw, None]):
        assert 'FTYP' in z_file.header_params
        assert 'WAVM' in z_file.header_params
        n_wl = min(int(z_file.header_params['FTYP'][0].split(' ')[3]), ZWaves.ZEMAX_MAX_WL_COUNT)
        wls = [tuple(map(float, wl.split(' ')[1:])) for wl in z_file.header_params['WAVM'][0:n_wl]]
        return super().__new__(cls, [v[0] for v in wls], [v[1] for v in wls])

    def n_waves(self) -> int:
        return len(self.wavelengths)

    def __str__(self):
        return ''.join(f'WAVM {index} {wl} {ww}\n' for index, (wl, ww) in enumerate(zip(self.wavelengths, self.weights)))

    def __iter__(self):
        for index, (wl, wlw) in enumerate(zip(self.wavelengths, self.weights)):
            yield "wave_length_n", index
            yield "wave_length", wl
            yield "wave_weight", wlw

    def waves(self) -> List[Dict[str, float]]:
        return [{'wave_length_n': index, "wave_length": wl, 'wave_weight': wlw}
                for index, (wl, wlw) in enumerate(zip(self.wavelengths, self.weights))]