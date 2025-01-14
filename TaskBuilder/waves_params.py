import dataclasses
from typing import Tuple


@dataclasses.dataclass(frozen=True)
class Wave:
    KEYS = ("lam", "weight")
    lam: float
    weight: float
    """Параметры одной длины волны для файла настроек"""
    @classmethod
    def create(cls, lam: float = 0.55, weight: float = 1.0) -> 'Wave':
        return cls(lam, weight)

    def __iter__(self):
        yield "lam", self.lam
        yield "weight", self.weight

    def __str__(self):
        return f"{{ \"lam\" : {self.lam}, \"weight\" : {self.weight} }}"


def read_waves(json_node) -> Tuple[Wave, ...]:
    if 'waves' not in json_node:
        return ()
    return tuple(Wave(*tuple((float(wave[k]) if k in wave else 0.0 for k in Wave.KEYS))) for wave in json_node['waves'])
