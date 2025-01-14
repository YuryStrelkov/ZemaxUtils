from Geometry import Transform2d, Vector3, Quaternion, Matrix4
import random
import math
r_amp = 1e-5
accuracy = 1e-5


def bild_rand_basis():
    f = Vector3 (random.uniform(-r_amp, r_amp), random.uniform(-r_amp, r_amp), 1.0).normalized()
    u = Vector3(0, 1, 0)
    r = Vector3.cross(f, u).normalized()
    u = Vector3.cross(r, f).normalized()
    return Matrix4(r.x, u.x, f.x, 0.0,
                   r.y, u.y, f.y, 0.0,
                   r.z, u.z, f.z, 0.0,
                   0.0, 0.0, 0.0, 1.0)


def bild_basis(r: Vector3, u: Vector3, f: Vector3, orig: Vector3 = None):
    f_r = abs(Vector3.dot(f, r))
    if f_r > accuracy:
        print(f'abs(Vector3.dot(f, r)) = {f_r} > {accuracy}')
        return Matrix4.identity() if orig is None else Matrix4(1.0, 0.0, 0.0, orig.x,
                                                               0.0, 1.0, 0.0, orig.y,
                                                               0.0, 0.0, 1.0, orig.z,
                                                               0.0, 0.0, 0.0, 1.0)
    r_u = abs(Vector3.dot(r, u))
    if r_u > accuracy:
        print(f'abs(Vector3.dot(r, u)) = {r_u} > {accuracy}')
        return Matrix4.identity() if orig is None else Matrix4(1.0, 0.0, 0.0, orig.x,
                                                               0.0, 1.0, 0.0, orig.y,
                                                               0.0, 0.0, 1.0, orig.z,
                                                               0.0, 0.0, 0.0, 1.0)
    u_f = abs(Vector3.dot(u, f))
    if u_f > accuracy:
        print(f'abs(Vector3.dot(u, f)) = {u_f} > {accuracy}')
        return Matrix4.identity() if orig is None else Matrix4(1.0, 0.0, 0.0, orig.x,
                                                               0.0, 1.0, 0.0, orig.y,
                                                               0.0, 0.0, 1.0, orig.z,
                                                               0.0, 0.0, 0.0, 1.0)
    return Matrix4(r.x, u.x, f.x, 0.0,
                   r.y, u.y, f.y, 0.0,
                   r.z, u.z, f.z, 0.0,
                   0.0, 0.0, 0.0, 1.0) if orig is None else Matrix4(r.x, u.x, f.x, orig.x,
                                                                    r.y, u.y, f.y, orig.y,
                                                                    r.z, u.z, f.z, orig.z,
                                                                    0.0, 0.0, 0.0, 1.0)


def build_star_sensor(ex: Vector3, ey: Vector3, ez: Vector3):
    ex = Vector3(*(math.cos(v / 180 * math.pi) for v in ex)).normalized()
    ey = Vector3(*(math.cos(v / 180 * math.pi) for v in ey)).normalized()
    ez = Vector3(*(math.cos(v / 180 * math.pi) for v in ez)).normalized()
    b = bild_basis(ex, ey, ez)
    q = Quaternion.from_rotation_matrix(basis)
    return q, b


def combine_basis(first: Matrix4, second: Matrix4):
    avg: Matrix4 = 0.5 * (first + second)
    return bild_basis(avg.right, avg.up, avg.front, avg.origin)


telescope_1 = Transform2d()
telescope_1.ay = (90 - 70.5)
print(telescope_1)
print(Quaternion.from_rotation_matrix(telescope_1.transform_matrix))
print()
telescope_2 = Transform2d()
telescope_2.ay = -(90 - 70.5)
print(telescope_2)
print(Quaternion.from_rotation_matrix(telescope_2.transform_matrix))
print()

basis = bild_rand_basis()
print(basis)
print(Quaternion.from_rotation_matrix(basis))

bis = (telescope_1.transform_matrix * basis + telescope_2.transform_matrix * basis).front.normalized()
print(f"bis: {bis}")

print()
print()

q_1, b_1 = build_star_sensor(Vector3(70.8664022, 147.0, 64.21673764),
                             Vector3(37.0, 90.0, 127.0),
                             Vector3(59.68693109, 57.0, 47.94897924))
print(f'q_1: {q_1}')
print(f'basis_1:\n {b_1}')

q_2, b_2 = build_star_sensor(Vector3(109.1335978, 147.0, 64.21673764),
                             Vector3(37.0, 90.0, 53.0),
                             Vector3(120.3130689, 57.0, 47.94897924))
print(f'q_2: {q_2}')
print(f'basis_2:\n {b_2}')

q_3, b_3 = build_star_sensor(Vector3(90.0, 145.0, 125.0),
                             Vector3(180.0, 90.0, 90.0),
                             Vector3(90.0, 55.0, 145.0))
print(f'q_3: {q_3}')
print(f'basis_3:\n {b_3}')

q_4, b_4 = build_star_sensor(Vector3(143.0, 90.0, 127.0),
                             Vector3(109.1335978, 147.0, 64.21673764),
                             Vector3(120.3130689, 57.0, 47.94897924))
print(f'q_4: {q_4}')
print(f'basis_4:\n {b_4}')

b_1_2 = combine_basis(b_1, b_2)
print(f'b_1_2:\n {b_1_2}')

# работает только датчик 1
# работает только датчик 2
# работает только датчик 3
# работает только датчик 4
# работают датчики 1 and 2
# работают датчики 1 and 3
# работают датчики 1 and 4
# работают датчики 2 and 3
# работают датчики 2 and 4
# работают датчики 3 and 4

# print("\nstar_sensor_axis_0")
# basis = bild_basis(bis, star_sensor_axis_0)
# print(basis)
# print(Quaternion.from_rotation_matrix(basis))
#
# print("\nstar_sensor_axis_1")
# basis = bild_basis(bis, star_sensor_axis_1)
# print(basis)
# print(Quaternion.from_rotation_matrix(basis))
#
# print("\nstar_sensor_axis_2")
# basis = bild_basis(bis, star_sensor_axis_2)
# print(basis)
# print(Quaternion.from_rotation_matrix(basis))
#
# print("\nstar_sensor_axis_3")
# basis = bild_basis(bis, star_sensor_axis_3)
# print(basis)
# print(Quaternion.from_rotation_matrix(basis))
