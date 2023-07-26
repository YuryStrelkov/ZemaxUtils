from Geometry import Transform, Vector3, Quaternion, Matrix4
import random
import math
r_amp = 1e-5


def bild_rand_basis():
    f = Vector3 (random.uniform(-r_amp, r_amp), random.uniform(-r_amp, r_amp), 1.0).normalized()
    u = Vector3(0, 1, 0)
    r = Vector3.cross(f, u).normalized()
    u = Vector3.cross(r, f).normalized()
    return Matrix4(r.x, u.x, f.x, 0.0,
                   r.y, u.y, f.y, 0.0,
                   r.z, u.z, f.z, 0.0,
                   0.0, 0.0, 0.0, 1.0)


def bild_basis(f: Vector3, r: Vector3):
    u = Vector3.cross(f, r).normalized()
    r = Vector3.cross(f, u).normalized()
    return Matrix4(r.x, u.x, f.x, 0.0,
                   r.y, u.y, f.y, 0.0,
                   r.z, u.z, f.z, 0.0,
                   0.0, 0.0, 0.0, 1.0)


telescope_1 = Transform()
telescope_1.ay = (90 - 70.5)
print(telescope_1)
print(Quaternion.from_rotation_matrix(telescope_1.transform_matrix))
print()
telescope_2 = Transform()
telescope_2.ay = -(90 - 70.5)
print(telescope_2)
print(Quaternion.from_rotation_matrix(telescope_2.transform_matrix))

print()

star_sensor_1 = Transform()
star_sensor_1.ay = -(90 - 70.5)
star_sensor_1.ay = -(90 - 70.5)

star_sensor_axis_1 = Vector3(*(math.cos(v / 180 *  math.pi) for v in (90.0, 55.0, 145))).normalized()
# print(sum(v ** 2 for v in star_sensor_axis_1))

star_sensor_axis_2 = Vector3(*(math.cos(v / 180 *  math.pi) for v in (120.3131, 57.0, 47.949))).normalized()
# print(sum(v ** 2 for v in star_sensor_axis_2))

star_sensor_axis_3 = Vector3(*(math.cos(v / 180 *  math.pi) for v in (59.6869, 57.0, 47.949))).normalized()
# print(sum(v ** 2 for v in star_sensor_axis_3))

print(star_sensor_axis_1)
print(star_sensor_axis_2)
print(star_sensor_axis_3)

basis = bild_rand_basis()
print(basis)
print(Quaternion.from_rotation_matrix(basis))

bis = ((telescope_1.transform_matrix * basis + telescope_2.transform_matrix * basis).front).normalized()
print(f"bis: {bis}")

print("\nstar_sensor_axis_1")
basis = bild_basis(bis, star_sensor_axis_1)
print(basis)
print(Quaternion.from_rotation_matrix(basis))

print("\nstar_sensor_axis_2")
basis = bild_basis(bis, star_sensor_axis_2)
print(basis)
print(Quaternion.from_rotation_matrix(basis))

print("\nstar_sensor_axis_3")
basis = bild_basis(bis, star_sensor_axis_3)
print(basis)
print(Quaternion.from_rotation_matrix(basis))
