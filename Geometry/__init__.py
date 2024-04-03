"""
Base geometry primitives library
"""
__version__ = '0.1.25'
__license__ = "GNU Lesser General Public License v3"
from .common import NUMERICAL_MAX_VALUE, NUMERICAL_MIN_VALUE, PI, TWO_PI, HALF_PI
from .common import NUMERICAL_ACCURACY, NUMERICAL_FORMAT_4F, NUMERICAL_FORMAT_8F
from .common import DEG_TO_RAD, RAD_TO_DEG
from .perspective_transform_2d import PerspectiveTransform2d, perspective_transform_test
from .transform_3d import Transform3d, deg_to_rad, transform_3d_test
from .transform_2d import Transform2d, transform_2d_test
from .bounding_rect import BoundingRect
from .bounding_box import BoundingBox
from .quaternion import Quaternion, quaternion_4_test
from .vector4 import Vector4, vector_4_test
from .vector3 import Vector3, vector_3_test
from .vector2 import Vector2, vector_2_test
from .matrix4 import Matrix4, matrix_4_test
from .matrix3 import Matrix3, matrix_3_test
from .camera import Camera
from .plane import Plane
from .ray import Ray
from .mutils import linear_regression, bi_linear_regression, n_linear_regression
from .mutils import second_order_surface, quadratic_shape_fit
from .mutils import poly_regression, quadratic_regression_2d
from .mutils import poly_fit, polynom, quadratic_shape_fit
from .raytracing import draw_scheme_2d, trace_ray_2d, trace_ray, send_trace_log_2d, send_draw_log_2d,\
    send_io_log_2d, trace_log_2d, draw_log_2d, io_log_2d
