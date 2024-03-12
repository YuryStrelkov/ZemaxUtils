from collections import namedtuple


class Wave(namedtuple('Wave', 'lam, weight')):
    """Параметры одной длины волны для файла настроек"""
    __slots__ = ()

    def __new__(cls, lam: float = 0.55, weight: float = 1.0):
        return super().__new__(cls, lam, weight)

    def __iter__(self):
        yield "lam", self.lam
        yield "weight", self.weight

    def __str__(self):
        return f"{{ \"lam\" : {self.lam}, \"weight\" : {self.weight} }}"


def read_waves(json_node):
    if 'waves' not in json_node:
        return None
    waves = json_node['waves']
    return [Wave(float(v['lam']) if 'lam' in v else 0.55,
                 float(v['weight']) if 'weight' in v else 0.0) for v in waves]
