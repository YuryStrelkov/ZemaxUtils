from Geometry import Vector4, Vector2
from matplotlib import pyplot as plt
from typing import Dict, Any, Tuple
from typing import Union


class ResultVisualSettings:
    FONT_FAMILIES = \
        {"Arial",
         "Helvetica",
         "Verdana",
         "Gill Sans",
         "Noto Sans",
         "Avantgarde",
         "Optima",
         "Arial Narrow",
         "Times",
         "Times New Roman",
         "Didot",
         "Georgia",
         "Palatino",
         "Bookman",
         "New Century Schoolbook",
         "American Typewriter",
         "Andale Mono",
         "Courier New",
         "Courier",
         "FreeMono",
         "OCR A Std",
         "DejaVu Sans Mono",
         "Comic Sans MS",
         "Comic Sans",
         "Apple Chancery",
         "Bradley Hand",
         "Brush Script MT",
         "Brush Script Std",
         "Snell Roundhand",
         "URW Chancery L",
         "Impact",
         "Luminari",
         "Chalkduster",
         "Jazz LET",
         "Blippo",
         "Stencil Std",
         "Marker Felt",
         "Trattatello"}

    UNITS_SCALES = \
        {
            "mm": 0.1,
            "MM": 0.1,
            "cm": 1.0,
            "CM": 1.0,
            "dm": 10.0,
            "DM": 10.0,
            "m": 100.0,
            "M": 100.0,
            "in": 2.54,
            "IN": 2.54
        }

    def __init__(self):
        self._units:        str = "cm"
        self._frame_width:  int = 17
        self._frame_height: int = 10
        self._font_size:    int = 10
        self._font_family:  str = "Times New Roman"
        self._plots_x:      int = 1
        self._plots_y:      int = 1
        self._bounds: Vector4 = Vector4(0.1, 0.1, 0.98, 0.98)
        self._spacing: Vector2 = Vector2(0.1, 0.1)

    @property
    def adjustment_args(self) -> Tuple[float, float, float, float, float, float]:
        return self._bounds.x, self._bounds.y, self._bounds.z, self._bounds.w, self._spacing.x, self._spacing.y

    @property
    def w_space(self) -> float:
        return self._spacing.x

    @w_space.setter
    def w_space(self, value: float) -> None:
        assert isinstance(value, float)
        self._spacing = Vector2(min(max(value, 0.0), 1.0), self._bounds.y)

    @property
    def h_space(self) -> float:
        return self._spacing.y

    @h_space.setter
    def h_space(self, value: float) -> None:
        assert isinstance(value, float)
        self._spacing = Vector2(self._bounds.y, min(max(value, 0.0), 1.0))

    @property
    def left(self) -> float:
        return self._bounds.x

    @left.setter
    def left(self, value: float) -> None:
        assert isinstance(value, float)
        self._bounds = Vector4(min(max(value, 0.0), 1.0), self._bounds.y, self._bounds.z, self._bounds.w)

    @property
    def bottom(self) -> float:
        return self._bounds.y

    @bottom.setter
    def bottom(self, value: float) -> None:
        assert isinstance(value, float)
        self._bounds = Vector4(self._bounds.x, min(max(value, 0.0), 1.0),  self._bounds.z, self._bounds.w)

    @property
    def right(self) -> float:
        return self._bounds.z

    @right.setter
    def right(self, value: float) -> None:
        assert isinstance(value, float)
        self._bounds = Vector4(self._bounds.x, self._bounds.y, min(max(value, 0.0), 1.0), self._bounds.w)

    @property
    def top(self) -> float:
        return self._bounds.w

    @top.setter
    def top(self, value: float) -> None:
        assert isinstance(value, float)
        self._bounds = Vector4(self._bounds.x, self._bounds.y, self._bounds.z, min(max(value, 0.0), 1.0))

    @property
    def bounds(self) -> Vector4:
        return self._bounds

    @bounds.setter
    def bounds(self, value: Union[Vector4, Tuple[float, float, float, float]]) -> None:
        if isinstance(value, Vector4):
            self._bounds = Vector4(min(max(value.x, 0.0), 1.0),
                                   min(max(value.y, 0.0), 1.0),
                                   min(max(value.z, 0.0), 1.0),
                                   min(max(value.w, 0.0), 1.0))
        if isinstance(value, tuple):
            assert len(value) == 4
            self._bounds = Vector4(min(max(value[0], 0.0), 1.0),
                                   min(max(value[1], 0.0), 1.0),
                                   min(max(value[2], 0.0), 1.0),
                                   min(max(value[3], 0.0), 1.0))

    @property
    def size(self) -> Tuple[float, float]:
        return self.width, self.height

    @property
    def inch_size(self) -> Tuple[float, float]:
        return self.width / 2.54, self.height / 2.54

    @property
    def has_subplots(self):
        return self._plots_x != 1 or self._plots_y != 1

    @property
    def subplots(self) -> Tuple[int, int]:
        return self._plots_x, self._plots_y

    @subplots.setter
    def subplots(self, value: Tuple[int, int]) -> None:
        assert len(value) == 2
        self.x_subplots = value[0]
        self.y_subplots = value[1]

    @property
    def subplots_count(self) -> int:
        return self._plots_x * self._plots_y

    @property
    def x_subplots(self) -> int:
        return self._plots_x

    @property
    def y_subplots(self) -> int:
        return self._plots_x

    @x_subplots.setter
    def x_subplots(self, value: int) -> None:
        assert isinstance(value, int)
        self._plots_x = max(1, value)

    @y_subplots.setter
    def y_subplots(self, value: int) -> None:
        assert isinstance(value, int)
        self._plots_y = max(1, value)

    @property
    def font(self) -> Dict[str, Any]:
        return {'font.family': self._font_family, 'font.size': self._font_size}

    @property
    def units_scale(self) -> float:
        return ResultVisualSettings.UNITS_SCALES[self._units]

    @property
    def units(self) -> str:
        return self._units

    @units.setter
    def units(self, value: str) -> None:
        assert isinstance(value, str)
        if value not in ResultVisualSettings.UNITS_SCALES:
            return
        self._units = ResultVisualSettings.UNITS_SCALES[value]

    @property
    def font_family(self) -> str:
        return self._font_family

    @font_family.setter
    def font_family(self, value: str) -> None:
        assert isinstance(value, str)
        if value not in ResultVisualSettings.FONT_FAMILIES:
            return
        self._font_family = value

    @property
    def font_size(self) -> float:
        return self._font_size

    @font_size.setter
    def font_size(self, value: float) -> None:
        assert isinstance(value, float) or isinstance(value, int)
        self._font_size = abs(value)

    @property
    def width(self) -> float:
        return self._frame_width * self.units_scale

    @width.setter
    def width(self, value: float) -> None:
        assert isinstance(value, float) or isinstance(value, int)
        self._frame_width = abs(value) / self.units_scale

    @property
    def height(self) -> float:
        return self._frame_height * self.units_scale

    @height.setter
    def height(self, value: float) -> None:
        assert isinstance(value, float) or isinstance(value, int)
        self._frame_height = abs(value) / self.units_scale

    def build_figure(self):
        fig, axes = plt.subplots(*self.subplots, figsize=self.inch_size)
        fig.tight_layout()
        fig.subplots_adjust(left=self.left,
                            bottom=self.bottom,
                            right=self.right,
                            top=self.top,
                            wspace=self.w_space,
                            hspace=self.h_space)
        plt.rcParams.update(self.font)
        # for k in plt.rcParams:
        #     print(k)

        return fig, axes
