"""
Base geometry primitives library
"""
__version__ = '0.1.25'
__license__ = "GNU Lesser General Public License v3"
from .perspective_transform_2d import PerspectiveTransform2d, perspective_transform_test
from .transform_3d import Transform3d, deg_to_rad, transform_3d_test
from .transform_2d import Transform2d, transform_2d_test
from .bounding_box import BoundingBox
from .march_squares import march_squares_2d
from .quaternion import Quaternion, quaternion_4_test
from .vector4 import Vector4, vector_4_test
from .vector3 import Vector3, vector_3_test
from .vector2 import Vector2, vector_2_test
from .matrix4 import Matrix4, matrix_4_test
from .matrix3 import Matrix3, matrix_3_test
from .camera import Camera
from .plane import Plane
from .ray import Ray
from .common import *
from .mutils import linear_regression
from .mutils import bi_linear_regression
from .mutils import polynom
from .mutils import poly_regression
from .mutils import poly_fit
from .mutils import n_linear_regression
from .mutils import quadratic_regression_2d
from .mutils import second_order_surface
from .mutils import quadratic_shape_fit
