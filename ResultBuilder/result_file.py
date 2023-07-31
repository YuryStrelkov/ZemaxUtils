from .result_components import read_cord_ang_dep, AngleToImagePosDistribution, Field
from .result_components import RaysPolarizationDistribution
from .result_components import PupilVignettingDistribution
from .result_components import read_vignetting_dep
from .result_components import read_chief_rays
from .result_components import read_rays_pol
from .result_components import MTFResponse
from .result_components import SpotDiagram
from .result_components import read_fields
from .result_components import PSFDiagram
from .result_components import read_spots
from .result_components import ChiefRay
from .result_components import read_mtf
from .result_components import read_psf
from typing import List, Dict, Union
from .utils import change_encoding
from Geometry import Vector2
import numpy as np
import os.path
import json


_ENTRIES_COUNT = "ENTRIES_COUNT"
_APERTURE_VALUE = "APERTURE_VALUE"
_APODIZATION_FACTOR = "APODIZATION_FACTOR"
_APODIZATION_TYPE = "APODIZATION_TYPE"
_USE_ENV_DATA = "USE_ENV_DATA"
_TEMP_C = "TEMP_C"
_PRESSURE_ATM = "PRESSURE_ATM"
_IMAGE_SPACE_F_DIV_N = "IMAGE_SPACE_F_DIV_#"
_OBJECT_SPACE_NA = "OBJECT_SPACE_NA"
_WORKING_F_DIV_N = "WORKING_F_DIV_#"
_ENTRANCE_PUPIL_DIA = "ENTRANCE_PUPIL_DIA"
_ENTRANCE_PUPIL_POS = "ENTRANCE_PUPIL_POS"
_EXIT_PUPIL_DIA = "EXIT_PUPIL_DIA"
_EXIT_PUPIL_POS = "EXIT_PUPIL_POS"
_PARAX_IMAGE_HEIGHT = "PARAX_IMAGE_HEIGHT"
_PARAX_MAGNIFICATION = "PARAX_MAGNIFICATION"
_ANGULAR_MAGNIFICATION = "ANGULAR_MAGNIFICATION"
_TOTAL_TRACK = "TOTAL_TRACK"
_USE_RAY_AIMING = "USE_RAY_AIMING"
_X_PUPIL_SHIFT = "X_PUPIL_SHIFT"
_Y_PUPIL_SHIFT = "Y_PUPIL_SHIFT"
_Z_PUPIL_SHIFT = "Z_PUPIL_SHIFT"
_STOP_SURFACE_NUMBER = "STOP_SURFACE_NUMBER"
_WAVELENGTHS = "WAVELENGTHS"
_WAVELENGTHS_WEIGHTS = "WAVELENGTHS_WEIGHTS"
_EFL = "EFL"


class ResultFile:
    def __init__(self):
        self.scheme_src = ""
        self.wavelengths_weights = []
        self.wavelengths = []
        self.chief_rays: List[ChiefRay] = []
        self.fields: Dict[int, Field]  = {}
        self.spots: List[SpotDiagram] = []
        self.psf_s: List[PSFDiagram] = []
        self.mtf_s: List[MTFResponse] = []
        self.cords: List[AngleToImagePosDistribution] = []
        self.vignetting: List[PupilVignettingDistribution] = []
        self.polarization: List[RaysPolarizationDistribution] = []
        self.entries_count: int = 0
        self.aperture_value: float = 0.0
        self.apodization_factor: float = 0.0
        self.apodization_type: float = 0.0
        self.use_env_data: float = 0.0
        self.temp_c: float = 0.0
        self.pressure_atm: float = 0.0
        self.efl: float = 0.0
        self.image_space_f_div: float = 0.0
        self.object_space_na: float = 0.0
        self.working_f_div_: float = 0.0
        self.entrance_pupil_dia: float = 0.0
        self.entrance_pupil_pos: float = 0.0
        self.exit_pupil_dia: float = 0.0
        self.exit_pupil_pos: float = 0.0
        self.parax_image_height: float = 0.0
        self.parax_magnification: float = 0.0
        self.angular_magnification: float = 0.0
        self.total_track: float = 0.0
        self.use_ray_aiming: float = 0.0
        self.x_pupil_shift: float = 0.0
        self.y_pupil_shift: float = 0.0
        self.z_pupil_shift: float = 0.0
        self.stop_surface_number: int = 0

    def load(self, file_src):
        if not os.path.exists(file_src):
            print(f"file at path {file_src} does not exists...")
            return
        self.scheme_src = file_src
        change_encoding(self.scheme_src, "utf-8")
        with open(self.scheme_src, "rt") as report:
            _json = json.load(report)
            self.fields = read_fields(_json)
            self.chief_rays = read_chief_rays(_json)
            self.spots = read_spots(_json)
            self.mtf_s = read_mtf(_json)
            self.psf_s = read_psf(_json)
            self.cords = read_cord_ang_dep(_json)
            self.polarization = read_rays_pol(_json)
            self.vignetting = read_vignetting_dep(_json)
            self.entries_count = int(_json[_ENTRIES_COUNT]) if _ENTRIES_COUNT in _json else 0
            self.aperture_value = float(_json[_APERTURE_VALUE]) if _APERTURE_VALUE in _json else 0.0
            self.apodization_factor = float(_json[_APODIZATION_FACTOR]) if _APODIZATION_FACTOR in _json else 0.0
            self.apodization_type = float(_json[_APODIZATION_TYPE]) if _APODIZATION_TYPE in _json else 0.0
            self.use_env_data = float(_json[_USE_ENV_DATA]) if _USE_ENV_DATA in _json else 0.0
            self.temp_c = float(_json[_TEMP_C]) if _TEMP_C in _json else 0.0
            self.pressure_atm = float(_json[_PRESSURE_ATM]) if _PRESSURE_ATM in _json else 0.0
            self.efl = float(_json[_EFL]) if _EFL in _json else 0.0
            self.image_space_f_div = float(_json[_IMAGE_SPACE_F_DIV_N]) if _IMAGE_SPACE_F_DIV_N in _json else 0.0
            self.object_space_na = float(_json[_OBJECT_SPACE_NA]) if _OBJECT_SPACE_NA in _json else 0.0
            self.working_f_div_ = float(_json[_WORKING_F_DIV_N]) if _WORKING_F_DIV_N in _json else 0.0
            self.entrance_pupil_dia = float(_json[_ENTRANCE_PUPIL_DIA]) if _ENTRANCE_PUPIL_DIA in _json else 0.0
            self.entrance_pupil_pos = float(_json[_ENTRANCE_PUPIL_POS]) if _ENTRANCE_PUPIL_POS in _json else 0.0
            self.exit_pupil_dia = float(_json[_EXIT_PUPIL_DIA]) if _EXIT_PUPIL_DIA in _json else 0.0
            self.exit_pupil_pos = float(_json[_EXIT_PUPIL_POS]) if _EXIT_PUPIL_DIA in _json else 0.0
            self.parax_image_height = float(_json[_PARAX_IMAGE_HEIGHT]) if _PARAX_IMAGE_HEIGHT in _json else 0.0
            self.parax_magnification = float(_json[_PARAX_MAGNIFICATION]) if _PARAX_MAGNIFICATION in _json else 0.0
            self.angular_magnification = \
                float(_json[_ANGULAR_MAGNIFICATION]) if _ANGULAR_MAGNIFICATION in _json else 0.0
            self.total_track = float(_json[_TOTAL_TRACK]) if _TOTAL_TRACK in _json else 0.0
            self.use_ray_aiming = float(_json[_USE_RAY_AIMING]) if _USE_RAY_AIMING in _json else 0.0
            self.x_pupil_shift = float(_json[_X_PUPIL_SHIFT]) if _X_PUPIL_SHIFT in _json else 0.0
            self.y_pupil_shift = float(_json[_Y_PUPIL_SHIFT]) if _Y_PUPIL_SHIFT in _json else 0.0
            self.z_pupil_shift = float(_json[_Z_PUPIL_SHIFT]) if _Z_PUPIL_SHIFT in _json else 0.0
            self.stop_surface_number = int(_json[_STOP_SURFACE_NUMBER]) if _STOP_SURFACE_NUMBER in _json else 0
            try:
                self.wavelengths = list(map(float, (v for v in _json[_WAVELENGTHS])))
                self.wavelengths_weights = list(map(float, (v for v in _json[_WAVELENGTHS_WEIGHTS])))
            except ValueError as _:
                ...
            except KeyError as _:
                ...
            except RuntimeError as _:
                ...

    @property
    def n_wave_lengths(self) -> int:
        return len(self.wavelengths)

    @property
    def n_wave_lengths_weights(self) -> int:
        return len(self.wavelengths)

    @property
    def n_fields(self) -> int:
        return len(self.fields)

    def get_mtf(self, field_id: int, wave_id: int) -> Union[MTFResponse, List[MTFResponse],  None]:
        if field_id == -1 and wave_id == -1:
            return self.mtf_s

        if field_id == -1:
            return [v for v in self.mtf_s if v.WAVE_ID == wave_id]

        if wave_id == -1:
            return [v for v in self.mtf_s if v.FIELD_ID == field_id]

        response = [v for v in self.mtf_s if v.FIELD_ID == field_id and v.WAVE_ID == wave_id]

        if len(response) == 0:
            return None

        return response[0]

    def get_chief_ray(self, field_id: int, wave_id: int) -> Union[ChiefRay, List[ChiefRay], None]:
        if field_id == -1 and wave_id == -1:
            return self.chief_rays

        if field_id == -1:
            return [v for v in self.chief_rays if v.WAVE_ID == wave_id]

        if wave_id == -1:
            return [v for v in self.chief_rays if v.FIELD_ID == field_id]

        responses = [v for v in self.chief_rays if v.FIELD_ID == field_id and v.WAVE_ID == wave_id]

        if len(responses) == 0:
            return ChiefRay(-1, -1, Vector2(0, 0))

        return responses[0]

    def get_spot(self, field_id: int, wave_id: int) -> Union[SpotDiagram, List[SpotDiagram], None]:
        if field_id == -1 and wave_id == -1:
            return self.spots

        if field_id == -1:
            return [v for v in self.spots if v.WAVE_ID == wave_id]

        if wave_id == -1:
            return [v for v in self.spots if v.FIELD_ID == field_id]

        responses = [v for v in self.spots if v.FIELD_ID == field_id and v.WAVE_ID == wave_id]

        if len(responses) == 0:
            return None

        return responses[0]

    def get_psf(self, field_id: int, wave_id: int) -> Union[PSFDiagram, List[PSFDiagram], None]:
        if field_id == -1 and wave_id == -1:
            return self.psf_s

        if field_id == -1:
            return [v for v in self.psf_s if v.WAVE_ID == wave_id]

        if wave_id == -1:
            return [v for v in self.psf_s if v.FIELD_ID == field_id]

        responses = [v for v in self.psf_s if v.FIELD_ID == field_id and v.WAVE_ID == wave_id]
        if len(responses) == 0:
            return None
        return responses[0]

    @property
    def x_angles(self):
        return np.array(sorted([f.FLDX for f in self.fields.values()]))

    @property
    def y_angles(self):
        return np.array(sorted([f.FLDY for f in self.fields.values()]))

    @property
    def chief_ray_x_slice(self):
        slices = [(v.WAVE_ID, v.x_slice) for v in self.cords]
        slices = sorted(slices, key=lambda v: slices[0])
        return [b for a, b in slices]

    @property
    def chief_ray_y_slice(self):
        slices = [(v.WAVE_ID, v.y_slice) for v in self.cords]
        slices = sorted(slices, key=lambda v: slices[0])
        return [b for a, b in slices]

    @property
    def x_image_pos_per_angle(self) -> List[np.ndarray]:
        """
            Возвращает список массиовов х-координат центров спот диаграм. Координаты отсортированы по возрастанию.
            Каждый массив соответствует длине волны с тем же индексом, что и массив в списке.
        """
        fields = [[v.CENTER for v in self.spots if v.WAVE_ID == wave_id + 1]for wave_id in range(self.n_wave_lengths)]
        fields = [sorted(v, key=lambda arg: arg.x)for v in fields]
        return [np.array([v.x for v in field])for field in fields]

    @property
    def y_image_pos_per_angle(self) -> List[np.ndarray]:
        """
            Возвращает список массивов у-координат центров спот диаграмм. Координаты отсортированы по возрастанию.
            Каждый массив соответствует длине волны с тем же индексом, что и массив в списке.
        """
        fields = [[v.CENTER for v in self.spots if v.WAVE_ID == wave_id + 1]for wave_id in range(self.n_wave_lengths)]
        fields = [sorted(v, key=lambda arg: arg.y)for v in fields]
        return [np.array([v.y for v in field])for field in fields]

    @property
    def x_image_pos_per_angle_from_psf(self) -> List[np.ndarray]:
        """
            Возвращает список массивов х-координат максимума интенсивности функции рассеяния точки.
            Координаты отсортированы по возрастанию. Каждый массив соответствует длине волны с тем же
            индексом, что и массив в списке.
        """
        # fields = [[Vector2(v.PSF_MAX.x, v.PSF_MAX.y) + self.get_chief_ray(vi + 1, wave_id + 1).POSITION
        #            for vi, v in enumerate(self.get_psf(-1, wave_id + 1))] for wave_id in range(self.n_wave_lengths)]
        # fields = [sorted(v, key=lambda arg: arg.x)for v in fields]
        # return [np.array([v.x for v in field])for field in fields]
        fields = [[v.center_world_space.x for v in self.psf_s if v.WAVE_ID == wave_id + 1]
                  for wave_id in range(self.n_wave_lengths)]
        return [np.array(sorted(v, key=lambda arg: arg)) for v in fields]

    @property
    def y_image_pos_per_angle_from_psf(self) -> List[np.ndarray]:
        """
            Возвращает список массивов y-координат максимума интенсивности функции рассеяния точки.
            Координаты отсортированы по возрастанию. Каждый массив соответствует длине волны с тем же
            индексом, что и массив в списке.
        """
        # fields = [[Vector2(v.PSF_MAX.x, v.PSF_MAX.y) + self.get_chief_ray(vi + 1, wave_id + 1).POSITION
        #            for vi, v in enumerate(self.get_psf(-1, wave_id + 1))] for wave_id in range(self.n_wave_lengths)]
        # fields = [sorted(v, key=lambda arg: arg.y)for v in fields]
        # return [np.array([v.y for v in field])for field in fields]
        fields = [[v.center_world_space.y for v in self.psf_s if v.WAVE_ID == wave_id + 1]
                  for wave_id in range(self.n_wave_lengths)]
        return [np.array(sorted(v, key=lambda arg: arg)) for v in fields]

    @property
    def image_intensity_per_angle_from_psf(self) -> List[np.ndarray]:
        """
            Возвращает список массивов y-координат максимума интенсивности функции рассеяния точки.
            Координаты отсортированы по возрастанию. Каждый массив соответствует длине волны с тем же
            индексом, что и массив в списке.
        """
        # fields = [[Vector2(v.PSF_MAX.x, v.PSF_MAX.y) + self.get_chief_ray(vi + 1, wave_id + 1).POSITION
        #            for vi, v in enumerate(self.get_psf(-1, wave_id + 1))] for wave_id in range(self.n_wave_lengths)]
        # fields = [sorted(v, key=lambda arg: arg.y)for v in fields]
        # return [np.array([v.y for v in field])for field in fields]
        fields = [[v.center_world_space for v in self.psf_s if v.WAVE_ID == wave_id + 1]
                  for wave_id in range(self.n_wave_lengths)]
        fields = [sorted(v, key=lambda arg: arg.y) for v in fields]
        return [np.array([v.y for v in field]) for field in fields]

    @property
    def y_image_pos_per_angle_from_psf_avg(self) -> np.ndarray:
        """
            Возвращает массив х-координат максимума интенсивности функции рассеяния точки,
            усреднённого по всем длинам волн (усреднение не взвешанное).
        """
        fields = self.y_image_pos_per_angle_from_psf
        scale  = 1.0 / len(fields)
        return np.array([scale * sum(i for i in v) for v in zip(*fields)])

    @property
    def x_image_pos_per_angle_from_psf_avg(self) -> np.ndarray:
        """
            Возвращает массив y-координат максимума интенсивности функции рассеяния точки,
            усреднённого по всем длинам волн (усреднение не взвешанное).
        """
        fields = self.x_image_pos_per_angle_from_psf
        scale  = 1.0 / len(fields)
        return np.array([scale * sum(i for i in v) for v in zip(*fields)])

    @property
    def psf_spot_centers_diff_y(self) -> List[np.ndarray]:
        psf  = self.y_image_pos_per_angle_from_psf
        spot = self.y_image_pos_per_angle
        return [np.array([s - p for s, p in zip(si, pi)])for si, pi in zip(spot, psf)]

    @property
    def psf_spot_centers_diff_x(self) -> List[np.ndarray]:
        psf  = self.x_image_pos_per_angle_from_psf
        spot = self.x_image_pos_per_angle
        return [np.array([s - p for s, p in zip(si, pi)]) for si, pi in zip(spot, psf)]

    @property
    def fields_angles_x(self) -> np.ndarray:
        return np.array([v.FLDX for v in self.fields.values()])

    @property
    def fields_angles_y(self) -> np.ndarray:
        return np.array([v.FLDY for v in self.fields.values()])

    @property
    def fields_angles(self) -> np.ndarray:
        return np.array([Vector2(v.FLDX, v.FLDY) for v in self.fields.values()])
