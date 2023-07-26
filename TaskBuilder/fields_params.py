from collections import namedtuple
from typing import List


class Field(namedtuple('Field', 'angle_x, angle_y, weight, vdx, vdy, vcx, vcy, van')):
    """Параметры одного поля для файла настроек"""
    __slots__ = ()

    def __new__(cls, angle_x: float = 0.0, angle_y: float = 0.0, weight: float = 1.0,
                vdx: float = 0.0, vdy: float = 0.0, vcx: float = 0.0, vcy: float = 0.0, van: float = 0.0):
        return super().__new__(cls, angle_x, angle_y, weight, vdx, vdy, vcx, vcy, van)

    def __str__(self):
        return f"{{ \"angle_x\" : {self.angle_x}, " \
               f"\"angle_y\" : {self.angle_x}, " \
               f"\"weight\" : {self.angle_x}, " \
               f"\"vdx\" : {self.angle_x}, " \
               f"\"vdy\" : {self.angle_x}, " \
               f"\"vcx\" : {self.angle_x}, " \
               f"\"vcy\" : {self.angle_x}, " \
               f"\"van\" : {self.angle_x}}}"


class FieldsParams(namedtuple('FieldsParams', 'fields_type, fields')):
    """Параметры полей для файла настроек"""
    __slots__ = ()

    def __new__(cls, fields_type: int = 0, fields: List[Field] = None):
        return super().__new__(cls, fields_type, fields)

    def __str__(self):
        if self.fields is None:
            return f"\t\t{{" \
                   f"\t\t\t\"fields_type\" : {self.fields_type},\n" \
                   f"\t\t\t\"fields\" : []\n" \
                   f"\n\t\t}}"
        sep = '\n\t\t\t\t'
        return f"\t\t{{" \
               f"\t\t\t\"fields_type\" : {self.fields_type},\n" \
               f"\t\t\t\"fields\" : [\n{sep.join(v for v in self.fields)}]\n" \
               f"\n\t\t}}"


def load_fields_params(json_node):
    if 'fields' not in json_node:
        return None
    fields = json_node['fields']
    fields_type = int(fields['fields_type']) if 'fields_type' in fields else 0
    fields_params = []
    for v in fields['fields']:
        fields_params.append(Field(float(v['angle_x']) if 'angle_x' in v else 0.0,
                                   float(v['angle_y']) if 'angle_y' in v else 0.0,
                                   float(v['weight']) if 'weight' in v else 1.0,
                                   float(v['vdx']) if 'vdx' in v else 0.0,
                                   float(v['vdy']) if 'vdy' in v else 0.0,
                                   float(v['vcx']) if 'vcx' in v else 0.0,
                                   float(v['vcy']) if 'vcy' in v else 0.0,
                                   float(v['van']) if 'van' in v else 0.0))

    return FieldsParams(fields_type, fields_params)
