from typing import List, Any, Dict, Union
from Geometry import Vector3, Vector2
from collections import namedtuple


def _round(v):
    try:
        return int(v) if v % 1 == 0 else v
    except TypeError as _:
        return v


class ZSurfaceTransform:
    """
    Описание способа преобразования системы координат для Zemax поверхности.
    """

    _AFTER_SURFACE = \
        {
            0: 'Explicit',
            1: 'Pickup This Surface',
            2: 'Reverse This Surface',
            3: 'Pickup Surface 1',
            4: 'Reverse Surface 1'
        }

    def __init__(self, transform_line: str = None):
        self._transform_order: int = 0
        self._order: int = 0
        self._after_surface: int = 0
        self.decenter: Vector2 = Vector2(0, 0)
        self.tilt:     Vector3 = Vector3(0, 0, 0)
        if transform_line is None:
            return
        transform_line = transform_line.split(" ")
        self.order           = int(transform_line[0])
        self.transform_order = int(transform_line[1])
        self.after_surface   = int(transform_line[2])
        self.decenter        = Vector2(float(transform_line[3]), float(transform_line[4]))
        self.tilt            = Vector3(float(transform_line[5]), float(transform_line[6]), float(transform_line[7]))

    def __repr__(self):
        td = "\"Tilt, Decenter\""
        dt = "\"Decenter, Tilt\""
        return f"{{\n" \
               f"\"Order\":         {dt if self._order == 0 else td},\n" \
               f"\"After Surface\": {ZSurfaceTransform._AFTER_SURFACE[self._after_surface]},\n" \
               f"\"Decenter X\":    {self.decenter.x:>10.5E},\n" \
               f"\"Decenter Y\":    {self.decenter.y:>10.5E},\n" \
               f"\"Tilt X\":        {self.tilt.x:>10.5E},\n" \
               f"\"Tilt Y\":        {self.tilt.y:>10.5E},\n" \
               f"\"Tilt Z\":        {self.tilt.z:>10.5E}\n}}"

    def __str__(self):
        return f"SCBD {self.order} {self.transform_order} {self.after_surface} {self.decenter.x} {self.decenter.y}" \
               f" {self.tilt.x} {self.tilt.y} {self.tilt.z}"

    @property
    def order(self) -> int:
        """
        Определяет порядок - трансформация до или после поверхности.
        :return:
        """
        return self._order

    @order.setter
    def order(self, value: int) -> None:
        """
        Определяет порядок - трансформация до или после поверхности.
        :return:
        """
        self._order = value if value in {1, 0} else self._order

    @property
    def transform_order(self) -> int:
        return self._transform_order

    @transform_order.setter
    def transform_order(self, value: int) -> None:
        self._transform_order = value if value in {1, 0} else self._transform_order

    @property
    def after_surface(self) -> int:
        return self._after_surface

    @after_surface.setter
    def after_surface(self, value: int) -> None:
        self._after_surface = value if value in ZSurfaceTransform._AFTER_SURFACE else self._after_surface


class ZFileField(namedtuple("ZFileField", "key, params" )):
    """
    Описание произвольного поля Zemax файла.
    Состоит из имени поля или его ключа и списка со значениями произвольного типа
    """
    def __new__(cls, field_line: str):
        field_line = field_line.split(" ")
        key: str = field_line[0]
        params: List[Any]   = []
        for v in field_line[1:]:
            try:
                params.append(float(v))
            except ValueError as _:
                params.append(v)
        return super().__new__(cls, key, params)

    def __str__(self):
        data = ' '.join(str(_round(v)) for v in self.params)
        data = data.replace("\\", '')
        return f"{self.key} {data}"


class ZSurface:
    """
    Описание поверхности Zemax файла.
    """
    Z_FILE_SURF_INDENT = '  '
    MAX_EVEN_ASPHERIC_TERM = 8
    MAX_ZERNIKE_TERM = 8

    def __init__(self, surface: Dict[str, List[str]]):
        self._curvature:    Union[ZFileField, None] = None
        self._semi_diam:    Union[ZFileField, None] = None
        self._material:     Union[ZFileField, None] = None
        self._others:       List[ZFileField]  = []
        self._type:         str         = "STANDARD"
        self.comment:       str         = ""
        self.conic:         float       = 0.0
        self.dist_z:        float       = 0.0
        self._params:       List[float] = []
        self._extra_params: List[float] = []
        self._transforms:   List[ZSurfaceTransform] = []
        self._parce(surface)

    @property
    def surf_type(self) -> str:
        return self._type

    @property
    def _has_transform_before(self) -> int:
        if len(self._transforms) == 0:
            return -1
        if len(self._transforms) == 1:
            return 0 if self._transforms[0].order == 0 else -1
        return 0 if self._transforms[0].order == 0 else 1

    @property
    def _has_transform_after(self) -> int:
        if len(self._transforms) == 0:
            return -1
        if len(self._transforms) == 1:
            return 0 if self._transforms[0].order == 1 else -1
        return 0 if self._transforms[0].order == 1 else 1

    @property
    def has_transform_before(self) -> bool:
        return self._has_transform_before != -1

    @property
    def has_transform_after(self) -> bool:
        return self._has_transform_after != -1

    @property
    def tilt_before(self) -> Vector3:
        index = self._has_transform_before
        return Vector3(0, 0, 0) if index == -1 else self._transforms[index].tilt

    @property
    def tilt_after(self) -> Vector3:
        index = self._has_transform_after
        return Vector3(0, 0, 0) if index == -1 else self._transforms[index].tilt

    @tilt_before.setter
    def tilt_before(self, tilt: Vector3) -> None:
        assert isinstance(tilt, Vector3)
        index = self._has_transform_before
        if index != -1:
            self._transforms[index].tilt = tilt

    @tilt_after.setter
    def tilt_after(self, tilt: Vector3) -> None:
        assert isinstance(tilt, Vector3)
        index = self._has_transform_after
        if index != -1:
            self._transforms[index].tilt = tilt

    @property
    def decenter_before(self) -> Vector2:
        index = self._has_transform_before
        return Vector2(0, 0) if index == -1 else self._transforms[index].decenter

    @property
    def decenter_after(self) -> Vector2:
        index = self._has_transform_after
        return Vector2(0, 0) if index == -1 else self._transforms[index].decenter

    @decenter_before.setter
    def decenter_before(self, decenter: Vector2) -> None:
        assert isinstance(decenter, Vector2)
        index = self._has_transform_before
        if index != -1:
            self._transforms[index].decenter = decenter

    @decenter_after.setter
    def decenter_after(self, decenter: Vector2) -> None:
        assert isinstance(decenter, Vector2)
        index = self._has_transform_after
        if index != -1:
            self._transforms[index].decenter = decenter

    @property
    def aperture(self):
        return self._semi_diam.params[0]

    @aperture.setter
    def aperture(self, value: float) -> None:
        assert isinstance(value, float)
        self._semi_diam.params[0] = max(0.0, value)

    @property
    def curvature(self):
        return self._semi_diam.params[0]

    @curvature.setter
    def curvature(self, value: float) -> None:
        assert isinstance(value, float)
        self._curvature.params[0] = value

    def _parce(self, surface: Dict[str, List[str]]):
        for key, value in surface.items():
            if key == "COMM":
                self.comment = value[0]
                continue
            if key == "TYPE":
                self._type = value[0]
                continue
            if key == "CONI":
                self.conic = float(value[0])
                continue
            if key == "DISZ":
                self.dist_z = float(value[0])
                continue
            if key == "PARM":
                self._params.extend([float(v.split(" ")[1])for v in value])
                continue
            if key == "XDAT":
                self._extra_params.extend([float(v.split(" ")[1])for v in value])
                continue
            if key == "SCBD":
                self._transforms.append(ZSurfaceTransform(value[0]))
                continue
            if key == "GLAS":
                self._material = ZFileField(key + " " + value[0])
                continue
            if key == "DIAM":
                self._semi_diam = ZFileField(key + " " + value[0])
                continue
            if key == "CURV":
                self._curvature = ZFileField(key + " " + value[0])
                continue
            self._others.append(ZFileField(key + " " + value[0]))

    def convert_to_even_aspheric(self, even_aspheric_params: List[float]):
        # PARM 1 - extrapolate
        self._type = 'EVENASPH'
        self._params.clear()
        self._params.append(1.0)
        for index, value in enumerate(even_aspheric_params):
            if index == ZSurface.MAX_EVEN_ASPHERIC_TERM:
                break
            self._params.append(value)

    def convert_to_zernike(self, zernike_params: List[float]):
        # PARM 1 - extrapolate
        # XDAT 1 - Max term
        # XDAT 2 - Norm radius
        self._type = 'SZERNSAG'
        self._extra_params.clear()
        self._extra_params.append(ZSurface.MAX_ZERNIKE_TERM)
        self._extra_params.append(self.aperture)
        for index, value in enumerate(zernike_params):
            if index == ZSurface.MAX_ZERNIKE_TERM:
                break
            self._extra_params.append(value)

    def __str__(self):
        nl = f'{ZSurface.Z_FILE_SURF_INDENT}\n'
        start = ZSurface.Z_FILE_SURF_INDENT
        args = [f"{start}COMM {self.comment}\n" if self.comment != "" else "",
                f"{start}TYPE {self._type}\n",
                f"{start}CONI {self.conic}\n",
                f"{start}DISZ {self.dist_z if self.dist_z != float('inf') else 'INFINITY'}\n",
                f"{start}{self._curvature}\n",
                f"{start}{self._semi_diam}\n",
                f"{start}{self._material}\n" if self._material is not None else "",
                f"{nl.join(f'{start}PARM {i + 1} {_round(v)}' for i, v in enumerate(self._params))}\n"
                if len(self._params) != 0 else "",
                f"{nl.join(f'{start}XDAT {i + 1} {_round(v)}' for i, v in enumerate(self._extra_params))}\n"
                if len(self._extra_params) != 0 else "",
                f"{nl.join(f'{start}{v}' for v in self._transforms)}\n" if len(self._transforms) != 0 else "",
                f"{nl.join(f'{start}{v}' for v in self._others)}\n" if len(self._others) != 0 else ""]
        return ''.join(v for v in args)
