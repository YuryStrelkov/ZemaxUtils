import logging.config
import os.path

from .ray_tracing_common import SOURCE_OBJECT, DUMMY_OBJECT, IMAGE_OBJECT, MATERIAL, GLASS, GLASS_PARAMS, MIRROR
from .ray_tracing_2d import reflect_2d, refract_2d, trace_ray_2d, trace_surface_2d, tracing_2d_test, draw_scheme_2d
from .ray_tracing_2d import build_shape_2d, intersect_flat_surface_2d, intersect_sphere_2d
from .ray_tracing_3d import reflect_3d, refract_3d, trace_ray_3d, trace_surface_3d, tracing_3d_test, draw_scheme_3d
from .ray_tracing_3d import build_shape_3d, intersect_flat_surface_3d, intersect_sphere_3d

loggers = logging.getLogger(__name__)
# Create the Handler for logging data to a file
filename = os.path.join(os.path.dirname(__file__), 'raytracing-log.log')
logger_handler = logging.FileHandler(filename=filename)
logger_handler.setLevel(logging.DEBUG)
# Create a Formatter for formatting the log messages
logger_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
# Add the Formatter to the Handler
logger_handler.setFormatter(logger_formatter)
# Add the Handler to the Logger
loggers.addHandler(logger_handler)
