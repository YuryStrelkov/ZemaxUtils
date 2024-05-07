from Geometry import poly_regression, poly_fit, linear_regression
from ResultBuilder import ResultFile, ResultVisualSettings
import matplotlib.pyplot as plt
import numpy as np
# разница смещений в плоскости изображения между real и deformed от PSF
# разница смещений в плоскости изображения между real и deformed от SPOT
# зависимость изменения угла от изменения положения на изображении для PSF
# зависимость изменения угла от изменения положения на изображении для SPOT
# усреднённая зависимость изменения угла от изменения положения на изображении для PSF
# усреднённая зависимость изменения угла от изменения положения на изображении для SPOT
font = {'family' : 'Times New Roman',
        'size'   : 12}

plt.rc('font', **font)

INCH_TO_CM = 1 / 2.54
WIDTH_SIZE = 17 * INCH_TO_CM
HEIGHT_SIZE = 17 * INCH_TO_CM


def psf_difference(scheme_real: ResultFile, scheme_deformed: ResultFile, spot_or_psf: bool = True,
                   avg: bool = False, inv: bool = False):
    psf_real     = scheme_real.y_image_pos_per_angle if spot_or_psf else scheme_real.y_image_pos_per_angle_from_psf
    psf_deformed = scheme_deformed.y_image_pos_per_angle\
        if spot_or_psf else scheme_deformed.y_image_pos_per_angle_from_psf
    difference =  [np.array([s - p for s, p in zip(si, pi)])for si, pi in zip(psf_deformed, psf_real)]
    ya = scheme_deformed.y_angles
    angles = np.linspace(ya[0], ya[-1], 128)
    fig, axes = plt.subplots(figsize=(WIDTH_SIZE, HEIGHT_SIZE))
    fig.subplots_adjust(left=0.075,
                        bottom=0.075,
                        right=0.925,
                        top=0.925,
                        wspace=0.25,
                        hspace=0.25)

    if inv:
        axes.set_ylabel("y - ang, [deg]")
        axes.set_xlabel("x, [$\mu$M]")
        if avg:
            legend = [f"avg"]
            scale = 1.0 / len(difference)
            difference_avg = np.array([scale * sum(i for i in v) for v in zip(*difference)])
            plt.plot(poly_fit(angles, ya, difference_avg, 5) * 1000, angles, 'k', linewidth=2)
        else:
            legend = []
            for val, wl in zip(difference, scheme_real.wavelengths):
                plt.plot(poly_fit(angles, ya, val, 5) * 1000, angles, linewidth=0.75)
                legend.append(f"lam = {str(wl):5>}, $\mu$M")
            legend.append(f"avg")
            scale = 1.0 / len(difference)
            difference_avg = np.array([scale * sum(i for i in v) for v in zip(*difference)])
            plt.plot(poly_fit(angles, ya, difference_avg, 5) * 1000, angles, 'k', linewidth=2)
    else:
        axes.set_xlabel("x - ang, [deg]")
        axes.set_ylabel("y, [$\mu$M]")
        if avg:
            legend = [f"avg"]
            scale = 1.0 / len(difference)
            difference_avg = np.array([scale * sum(i for i in v) for v in zip(*difference)])
            plt.plot(angles, poly_fit(angles, ya, difference_avg, 5) * 1000, 'k', linewidth=2)
        else:
            legend = []
            for val, wl in zip(difference, scheme_real.wavelengths):
                plt.plot(angles, poly_fit(angles, ya, val, 5) * 1000, linewidth=0.75)
                legend.append(f"lam = {str(wl):5>}, $\mu$M")
            legend.append(f"avg")
            scale = 1.0 / len(difference)
            difference_avg = np.array([scale * sum(i for i in v) for v in zip(*difference)])
            plt.plot(angles, poly_fit(angles, ya, difference_avg, 5) * 1000, 'k', linewidth=2)
    axes.grid(True)
    axes.legend(legend, loc=2)
    # plt.show()
    return fig


def psf_difference_div(scheme_real: ResultFile, scheme_deformed: ResultFile, spot_or_psf: bool = True,
                   avg: bool = False, inv: bool = False):
    psf_real     = scheme_real.y_image_pos_per_angle if spot_or_psf else scheme_real.y_image_pos_per_angle_from_psf
    psf_deformed = scheme_deformed.y_image_pos_per_angle\
        if spot_or_psf else scheme_deformed.y_image_pos_per_angle_from_psf
    difference =  [np.array([s - p for s, p in zip(si, pi)])for si, pi in zip(psf_deformed, psf_real)]
    ya = scheme_deformed.y_angles
    angles = np.linspace(ya[0], ya[-1], 128)
    d_y = 1.0 / (angles[1] - angles[0])
    fig, axes = plt.subplots(figsize=(WIDTH_SIZE, HEIGHT_SIZE))
    fig.subplots_adjust(left=0.075,
                        bottom=0.075,
                        right=0.925,
                        top=0.925,
                        wspace=0.25,
                        hspace=0.25)

    if inv:
        axes.set_ylabel("y - ang, [deg]")
        axes.set_xlabel("x, [$\mu$M]")
        if avg:
            legend = [f"avg"]
            scale = 1.0 / len(difference)
            difference_avg = np.array([scale * sum(i for i in v) for v in zip(*difference)])
            values = poly_fit(angles, ya, difference_avg, 5)
            plt.plot((values[1:] - values[:-1]) * d_y * 1000, angles[:-1], 'k', linewidth=2)
        else:
            legend = []
            for val, wl in zip(difference, scheme_real.wavelengths):
                values = poly_fit(angles, ya, val, 5)
                plt.plot((values[1:] - values[:-1]) * d_y * 1000, angles[:-1], linewidth=0.75)
                legend.append(f"lam = {str(wl):5>}, $\mu$M")
            legend.append(f"avg")
            scale = 1.0 / len(difference)
            difference_avg = poly_fit(angles, ya, np.array([scale * sum(i for i in v) for v in zip(*difference)]), 5)
            plt.plot((difference_avg[1:] - difference_avg[:-1]) * d_y * 1000, angles[:-1], 'k', linewidth=2)
    else:
        axes.set_ylabel("x - ang, [deg]")
        axes.set_xlabel("y, [$\mu$M]")
        if avg:
            legend = [f"avg"]
            scale = 1.0 / len(difference)
            difference_avg = np.array([scale * sum(i for i in v) for v in zip(*difference)])
            values = poly_fit(angles, ya, difference_avg, 5)
            plt.plot(angles[:-1], (values[1:] - values[:-1]) * d_y * 1000, 'k', linewidth=2)
        else:
            legend = []
            for val, wl in zip(difference, scheme_real.wavelengths):
                values = poly_fit(angles, ya, val, 5)
                plt.plot(angles[:-1], (values[1:] - values[:-1]) * 1000 * d_y, linewidth=0.75)
                legend.append(f"lam = {str(wl):5>}, $\mu$M")
            legend.append(f"avg")
            scale = 1.0 / len(difference)
            difference_avg = poly_fit(angles, ya, np.array([scale * sum(i for i in v) for v in zip(*difference)]), 5)
            plt.plot(angles[:-1], (difference_avg[1:] - difference_avg[:-1]) * 1000 * d_y, 'k', linewidth=2)
    axes.grid(True)
    axes.legend(legend, loc=2)
    # plt.show()
    return fig


def compute_focal_shift(scheme_real: ResultFile, file_name: str = "focal_shift.csv", psf: bool = False):
    a = 0.750
    da = 1e-5

    def formatter(i):
        return f"\"C{i}\""

    with open(file_name, "wt") as output_file:
        print(f"\"poly-x\"", file=output_file)
        print(f"\"wl\";{';'.join(f'{formatter(i)}' for i in range(6))}", file=output_file)
        for coord in scheme_real.cords:
            angles = np.linspace(coord.AX_MIN, coord.AX_MAX, coord.N_ANGLES_X)
            wl = scheme_real.wavelengths[coord.WAVE_ID - 1]
            print(f"{wl:>.2f};{';'.join(f'{v:.6E}' for v in poly_regression(angles, a * coord.x_slice, 6).flat)}",
                  file=output_file)

        print("", file=output_file)
        print(f"\"poly-y\"", file=output_file)
        print(f"\"wl\";{';'.join(f'{formatter(i)}' for i in range(6))}", file=output_file)
        for coord in scheme_real.cords:
            angles = np.linspace(coord.AY_MIN, coord.AY_MAX, coord.N_ANGLES_Y)
            wl = scheme_real.wavelengths[coord.WAVE_ID - 1]
            print(f"{wl:>.2f};{';'.join(f'{v:.6E}' for v in poly_regression(angles, a * coord.y_slice, 6).flat)}",
                      file=output_file)

        print("", file=output_file)
        print(f"\"linear-x\"", file=output_file)
        print(f"\"wl\";\"k\";\"b\"", file=output_file)
        for coord in scheme_real.cords:
            angles = np.linspace(coord.AX_MIN, coord.AX_MAX, coord.N_ANGLES_X)
            wl = scheme_real.wavelengths[coord.WAVE_ID - 1]
            print(f"{wl:>.2f};{';'.join(f'{v:.8E}' for v in linear_regression(angles, a * coord.x_slice))}",
                  file=output_file)

        print("", file=output_file)
        print(f"\"linear-y\"", file=output_file)
        print(f"\"wl\";\"k\";\"b\"", file=output_file)
        for coord in scheme_real.cords:
            angles = np.linspace(coord.AY_MIN, coord.AY_MAX, coord.N_ANGLES_Y)
            wl = scheme_real.wavelengths[coord.WAVE_ID - 1]
            print(f"{wl:>.2f};{';'.join(f'{v:.6E}'  for v in linear_regression(angles, a * coord.y_slice))}",
                  file=output_file)

        print("", file=output_file)
        print(f"\"inv-poly-x\"", file=output_file)
        print(f"\"wl\";{';'.join(f'{formatter(i)}' for i in range(6))}", file=output_file)
        for coord in scheme_real.cords:
            angles = np.linspace(coord.AX_MIN, coord.AX_MAX, coord.N_ANGLES_X)
            wl = scheme_real.wavelengths[coord.WAVE_ID - 1]
            print(f"{wl:>.2f};{';'.join(f'{v:.6E}' for v in poly_regression(a * coord.x_slice, angles, 6).flat)}",
                  file=output_file)
        print("", file=output_file)
        print(f"\"inv-poly-y\"", file=output_file)
        print(f"\"wl\";{';'.join(f'{formatter(i)}' for i in range(6))}", file=output_file)
        for coord in scheme_real.cords:
            angles = np.linspace(coord.AY_MIN, coord.AY_MAX, coord.N_ANGLES_Y)
            wl = scheme_real.wavelengths[coord.WAVE_ID - 1]
            print(f"{wl:>.2f};{';'.join(f'{v:.6E}' for v in poly_regression(a * coord.y_slice, angles, 6).flat)}",
                  file=output_file)

        print("", file=output_file)
        print(f"\"inv-linear-x\"", file=output_file)
        print(f"\"wl\";\"k\";\"b\"", file=output_file)
        for coord in scheme_real.cords:
            angles = np.linspace(coord.AX_MIN, coord.AX_MAX, coord.N_ANGLES_X)
            wl = scheme_real.wavelengths[coord.WAVE_ID - 1]
            print(f"{wl:>.2f};{';'.join(f'{v:.6E}' for v in linear_regression(a * coord.x_slice, angles))}",
                  file=output_file)

        print("", file=output_file)
        print(f"\"inv-linear-y\"", file=output_file)
        print(f"\"wl\";\"k\";\"b\"", file=output_file)
        for coord in scheme_real.cords:
            angles = np.linspace(coord.AY_MIN, coord.AY_MAX, coord.N_ANGLES_Y)
            wl = scheme_real.wavelengths[coord.WAVE_ID - 1]
            print(f"{wl:>.2f};{';'.join(f'{v:.6E}' for v in linear_regression(a * coord.y_slice, angles))}",
                  file=output_file)


def draw_pos_from_angle(scheme_real, scheme_deformed, direction="y"):
    _dir = True if direction == "y" else False
    angles = scheme_real.y_angles if _dir else scheme_real.x_angles
    ys = np.linspace(angles[0], angles[-1], 128)
    fig, axes = plt.subplots(figsize=(WIDTH_SIZE, HEIGHT_SIZE))
    fig.subplots_adjust(left=0.075,
                        bottom=0.075,
                        right=0.925,
                        top=0.925,
                        wspace=0.125,
                        hspace=0.125)

    axes.set_xlabel("ang, [deg]")
    axes.set_ylabel("y, [mm]" if _dir else "x, [mm]")
    legend = []
    print(scheme_real.n_wave_lengths)
    if scheme_real is not None:
        a = 1.0
        da = 1e-5
        print(f"\n{'wl':^15} {' '.join(f'{i:^15}' for i in range(6))}")
        with open("FocalShift/psf_inv_poly.csv", "wt") as output_file:
            for coord in scheme_real.cords:
                angles  = np.linspace(coord.AY_MIN, coord.AY_MAX, coord.N_ANGLES_Y) \
                    if _dir else np.linspace(coord.AX_MIN, coord.AX_MAX, coord.N_ANGLES_X)
                coord_slice = coord.y_slice if _dir else coord.x_slice
                wl       = scheme_real.wavelengths[coord.WAVE_ID - 1]
                ys       = np.linspace(angles[0], angles[-1], 128)
                line_sag = plt.plot(poly_fit(ys, angles, coord_slice, 5), ys)
                # print(f"{wl:>.2f};{';'.join(f'{v:15.8E}'for v in linear_regression(a * coord_slice, angles))}", file=output_file)
                print(f"{wl:>.2f};{';'.join(f'{v:15.8E}'for v in poly_regression(a * coord_slice, angles,  6).flat)}", file=output_file)
                a += da
                if scheme_deformed is not None:
                    line_sag[-1].set_linestyle('--')
                legend.append(f"lam = {str(wl):5>}, $\mu$M"
                              if scheme_deformed is None else f"Real, lam = {str(wl):5>}, $\mu$M")

    if scheme_deformed is not None:
        for val, wl in zip(scheme_deformed.y_image_pos_per_angle_from_psf
                           if _dir else scheme_deformed.x_image_pos_per_angle_from_psf, scheme_deformed.wavelengths):
            plt.plot(ys, poly_fit(ys, angles, val, 5))
            legend.append(f"lam = {str(wl):5>}, $\mu$M"
                          if scheme_real is None else f"Deform, lam = {str(wl):5>}, $\mu$M" )
    axes.grid(True)
    axes.legend(legend, loc=2)
    # plt.show()
    return fig


def draw_y_from_angle_avg(scheme_1: ResultFile, scheme_2: ResultFile):
    ya = scheme_2.y_angles
    ys = np.linspace(ya[0], ya[-1], 128)
    fig, axes = plt.subplots(figsize=(WIDTH_SIZE, HEIGHT_SIZE))
    fig.subplots_adjust(left=0.075,
                        bottom=0.075,
                        right=0.925,
                        top=0.925,
                        wspace=0.25,
                        hspace=0.25)

    axes.set_xlabel("y - ang, [deg]")
    axes.set_ylabel("y, [mm]")
    legend = []
    line_sag = plt.plot(ys, poly_fit(ys, ya, scheme_1.y_image_pos_per_angle_from_psf_avg, 5))
    line_sag[-1].set_linestyle('--')
    legend.append(f"Real")

    plt.plot(ys, poly_fit(ys, ya, scheme_2.y_image_pos_per_angle_from_psf_avg, 5))
    legend.append(f"Deform")

    axes.grid(True)
    axes.legend(legend, loc=2)
    plt.show()


if __name__ == "__main__":
    renderSettings = ResultVisualSettings()
    renderSettings.subplots = (3, 3)
    results = ResultFile()
    results_deformed = ResultFile()

    results.         load(r"E:\Aist_T\ZemaxExec\Task\RESULTS\real_scheme.json")
    results_deformed.load(r"E:\Aist_T\ZemaxExec\Task\RESULTS\real_deformed_scheme.json")

    compute_focal_shift(results_deformed, "FocalShift/psf_results_deformed.csv")

    fig = draw_pos_from_angle(results, None)
    # fig.savefig(f"E:\\Aist_T\\angle_y_per_image_coord_center_pos.png")
    fig.show()

    fig = draw_pos_from_angle(results, None, 'x')
    # fig.savefig(f"E:\\Aist_T\\angle_x_per_image_coord_center_pos.png")
    fig.show()
    draw_y_from_angle_avg(results, results_deformed)

    fig = psf_difference(results, results_deformed)
    # fig.savefig(f"E:\\Aist_T\\psf_difference1111.png")
    fig.show()
    fig = psf_difference(results, results_deformed, spot_or_psf=False)
    # fig.savefig(f"E:\\Aist_T\\spot_difference.png")
    fig.show()

   #  fig = psf_difference(results, results_deformed, inv=True)
   #  fig.savefig(f"E:\\Aist_T\\psf_difference_inv.png")
   #  fig.show()
   #  fig = psf_difference(results, results_deformed, spot_or_psf=False, inv=True)
   #  fig.savefig(f"E:\\Aist_T\\spot_difference_inv.png")
   #  fig.show()
#
   #  fig = psf_difference_div(results, results_deformed)
   #  fig.savefig(f"E:\\Aist_T\\psf_difference_derivative.png")
   #  fig.show()
   #  fig = psf_difference_div(results, results_deformed, spot_or_psf=False)
   #  fig.savefig(f"E:\\Aist_T\\spot_difference_derivative.png")
   #  fig.show()
#
   #  fig = psf_difference_div(results, results_deformed, inv=True)
   #  fig.savefig(f"E:\\Aist_T\\psf_difference_derivative_inv.png")
   #  fig.show()
   #  fig = psf_difference_div(results, results_deformed, spot_or_psf=False, inv=True)
   #  fig.savefig(f"E:\\Aist_T\\spot_difference_derivative_inv.png")
   #  fig.show()
#

