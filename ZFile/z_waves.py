from ZFile.z_file_raw import ZFileRaw
from collections import namedtuple


class ZWaves(namedtuple('ZFileRaw', 'wavelengths, weights')):

    ZEMAX_MAX_WL_COUNT = 24

    def __new__(cls, z_file: ZFileRaw):
        assert 'FTYP' in z_file.header_params
        assert 'WAVM' in z_file.header_params
        n_wl = min(int(z_file.header_params['FTYP'][0].split(' ')[3]), ZWaves.ZEMAX_MAX_WL_COUNT)
        wls = [tuple(map(float, wl.split(' ')[1:])) for wl in z_file.header_params['WAVM'][0:n_wl]]

        return super().__new__(cls, [v[0] for v in wls], [v[1] for v in wls])

    def n_waves(self) -> int:
        return len(self.wavelengths)

    def __str__(self):
        return ''.join(f'WAVM {index} {wl} {ww}\n' for index, (wl, ww) in enumerate(zip(self.wavelengths, self.weights)))


