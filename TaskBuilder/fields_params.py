from typing import List, Tuple, Union, Dict, Any
import dataclasses


@dataclasses.dataclass(frozen=True)
class Field:
    KEYS = ("angle_x", "angle_y", "weight", "vdx", "vdy", "vcx", "vcy", "van")
    """Параметры одного поля для файла настроек"""
    angle_x: float
    angle_y: float
    weight: float
    vdx: float
    vdy: float
    vcx: float
    vcy: float
    van: float

    @classmethod
    def create(cls, angle_x: float = 0.0, angle_y: float = 0.0, weight: float = 1.0,
               vdx: float = 0.0, vdy: float = 0.0, vcx: float = 0.0, vcy: float = 0.0, van: float = 0.0):
        return cls(angle_x, angle_y, weight, vdx, vdy, vcx, vcy, van)

    def __iter__(self):
        yield "angle_x", self.angle_x
        yield "angle_y", self.angle_y
        yield "weight", self.weight
        yield "vdx", self.vdx
        yield "vdy", self.vdy
        yield "vcx", self.vcx
        yield "vcy", self.vcy
        yield "van", self.van

    @property
    def to_list(self) -> List[float]:
        return [v for _, v in self]

    def __str__(self):
        raw = ",\n".join(f"\"{k}\": {v}" for k, v in self)
        return f"{{\n{raw}\n}}"


@dataclasses.dataclass(frozen=True)
class FieldsParams:
    """Параметры полей для файла настроек"""
    fields_type: int
    fields: Tuple[Field, ...]

    @classmethod
    def create(cls, fields_type: int = 0, fields: Tuple[Field, ...] = None):
        return cls(fields_type, fields)

    def __str__(self):
        if self.fields is None:
            return f"\t\t{{" \
                   f"\t\t\t\"fields_type\" : {self.fields_type},\n" \
                   f"\t\t\t\"fields\" : []\n" \
                   f"\n\t\t}}"
        sep = '\n\t\t\t\t'
        return f"\t\t{{" \
               f"\t\t\t\"fields_type\" : {self.fields_type},\n" \
               f"\t\t\t\"fields\" : [\n{sep.join(str(v) for v in self.fields)}]\n" \
               f"\n\t\t}}"


def load_fields_params(json_node: Dict[str, Any]) -> Union['FieldsParams', None]:
    if 'fields' not in json_node:
        return None
    fields = json_node['fields']
    fields_type = int(fields['fields_type']) if 'fields_type' in fields else 0
    fields_params = tuple(Field(*tuple(v[k] if k in v else 0.0 for k in Field.KEYS)) for v in fields['fields'])
    return FieldsParams(fields_type, fields_params)
