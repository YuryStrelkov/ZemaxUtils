from typing import List, Dict, Tuple, Union
from Geometry import Vector2, Vector3
from collections import namedtuple
import numpy as np
import math

_N_X = "N_X"
_N_Y = "N_Y"
_PX_MIN = "PX_MIN"
_PX_MAX = "PX_MAX"
_PY_MIN = "PY_MIN"
_PY_MAX = "PY_MAX"
_AX_MIN = "AX_MIN"
_AX_MAX = "AX_MAX"
_AY_MIN = "AY_MIN"
_AY_MAX = "AY_MAX"
_N_ANGLES_X = "N_ANGLES_X"
_N_ANGLES_Y = "N_ANGLES_Y"
_WAVE_ID = "WAVE_ID"
_FIELD_ID = "FIELD_ID"
_VIG_PER_POS = "VIG_PER_POS"
_PX = "PX"
_PY = "PY"
_AX = "AX"
_AY = "AY"
_X = "X"
_Y = "Y"
_Z = "Z"
_RAY_VIGNETTING = "RAY_VIGNETTING"
_RAY_POL_FIELD = "RAY_POL_FIELD"
_INTENSITY = "INTENSITY"
_E_REAL = "E_REAL"
_E_IMAG = "E_IMAG"
_S_REFLECTION = "S_REFLECTION"
_S_TRANSMISSION = "S_TRANSMISSION"
_P_REFLECTION = "P_REFLECTION"
_P_TRANSMISSION = "P_TRANSMISSION"
_PHASE = "PHASE"
_POL_ELLIPSE = "POL_ELLIPSE"
_MAJOR_AXIS = "MAJOR_AXIS"
_MINOR_AXIS = "MINOR_AXIS"
_ANGLE = "ANGLE"
_S_AMP_REFLECTION = "S_AMP_REFLECTION"
_S_AMP_TRANSMISSION = "S_AMP_TRANSMISSION"
_P_AMP_REFLECTION = "P_AMP_REFLECTION"
_P_AMP_TRANSMISSION = "P_AMP_TRANSMISSION"
_POL_PER_ANG = "POL_PER_ANG"
_RAY_CORDS_FIELD = "RAY_CORDS_FIELD"
_N_POINTS = "N_POINTS"
_PSF_DELTA = "PSF_DELTA"
_PSF_DATA = "PSF_DATA"
_POS_PER_ANG = "POS_PER_ANG"
_MTF = "MTF"
_FREQ = "FREQ"
_TAN = "TAN"
_SAG = "SAG"
_R_GEO = "R_GEO"
_R_RMS = "R_RMS"
_POINTS = "POINTS"
_SPOT = "SPOT"
_PSF = "PSF"
_CHIEF_RAY_CORDS = "CHIEF_RAY_CORDS"
_POSITION = "POSITION"
_FLDX = "FLDX"
_FLDY = "FLDY"
_FWGT = "FWGT"
_FVDX = "FVDX"
_FVDY = "FVDY"
_FVCX = "FVCX"
_FVCY = "FVCY"
_FVAN = "FVAN"
_FIELDS = "FIELDS"


class Field(namedtuple("Field", "FLDX, FLDY, FWGT, FVDX, FVDY, FVCX, FVCY, FVAN")):
    """
    Репрезентирует информацию о падающем поле в файле результатов.
    """
    __slots__ = ()

    def __new__(cls, fldx: float, fldy: float, fwgt: float,
                fvdx: float, fvdy: float, fvcx: float, fvcy: float, fvan: float):
        return super().__new__(cls, fldx, fldy, fwgt, fvdx, fvdy, fvcx, fvcy, fvan)

    def __str__(self):
        return f"{{\"FLDX\": {self.FLDX}, \"FLDY\": {self.FLDY}," \
               f" \"FWGT\": {self.FWGT}, \"FVDX\": {self.FVDX}," \
               f" \"FVDY\": {self.FVDY}, \"FVCX\": {self.FVCX}," \
               f" \"FVCY\": {self.FVCY}, \"FVAN\": {self.FVAN}}}"

    def __len__(self) -> int:
        return 1


class RayPolarization(namedtuple("RayPolarization", "INTENSITY, E_REAL, E_IMAG, S_REFLECTION,"
                                                    "S_TRANSMISSION, P_REFLECTION, P_TRANSMISSION,"
                                                    "PHASE, POL_ELLIPSE, S_AMP_REFLECTION, S_AMP_TRANSMISSION,"
                                                    "P_AMP_REFLECTION, P_AMP_TRANSMISSION")):
    """
     Репрезентирует информацию о поляризации всех падающих полей в плоскости изображения для файла результатов.
     | - INTENSITY      - интенсивность E,
     | - E_REAL         - Действительная часть вектора E,
     | - E_IMAG         - Мнимая часть вектора E,
     | - S_REFLECTION   - Отражение для S - поляризации,
     | - S_TRANSMISSION - Пропускание для S - поляризации,
     | - P_REFLECTION   - Отражение для P - поляризации,
     | - P_TRANSMISSION - Пропускание для P - поляризации,
     | - PHASE          - Фаза поля для компонент вектора E,
     | - POL_ELLIPSE    - Эллипс поляризации,
     | - S_AMP_REFLECTION   - Абсолютное значение для отражение для S - поляризации,
     | - S_AMP_TRANSMISSION - Абсолютное значение для пропускание для S - поляризации,
     | - P_AMP_REFLECTION   - Абсолютное значение для отражение для P - поляризации,
     | - P_AMP_TRANSMISSION - Абсолютное значение для пропускание для P - поляризации.
    """
    __slots__ = ()

    def __new__(cls, intensity: float,
                e_real: Vector3,
                e_image: Vector3,
                s_reflection: Vector2,
                s_transmission: Vector2,
                p_reflection: Vector2,
                p_transmission: Vector2,
                phase: Vector3,
                pol_ellipse: Vector3,
                s_amp_reflection: Vector2,
                s_amp_transmission: Vector2,
                p_amp_reflection: Vector2,
                p_amp_transmission: Vector2):
        return super().__new__(cls, intensity, e_real, e_image, s_reflection, s_transmission, p_reflection,
                               p_transmission, phase, pol_ellipse, s_amp_reflection, s_amp_transmission,
                               p_amp_reflection, p_amp_transmission)

    def __str__(self):
        return f"{{\n" \
               f" \"INTENSITY\"          : {self.INTENSITY},\n" \
               f" \"E_REAL\"             : {self.E_REAL},\n" \
               f" \"E_IMAG\"             : {self.E_IMAG},\n" \
               f" \"S_REFLECTION\"       : {self.S_REFLECTION},\n" \
               f" \"S_TRANSMISSION\"     : {self.S_TRANSMISSION},\n" \
               f" \"P_REFLECTION\"       : {self.P_REFLECTION},\n" \
               f" \"P_TRANSMISSION\"     : {self.P_TRANSMISSION},\n" \
               f" \"PHASE\"              : {self.PHASE},\n" \
               f" \"POL_ELLIPSE\"        : {{\"MAJOR_AXIS\": {self.POL_ELLIPSE.x}," \
               f" \"MINOR_AXIS\": {self.POL_ELLIPSE.y}," \
               f" \"ANGLE\": {self.POL_ELLIPSE.z}}}\n" \
               f" \"S_AMP_REFLECTION\"   : {self.S_AMP_REFLECTION},\n" \
               f" \"S_AMP_TRANSMISSION\" : {self.S_AMP_TRANSMISSION},\n" \
               f" \"P_AMP_REFLECTION\"   : {self.P_AMP_REFLECTION},\n" \
               f" \"P_AMP_TRANSMISSION\" : {self.P_AMP_TRANSMISSION}\n}}"

    def __len__(self) -> int:
        return 1


class ChiefRay(namedtuple("ChiefRay", "FIELD_ID, WAVE_ID, POSITION")):
    __slots__ = ()

    def __new__(cls, field_id: int, wave_id: int, position: Vector2):
        return super().__new__(cls, field_id, wave_id, position)

    def __str__(self):
        return f"{{\"FIELD_ID\": {self.FIELD_ID}," \
               f" \"WAVE_ID\": {self.WAVE_ID}," \
               f" \"POSITION\": {self.POSITION}}}"

    def __len__(self) -> int:
        return 1


class PupilVignetting(namedtuple("PupilVignetting", "pupil, position, vignetting")):
    __slots__ = ()

    def __new__(cls, angles: Vector2, position: Vector2, vignetting: float):
        return super().__new__(cls, angles, position, vignetting)

    def __str__(self):
        return f"{{\"PX\": {self.pupil.x}, \"PX\": {self.pupil.y}, " \
               f"\"X\": {self.position.x}, \"Y\": {self.position.y}," \
               f"\"RAY_V\": {self.vignetting}}}"

    def __len__(self) -> int:
        return 1


class AngleToImagePos(namedtuple("AngleToImagePos", "angles, position")):
    __slots__ = ()

    def __new__(cls, angles: Vector2, position: Vector2):
        return super().__new__(cls, angles, position)

    def __str__(self):
        return f"{{\"AX\": {self.angles.x}, \"AY\": {self.angles.y}, " \
               f"\"X\": {self.position.x}, \"Y\": {self.position.y}}}"

    def __len__(self) -> int:
        return 1


class RaysPolarizationDistribution(namedtuple("RaysPolarizationDistribution", "WAVE_ID, AX_MIN, AX_MAX, AY_MIN, AY_MAX,"
                                                                              "N_ANGLES_X, N_ANGLES_Y, POL_PER_ANG")):
    __slots__ = ()

    def __new__(cls, wave_id: int, ax_min: float, ax_max: float, ay_min: float,
                ay_max: float, n_angles_x: int, n_angles_y: int, pos_per_ang: List[RayPolarization]):
        return super().__new__(cls, wave_id, ax_min, ax_max, ay_min, ay_max,
                               n_angles_x, n_angles_y, pos_per_ang)

    def __len__(self) -> int:
        return 1


class PupilVignettingDistribution(namedtuple("PupilVignettingDistribution", "WAVE_ID, PX_MIN, PX_MAX, PY_MIN, PY_MAX, "
                                                                            "N_X, N_Y, VIG_PER_POS")):
    __slots__ = ()

    def __new__(cls, wave_id: int, px_min: float, px_max: float, py_min: float,
                py_max: float, n_x: int, n_y: int, vig_per_ang: List[PupilVignetting]):
        return super().__new__(cls, wave_id, px_min, px_max, py_min, py_max, n_x, n_y, vig_per_ang)

    def __len__(self) -> int:
        return 1

    @property
    def x_slice(self):
        return np.array([self.VIG_PER_POS[i + self.N_X * self.N_Y // 2].position.x for i in range(self.N_X)])

    @property
    def y_slice(self):
        return np.array([self.VIG_PER_POS[i * self.N_X + self.N_Y // 2].position.y for i in range(self.N_Y)])

    @property
    def vignetting(self):
        return np.array([v.vignetting for v in self.VIG_PER_POS]).reshape((self.N_Y, self.N_X))

    @property
    def pupil_coordinates(self):
        return np.linspace(self.PX_MIN, self.PX_MAX, self.N_X, dtype=float), \
               np.linspace(self.PY_MIN, self.PY_MAX, self.N_Y, dtype=float)

    # @property
    # def images_coordinates(self):
    #     return np.linspace(self.PX_MIN, self.PX_MAX, self.N_X, dtype=float), \
    #            np.linspace(self.PY_MIN, self.PY_MAX, self.N_Y, dtype=float)


class AngleToImagePosDistribution(namedtuple("AngleToImagePosDistribution", "WAVE_ID, AX_MIN, AX_MAX, AY_MIN, AY_MAX, "
                                                                            "N_ANGLES_X, N_ANGLES_Y, POS_PER_ANG")):
    __slots__ = ()

    def __new__(cls, wave_id: int, ax_min: float, ax_max: float, ay_min: float,
                ay_max: float, n_angles_x: int, n_angles_y: int, pos_per_ang: List[AngleToImagePos]):
        return super().__new__(cls, wave_id, ax_min, ax_max, ay_min, ay_max,
                               n_angles_x, n_angles_y, pos_per_ang)

    def __len__(self) -> int:
        return 1

    @property
    def x_slice(self):
        return np.array([self.POS_PER_ANG[i + self.N_ANGLES_X * self.N_ANGLES_Y // 2].position.x
                         for i in range(self.N_ANGLES_X)])

    @property
    def y_slice(self):
        return np.array([self.POS_PER_ANG[i * self.N_ANGLES_X + self.N_ANGLES_Y // 2].position.y
                         for i in range(self.N_ANGLES_Y)])


class SpotDiagram(namedtuple("SpotDiagram", "FIELD_ID, WAVE_ID, POINTS, R_RMS, R_GEO, CENTER")):
    __slots__ = ()

    def __new__(cls, field_id: int, wave_id: int, points: List[Vector2], r_rms: float, r_geo: float):
        center = sum(v for v in points) / len(points)
        return super().__new__(cls, field_id, wave_id, points, r_rms, r_geo, center)

    def __str__(self):
        sep = ',\n\t\t'
        return f"{{\n" \
               f"\t\"FIELD_ID\": {self.FIELD_ID},\n" \
               f"\t\"WAVE_ID\": {self.WAVE_ID},\n" \
               f"\t\"POINTS\": [\n\t\t{sep.join(str(v) for v in self.POINTS)}\n\t],\n" \
               f"\t\"R_RMS\": {self.R_RMS},\n" \
               f"\t\"R_RMS\": {self.R_GEO}\n" \
               f"}}"

    def __len__(self) -> int:
        return 1


class PSFDiagram(namedtuple("SpotDiagram", "FIELD_ID, WAVE_ID, N_POINTS, CENTER, PSF_DELTA, PSF_DATA, PSF_MAX")):
    __slots__ = ()

    MUM_TO_MM = 0.001

    def __new__(cls, field_id: int, wave_id: int, n_points: int, psf_delta: float,
                position: Vector2, psf_data: List[float]):
        n_samples = int(math.sqrt(len(psf_data) // 4))
        data = np.array(psf_data).reshape((n_samples, n_samples, 4))
        i, j = np.unravel_index(data[:, :, 0].argmax(), (n_samples, n_samples))

        max_val = Vector3((j - n_samples * 0.5) * psf_delta * PSFDiagram.MUM_TO_MM,
                          (i - n_samples * 0.5) * psf_delta * PSFDiagram.MUM_TO_MM, data[i, j, 0])

        return super().__new__(cls, field_id, wave_id, n_points, position, psf_delta, data, max_val)

    @property
    def relative_intensity(self) -> float:
        return self.PSF_MAX.z

    @property
    def center_world_space(self) -> Vector2:
        return Vector2(self.PSF_MAX.x + self.CENTER.x, self.PSF_MAX.y + self.CENTER.y)

    @property
    def center_local_space(self) -> Vector2:
        return Vector2(self.PSF_MAX.x, self.PSF_MAX.y)

    @property
    def width(self) -> float:
        return self.cols * self.delta_in_mm

    @property
    def height(self) -> float:
        return self.rows * self.delta_in_mm

    @property
    def delta_in_mm(self) -> float:
        return self.PSF_DELTA * PSFDiagram.MUM_TO_MM

    @property
    def rows(self) -> int:
        return self.PSF_DATA.shape[0]

    @property
    def cols(self) -> int:
        return self.PSF_DATA.shape[1]

    def cross_section(self, u: float, v: float) -> Tuple[np.ndarray, np.ndarray]:
        row = min(max(0, int(v * self.rows)), self.rows - 1)
        col = min(max(0, int(u * self.cols)), self.cols - 1)
        return self.PSF_DATA[:, col, 0], self.PSF_DATA[row, :, 0]

    @property
    def cross_section_at_center(self) -> Tuple[np.ndarray, np.ndarray]:
        return self.cross_section(0.5, 0.5)

    def __str__(self):
        sep = ','
        return f"{{\n" \
               f"\t\"FIELD_ID\": {self.FIELD_ID},\n" \
               f"\t\"WAVE_ID\": {self.WAVE_ID},\n" \
               f"\t\"N_POINTS\": {self.N_POINTS},\n" \
               f"\t\"PSF_DELTA\": {self.PSF_DELTA}," \
               f"\t\"PSF_DATA\": [\n\t\t{sep.join(str(v) for v in self.PSF_DATA)}\n\t]\n" \
               f"}}"

    def __len__(self) -> int:
        return 1


class MTFResponse(namedtuple("ChiefRay", "FIELD_ID, WAVE_ID, FREQ, TAN, SAG")):
    __slots__ = ()

    def __new__(cls, field_id: int, wave_id: int, freq: List[float], tan: List[float], sag: List[float]):
        return super().__new__(cls, field_id, wave_id, freq, tan, sag)

    def __str__(self):
        sep = ',\n'

        def fts(f, t, s):
            return f'\t\t\"FREQ\": {f}, \"TAN\": {t}, \"SAG\": {s}}}'

        return f"{{" \
               f"\t\"FIELD_ID\": {self.FIELD_ID},\n" \
               f"\t\"WAVE_ID\": {self.WAVE_ID},\n" \
               f"\t\"POINTS\":" \
               f"\n\t[\n\t\t{sep.join(fts(f, t, s) for f, t, s in zip(self.FREQ, self.TAN, self.SAG))}\n\t]" \
               f"\n}}"

    def __len__(self) -> int:
        return 1


def read_fields(json_node) -> Union[Dict[int, Field], None]:
    if _FIELDS not in json_node:
        return None
    fields = {}
    node = json_node[_FIELDS]
    for n_id, n in enumerate(node):
        try:
            fldx = n[_FLDX] if _FLDX in n else 0.0
            fldy = n[_FLDY] if _FLDY in n else 0.0
            fwgt = n[_FWGT] if _FWGT in n else 0.0
            fvdx = n[_FVDX] if _FVDX in n else 0.0
            fvdy = n[_FVDY] if _FVDY in n else 0.0
            fvcx = n[_FVCX] if _FVCX in n else 0.0
            fvcy = n[_FVCY] if _FVCY in n else 0.0
            fvan = n[_FVAN] if _FVAN in n else 0.0
            fields.update({n_id + 1: Field(fldx, fldy, fwgt, fvdx, fvdy, fvcx, fvcy, fvan)})
        except KeyError as _:
            continue
        except ValueError as _:
            continue
    return fields


def read_chief_rays(json_node) -> Union[List[ChiefRay], None]:
    if _CHIEF_RAY_CORDS not in json_node:
        return None
    chief_rays = []
    node = json_node[_CHIEF_RAY_CORDS]
    for n in node:
        try:
            field_id = int(n[_FIELD_ID])
            wave_id = int(n[_WAVE_ID])
            position = Vector2(float(n[_POSITION][_X]), float(n[_POSITION][_Y]))
            chief_rays.append(ChiefRay(field_id, wave_id, position))
        except KeyError as _:
            continue
        except ValueError as _:
            continue
    return chief_rays


def read_spots(json_node) -> Union[List[SpotDiagram], None]:
    if _SPOT not in json_node:
        return None
    spots = []
    node = json_node[_SPOT]
    for n in node:
        try:
            field_id = int(n[_FIELD_ID])
            wave_id = int(n[_WAVE_ID])
            r_geo = float(n[_R_GEO])
            r_rms = float(n[_R_RMS])
            points = [Vector2(float(v[_X]), float(v[_Y])) for v in n[_POINTS]]
            spots.append(SpotDiagram(field_id, wave_id, points, r_rms, r_geo))
        except KeyError as _:
            continue
        except ValueError as _:
            continue
    return spots


def read_mtf(json_node) -> Union[List[MTFResponse], None]:
    if _MTF not in json_node:
        return None
    spots = []
    node = json_node[_MTF]
    if isinstance(node, str):
        mtf_info = []
        for line in node.split("\n"):
            line = line.strip().split(" ")
            if line[0] == "Field:":
                mtf_info.append([])
                continue
            try:
                mtf_info[-1].append((float(line[0]), float(line[1]), float(line[2])))
            except ValueError as _:
                continue
            except IndexError as _:
                continue
        for field_id, mtf in enumerate(mtf_info):
            spots.append(MTFResponse(field_id + 1, -1, [v[0] for v in mtf], [v[1] for v in mtf], [v[2] for v in mtf]))
        return spots
    for n in node:
        try:
            field_id = int(n[_FIELD_ID])
            wave_id = int(n[_WAVE_ID])
            mtf = n[_MTF]
            freq = []
            tan = []
            sag = []
            for v in mtf:
                freq.append(float(v[_FREQ]))
                tan.append(float(v[_TAN]))
                sag.append(float(v[_SAG]))
            spots.append(MTFResponse(field_id, wave_id, freq, tan, sag))
        except KeyError as _:
            continue
        except ValueError as _:
            continue
    return spots


def read_psf(json_node) -> Union[List[PSFDiagram], None]:
    if _PSF not in json_node:
        return None
    spots = []
    node = json_node[_PSF]
    for n in node:
        try:
            field_id = int(n[_FIELD_ID])
            wave_id = int(n[_WAVE_ID])
            n_points = int(n[_N_POINTS])
            delta = float(n[_PSF_DELTA])
            center = Vector2(float(n['CENTER'][_X]), float(n['CENTER'][_Y]))
            spots.append(PSFDiagram(field_id, wave_id, n_points, delta, center, [float(v) for v in n[_PSF_DATA]]))
        except KeyError as _:
            continue
        except ValueError as _:
            continue
    return spots


def read_cord_ang_dep(json_node) -> Union[List[AngleToImagePosDistribution], None]:
    if _RAY_CORDS_FIELD not in json_node:
        return None
    cord_dep = []
    node = json_node[_RAY_CORDS_FIELD]
    for n in node:
        try:
            ang_x_min = float(n[_AX_MIN])
            ang_x_max = float(n[_AX_MAX])
            ang_y_min = float(n[_AY_MIN])
            ang_y_max = float(n[_AY_MAX])
            n_ang_x = int(n[_N_ANGLES_X])
            n_ang_y = int(n[_N_ANGLES_Y])
            wave_id = int(n[_WAVE_ID])
            pts = [AngleToImagePos(Vector2(float(v[_AX]), float(v[_AY])),
                                   Vector2(float(v[_X]), float(v[_Y]))) for v in n[_POS_PER_ANG]]
            cord_dep.append(AngleToImagePosDistribution(wave_id, ang_x_min, ang_x_max, ang_y_min,
                                                        ang_y_max, n_ang_x, n_ang_y, pts))
        except KeyError as _:
            continue
        except ValueError as _:
            continue
    return cord_dep


def read_rays_pol(json_node) -> Union[List[RaysPolarizationDistribution], None]:
    if _RAY_POL_FIELD not in json_node:
        return None
    cord_dep = []
    node = json_node[_RAY_POL_FIELD]
    for n in node:
        try:
            ang_x_min = float(n[_AX_MIN])
            ang_x_max = float(n[_AX_MAX])
            ang_y_min = float(n[_AY_MIN])
            ang_y_max = float(n[_AY_MAX])
            n_ang_x = int(n[_N_ANGLES_X])
            n_ang_y = int(n[_N_ANGLES_Y])
            wave_id = int(n[_WAVE_ID])
            pts = [RayPolarization(float(v[_INTENSITY]),
                                   Vector3(float(v[_E_REAL][_X]), float(v[_E_REAL][_Y]), float(v[_E_REAL][_Z])),
                                   Vector3(float(v[_E_IMAG][_X]), float(v[_E_IMAG][_Y]), float(v[_E_IMAG][_Z])),
                                   Vector2(float(v[_S_REFLECTION][_X]), float(v[_S_REFLECTION][_Y])),
                                   Vector2(float(v[_S_TRANSMISSION][_X]), float(v[_S_TRANSMISSION][_Y])),
                                   Vector2(float(v[_P_REFLECTION][_X]), float(v[_P_REFLECTION][_Y])),
                                   Vector2(float(v[_P_TRANSMISSION][_X]), float(v[_P_TRANSMISSION][_Y])),
                                   Vector3(float(v[_PHASE][_X]), float(v[_PHASE][_Y]), float(v[_PHASE][_Z])),
                                   Vector3(float(v[_POL_ELLIPSE][_MAJOR_AXIS]), float(v[_POL_ELLIPSE][_MINOR_AXIS]),
                                           float(v[_POL_ELLIPSE][_ANGLE])),
                                   Vector2(float(v[_S_AMP_REFLECTION][_X]), float(v[_S_AMP_REFLECTION][_Y])),
                                   Vector2(float(v[_S_AMP_TRANSMISSION][_X]), float(v[_S_AMP_TRANSMISSION][_Y])),
                                   Vector2(float(v[_P_AMP_REFLECTION][_X]), float(v[_P_AMP_REFLECTION][_Y])),
                                   Vector2(float(v[_P_AMP_TRANSMISSION][_X]), float(v[_P_AMP_TRANSMISSION][_Y])))
                   for v in n[_POL_PER_ANG]]
            cord_dep.append(RaysPolarizationDistribution(wave_id, ang_x_min, ang_x_max, ang_y_min,
                                                         ang_y_max, n_ang_x, n_ang_y, pts))
        except KeyError as _:
            continue
        except ValueError as _:
            continue
    return cord_dep


def read_vignetting_dep(json_node) -> Union[List[PupilVignettingDistribution], None]:
    if _RAY_VIGNETTING not in json_node:
        return None
    cord_dep = []
    node = json_node[_RAY_VIGNETTING]
    for n in node:
        try:
            ang_x_min = float(n[_PX_MIN])
            ang_x_max = float(n[_PX_MAX])
            ang_y_min = float(n[_PY_MIN])
            ang_y_max = float(n[_PY_MAX])
            n_ang_x = int(n[_N_X])
            n_ang_y = int(n[_N_X])
            wave_id = int(n[_WAVE_ID])
            pts = [PupilVignetting(Vector2(float(v[_PX]), float(v[_PY])),
                                   Vector2(float(v[_X]), float(v[_Y])), float(v['RAY_V'])) for v in n[_VIG_PER_POS]]
            cord_dep.append(PupilVignettingDistribution(wave_id, ang_x_min, ang_x_max, ang_y_min,
                                                        ang_y_max, n_ang_x, n_ang_y, pts))
        except KeyError as _:
            continue
        except ValueError as _:
            continue
    return cord_dep
