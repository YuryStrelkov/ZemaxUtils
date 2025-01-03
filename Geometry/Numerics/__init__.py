import logging.config
import os.path

from .mutils import dec_to_rad, rad_to_dec, compute_derivatives_2_at_pt, compute_derivatives_at_pt
from .mutils import linear_regression, bi_linear_regression, n_linear_regression
from .mutils import compute_derivatives_2, compute_derivatives, compute_normals
from .mutils import square_equation, clamp, dec_to_rad_pt, rad_to_dec_pt
from .mutils import second_order_surface, quadratic_shape_fit
from .mutils import poly_regression, quadratic_regression_2d
from .mutils import poly_fit, polynom, quadratic_shape_fit
from .fourier import fft, fft_2d, ifft, ifft_2d
from .interpolators import bi_linear_cut_along_curve, bi_cubic_interp_derivatives_pt, bi_cubic_interp_derivatives2_pt
from .interpolators import bi_cubic_interp_derivatives, bi_cubic_interp_derivatives2, bi_qubic_interp, bi_qubic_cut
from .interpolators import bi_linear_interp_derivatives2_pt, bi_linear_interp_derivatives, bi_qubic_cut_along_curve
from .interpolators import bi_linear_interp_derivatives2, bi_linear_interp, bi_linear_cut
from .interpolators import bi_linear_interp_pt, bi_linear_interp_derivatives_pt

loggers = logging.getLogger(__name__)
# Create the Handler for logging data to a file
filename = os.path.join(os.path.dirname(__file__), 'mutils-log.log')
logger_handler = logging.FileHandler(filename=filename)
logger_handler.setLevel(logging.DEBUG)
# Create a Formatter for formatting the log messages
logger_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
# Add the Formatter to the Handler
logger_handler.setFormatter(logger_formatter)
# Add the Handler to the Logger
loggers.addHandler(logger_handler)
