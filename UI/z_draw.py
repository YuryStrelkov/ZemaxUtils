import math
from typing import Tuple, List
import matplotlib.pyplot as plt

from Geometry import Vector2


def intersect_sphere(direction: Vector2, origin: Vector2, radius: float, position: Vector2) -> float:
    b = Vector2.dot(origin - position, direction)
    d = b ** 2 + Vector2.dot(origin - position, origin - position) + radius ** 2
    if d < 0:
        return -1.0
    d = math.sqrt(d)
    t1, t2 = b + d, b - d
    if radius > 0:
        if t1 * t2 < 0:
            return t1 if t1 > 0 else t2
        return min(t1, t2)
    else:
        if t1 * t2 < 0:
            return t1 if t1 > 0 else t2
        return max(t1, t2)


def intersect_surface(direction: Vector2, origin: Vector2, position: Vector2, normal: Vector2) -> float:
    rn = Vector2.dot(origin, normal)
    en = Vector2.dot(direction, normal)
    return (rn - Vector2.dot(position, direction)) / en


def transform_ray(direction: Vector2, origin: Vector2, position: Vector2 = None, angle: float = 0.0):
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    rd = Vector2( cos_a * direction.x + sin_a * direction.y,
                 -sin_a * direction.x + cos_a * direction.y)
    if position is None:
        ro = Vector2( cos_a * origin.x + sin_a * origin.y,
                     -sin_a * origin.x + cos_a * origin.y)
        return rd, ro
    ro = Vector2( cos_a * origin.x + sin_a * origin.y - (cos_a * position.x - sin_a * position.y),
                 -sin_a * origin.x + cos_a * origin.y - (sin_a * position.x + cos_a * position.y))
    return rd, ro


def trace_sphere(direction: Vector2, origin: Vector2, radius: float,
                 position: Vector2 = None, angle: float = 0.0) -> float:
    rd, ro = transform_ray(direction, origin, position, angle)
    return intersect_sphere(rd, ro, radius, Vector2(0, 0))


def trace_lens(rd: Vector2, ro: Vector2, p0: Vector2, r1: float, r2: float, sd: float, a: float):
    t1 = trace_sphere(rd, ro, r1, p0, a)
    ro1 = rd * t1 + ro
    rn = (ro1 - p0).normalized
    rd1 = Vector2.refract(rd, rn, 1.0, 1.333)
    p1 =  p0 + Vector2(-sd *  math.sin(a), sd * math.cos(a))
    t2 = trace_sphere(rd1, ro1, r2, p1, a)
    ro2 = rd1 * t2 + ro1
    rn1 = (ro2 - p1).normalized
    rd2 = Vector2.refract(rd1, rn1, 1.333, 1.0)
    return (ro1, rd1), (ro2, rd2)


def build_shape(radius: float, semi_diam: float, steps: int = 16,
                pos: Vector2 = None, angle: float = 0.0) -> Tuple[List[float], List[float]]:
    if abs(semi_diam) < 1e-9:
        return [], []
    if abs(radius) < 1e-9:
        xs, ys = [-semi_diam, semi_diam], [0, 0]
    else:
        da = 2 * semi_diam / (steps - 1)
        xs = [da * i - semi_diam for i in range(steps)]
        sgn = -1.0 if radius > 0 else 1.0
        ys = [-radius - sgn * math.sqrt((radius * radius - x * x)) for x in xs]

    sin_a = math.sin(angle)
    cos_a = math.cos(angle)
    x0, y0 = (pos.x, pos.y) if pos else (0, 0)
    for index, (xi, yi) in enumerate(zip(xs, ys)):
        xs[index] = xi * cos_a - yi * sin_a + x0
        ys[index] = xi * sin_a + yi * cos_a + y0
    return xs, ys


def lens_shape(r1: float, r2: float, s_dia1: float, s_dia2: float, thickness: float,
               pos: Vector2 = None, angle: float = 0.0) -> Tuple[List[float], List[float]]:
    s_dia = max(s_dia1, s_dia2)
    xs, ys = build_shape(r1, s_dia, pos=pos, angle=angle)
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)
    pos1 = Vector2(pos.x - thickness * sin_a, pos.y + thickness * cos_a) if pos else\
           Vector2(-thickness * sin_a, thickness * cos_a)
    xs1, ys1 = build_shape(r2, s_dia, pos=pos1, angle=angle)
    xs1.reverse()
    ys1.reverse()
    xs.extend(xs1)
    ys.extend(ys1)
    xs.append(xs[0])
    ys.append(ys[0])
    return xs, ys


def create_z_surfaces(z_file, angle: float = 0.0):
    surfaces = iter(z_file.surfaces.values())
    z_distances = [z_file.get_dist_z(index) for index in z_file.surfaces.keys()]
    z_distances[0] = 0.0
    z_distances.insert(0, 0)
    for i in range(2, len(z_distances)):
        z_distances[i] += z_distances[i - 1]
    z_distances = iter(z_distances)
    surfaces_x = []
    surfaces_y = []
    is_lens = []
    while True:
        try:
            s1 = next(surfaces)
            z1 = next(z_distances)
            if not s1.material:
                is_lens.append(0)
                x, y = build_shape(1.0 / s1.curvature if abs(s1.curvature) > 1e-9 else 0.0,
                                   s1.aperture if not isinstance(s1.aperture, tuple) else s1.aperture[-1],
                                   pos=Vector2(z1 * math.cos(angle),  z1 * math.sin(angle)), angle=angle)
                surfaces_x.append(x)
                surfaces_y.append(y)
                continue
            if s1.material.params[0] == 'MIRROR':
                is_lens.append(1)
                x, y = build_shape(1.0 / s1.curvature if abs(s1.curvature) > 1e-9 else 0.0,
                                   s1.aperture if not isinstance(s1.aperture, tuple) else s1.aperture[-1],
                                   pos=Vector2(z1 * math.cos(angle),  z1 * math.sin(angle)), angle=angle)
                surfaces_x.append(x)
                surfaces_y.append(y)
                continue
            is_lens.append(2)
            s2 = next(surfaces)
            z2 = next(z_distances)
            x, y = lens_shape(1.0 / s1.curvature if abs(s1.curvature) > 1e-9 else 0.0,
                              1.0 / s2.curvature if abs(s2.curvature) > 1e-9 else 0.0,
                              s1.aperture if not isinstance(s1.aperture, tuple) else s1.aperture[-1],
                              s2.aperture if not isinstance(s2.aperture, tuple) else s2.aperture[-1],
                              z2 - z1, pos=Vector2(z1 * math.cos(angle),  z1 * math.sin(angle)), angle=angle)
            surfaces_x.append(x)
            surfaces_y.append(y)
        except StopIteration as stop:
            break
    return surfaces_x, surfaces_y, is_lens


def test(scheme):
    # scheme = ZFile()
    # scheme.load("ZemaxSchemes/F_07g_04_Blenda_PI_Fin.ZMX")
    sx, sy, is_lens = create_z_surfaces(scheme)
    # xl, yl = lens_shape(100, -100, 20, 20, 5, pos=(0, 10), angle=math.pi * 0.25)
    # x1, y1 = build_shape(100,  20, pos=(0, -10)) #, angle=math.pi * 0.25)
    # x2, y2 = build_shape(-100,  20)
    # plt.plot(0, 10, '*k')
    # plt.plot(x1, y1, 'k')
    # plt.plot(x2, y2, 'r')
    for x, y, s_type in zip(sx, sy, is_lens):
        if s_type == 0:
            plt.plot(x, y, '--k')
        if s_type == 1:
            plt.plot(x, y, 'k')
        if s_type == 2:
            plt.plot(x, y, 'b')
    plt.gca().set_aspect('equal', 'box')
    plt.show()
