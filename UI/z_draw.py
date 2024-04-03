import matplotlib.pyplot as plt
from Geometry import Vector2, Transform2d, draw_scheme_2d, trace_ray_2d, send_io_log_2d,\
    trace_log_2d, draw_log_2d, io_log_2d
from ZFile import ZFile


def convert_zemax_file_to_tracer_task(z_file: ZFile):
    surfaces = iter(z_file.surfaces.values())
    surfaces_r = []
    aperture_a = []
    surfaces_t = []
    surfaces_p = []
    z_distances = [z_file.get_dist_z(index) for index in z_file.surfaces.keys()]
    z_distances[0] = 0.0
    z_distances.insert(0, 0)
    for i in range(2, len(z_distances)):
        z_distances[i] += z_distances[i - 1]
    z_distances = iter(z_distances)
    while True:
        try:
            s1 = next(surfaces)
            z1 = next(z_distances)
            if not s1.material:
                surfaces_r.append(-1.0 / s1.curvature if abs(s1.curvature) > 1e-9 else 1e6)
                aperture_a.append(s1.aperture if not isinstance(s1.aperture, tuple) else s1.aperture[-1])
                surfaces_t.append(Transform2d(pos=Vector2(z1, 0.0), angle=90.0))
                surfaces_p.append({'material': 'dummy'})
                continue
            if s1.material.params[0] == 'MIRROR':
                surfaces_r.append(-1.0 / s1.curvature if abs(s1.curvature) > 1e-9 else 1e6)
                aperture_a.append(s1.aperture if not isinstance(s1.aperture, tuple) else s1.aperture[-1])
                surfaces_t.append(Transform2d(pos=Vector2(z1, 0.0), angle=90.0))
                surfaces_p.append({'material': 'mirror'})
                continue
            try:
                ri = float(s1.material.params[3])
                ri = ri if abs(ri) > 1.0 else 1.0
            except IndexError | ValueError as error:
                send_io_log_2d(f"\tparce-error : error while parsing surface material params, "
                               f"default value of \"refraction index\" will be assigned\n"
                               f"\terror-info : {error}")
                ri = 1.333
            surfaces_r.append(-1.0 / s1.curvature if abs(s1.curvature) > 1e-9 else 1e6)
            aperture_a.append(s1.aperture if not isinstance(s1.aperture, tuple) else s1.aperture[-1])
            surfaces_t.append(Transform2d(pos=Vector2(z1, 0.0), angle=90.0))
            surfaces_p.append({'material': 'glass', 'glass-params': (1.0, ri)})
            s1 = next(surfaces)
            z1 = next(z_distances)
            surfaces_r.append(-1.0 / s1.curvature if abs(s1.curvature) > 1e-9 else 1e6)
            aperture_a.append(s1.aperture if not isinstance(s1.aperture, tuple) else s1.aperture[-1])
            surfaces_t.append(Transform2d(pos=Vector2(z1, 0.0), angle=90.0))
            surfaces_p.append({'material': 'glass', 'glass-params': (ri, 1.0)})
            continue
        except StopIteration:
            send_io_log_2d(f"\tparce-info  : file: \"{z_file.name.params[0]}\""
                           f" successfully parsed and redy to trace and draw...")
            break
    surfaces_p[0]['material'] = 'object'
    aperture_a[0] = max(aperture_a[0], aperture_a[1])
    surfaces_p[-1]['material'] = 'image'
    return surfaces_r, aperture_a, surfaces_t, surfaces_p


def render_scheme_preview(scheme, axis=None):
    axis = axis if axis else plt.gca()
    surfaces_r, aperture_a, surfaces_t, surfaces_p = convert_zemax_file_to_tracer_task(scheme)

    da = aperture_a[0] / 30 * 1.333

    for i in range(-15, 16):
        positions, directions = trace_ray_2d(Vector2(1, 0), Vector2(-2, i * da), surfaces_r, surfaces_t, surfaces_p)
        xs = [v.x for v in positions]
        ys = [v.y for v in positions]
        axis.plot(xs, ys, 'r', linewidth=0.75)
    draw_scheme_2d(surfaces_r, aperture_a, surfaces_t, surfaces_p, axis=axis)
    for message in io_log_2d():
        print(message)
    for message in trace_log_2d():
        print(message)
    for message in draw_log_2d():
        print(message)


def test(scheme):
    render_scheme_preview(scheme, plt.gca())
    plt.show()
