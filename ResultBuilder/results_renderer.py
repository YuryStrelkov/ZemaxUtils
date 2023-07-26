from .result_visual_settings import ResultVisualSettings
from .result_components import MTFResponse
from .result_components import SpotDiagram
from .result_components import PSFDiagram
from typing import List, Tuple, Union
from matplotlib import pyplot as plt
from matplotlib.artist import Artist
from .result_file import ResultFile
from .utils import color_map_quad
import numpy as np


def _re_append_text(axes, text):
    if len(axes.texts) != 0:
        Artist.remove(axes.texts[-1])
    props = dict(boxstyle='round', facecolor='white', alpha=0.9)
    axes.text(0.05, 0.05, text, horizontalalignment='left', verticalalignment='bottom',
              transform=axes.transAxes, bbox=props)


def _append_legend_twice(axes, results: ResultFile, response: Union[MTFResponse, PSFDiagram, SpotDiagram]):
    ax_legend = axes.get_legend()
    legend = [] if ax_legend is None else [v.get_text() for v in ax_legend.texts]
    if response.WAVE_ID == -1:
        legend.append(f"S, Ax =  {str(results.fields[response.FIELD_ID].FLDX):5>}, lam = ALL")
        legend.append(f"T, Ay =  {str(results.fields[response.FIELD_ID].FLDY):5>}, lam = ALL")
    elif response.FIELD_ID == -1:
        legend.append(f"S, Ax = ALL, lam = {str(results.wavelengths[response.WAVE_ID - 1]):5>}, $\mu$M")
        legend.append(f"T, Ay = ALL, lam = {str(results.wavelengths[response.WAVE_ID - 1]):5>}, $\mu$M")
    else:
        legend.append(f"S, Ax =  {str(results.fields[response.FIELD_ID].FLDX):5>},"
                      f" lam = {str(results.wavelengths[response.WAVE_ID - 1]):5>}, $\mu$M")
        legend.append(f"T, Ay =  {str(results.fields[response.FIELD_ID].FLDY):5>},"
                      f" lam = {str(results.wavelengths[response.WAVE_ID - 1]):5>}, $\mu$M")
    return legend


def _append_legend(axes, results: ResultFile, response: Union[MTFResponse, PSFDiagram, SpotDiagram]):
    ax_legend = axes.get_legend()
    legend = [] if ax_legend is None else [v.get_text() for v in ax_legend.texts]
    if response.WAVE_ID == -1:
        legend.append(f"Ax = {str(results.fields[response.FIELD_ID].FLDX):5>},"
                      f" Ay = {str(results.fields[response.FIELD_ID].FLDY):5>}, lam = ALL")
    elif response.FIELD_ID == -1:
        legend.append(f"Ax = ALL, Ay = ALL, lam = {str(results.wavelengths[response.WAVE_ID - 1]):5>}, $\mu$M")

    elif response.FIELD_ID == -1 and response.WAVE_ID == -1:
        if len(legend) == 0:
            legend.append(f"Ax = ALL, Ay = ALL, lam = ALL, $\mu$M")
            return legend
        return []
    else:
        legend.append(f"Ax = {str(results.fields[response.FIELD_ID].FLDX):5>},"
                      f" Ay = {str(results.fields[response.FIELD_ID].FLDY):5>},"
                      f" lam = {str(results.wavelengths[response.WAVE_ID - 1]):5>}, $\mu$M")
    return legend


def show_mtf_data(results: ResultFile, response: MTFResponse, axes=None, color="#0000ff"):
    """
    :param results:
    :param response:
    :param axes:
    :param color:
    :param legend_info: 0 - только поля в легенде, 1 -  только длины волн в легенде, 2 -  и поля и длины волн в легенде
    :return:
    """
    if axes is None:
        fig, axes = plt.subplots(1)
    if not response:
        return axes.figure
    line_tan = axes.plot(response.FREQ, response.TAN, color=color)
    line_sag = axes.plot(response.FREQ, response.SAG, color=color)
    line_sag[-1].set_linestyle('--')
    axes.set_xlabel("freq, [lines/mm]")
    axes.set_ylabel("|OTF|")
    axes.legend(_append_legend_twice(axes, results, response), loc=1)
    axes.grid(True)
    return axes.figure


def _show_mtf(results: ResultFile, field_id: int, wave_id: int, axes=None):
    if axes is None:
        fig, axes = plt.subplots(1)
        axes.set_title(f"FFT MTF | WL: {'ALL' if field_id == -1 else field_id} |"
                       f" FIELD: {'ALL' if wave_id == -1 else wave_id}",  y=1.0, pad=-14)

    axes.set_xlabel("freq, [lines/mm]")
    axes.set_ylabel("|FFT MTF|")
    axes.grid      (True)
    mtf_s = results.get_mtf(field_id, wave_id)
    if not isinstance(mtf_s, list):
        return show_mtf_data(results, mtf_s, axes)
    color = color_map_quad(len(mtf_s))
    for item_id, mtf in enumerate(mtf_s):
        show_mtf_data(results, mtf, axes, color[item_id])
    return axes.figure


def show_spt_data(results: ResultFile, spot: SpotDiagram, axes=None, color="#000000", box_size: float = 20):
    """
    :param results:
    :param spot:
    :param axes:
    :param color:
    :param box_size:
    :param legend_info: 0 - только поля в легенде, 1 -  только длины волн в легенде, 2 -  и поля и длины волн в легенде
    :return:
    """
    if axes is None:
        fig, axes = plt.subplots(1)
        axes.set_title(f"SPOT | WL: {spot.WAVE_ID} | FIELD: {spot.FIELD_ID}",  y=1.0, pad=-14)
    if not spot:
        return axes.figure
    axes.plot([v.x for v in spot.POINTS], [v.y for v in spot.POINTS], color=color, linewidth=0, marker='.')
    axes.set_xlabel("x, [mm]")
    axes.set_ylabel("y, [mm]")
    axes.set_yticklabels([])
    axes.set_xticklabels([])
    ray = results.get_chief_ray(spot.FIELD_ID, spot.WAVE_ID)
    x0, y0 = ray.POSITION.x, ray.POSITION.y
    text = f"GEO R = {spot.R_GEO:>10.4f} [mm], RMS R = {spot.R_RMS:>10.4f} [mm]\n" \
           f"СENTER, [mm] = {{{x0:>10.4f} [mm], {y0:>10.4f}}}\n" \
           f"BOX SIZE, [mm] = {{{box_size:>10.2f}, {box_size:>10.2f}}}"
    _re_append_text(axes, text)
    axes.set_xlim([-0.5 * box_size * spot.R_GEO + x0, 0.5 * box_size * spot.R_GEO + x0])
    axes.set_ylim([-0.5 * box_size * spot.R_GEO + y0, 0.5 * box_size * spot.R_GEO + y0])
    axes.set_aspect('equal', 'box')
    axes.grid(True)
    return axes.figure


def _spot_geo_info(results: ResultFile, spots: List[SpotDiagram]) -> Tuple[float, float, float, float]:
    avg_r = 0.0
    rms_r = 0.0
    x0 = 0.0
    y0 = 0.0
    for spt in spots:
        ray = results.get_chief_ray(spt.FIELD_ID, spt.WAVE_ID)
        if ray is None:
            continue
        x0 += ray.POSITION.x
        y0 += ray.POSITION.y
        avg_r += spt.R_GEO
        rms_r += spt.R_RMS
    return x0 / len(spots), y0 / len(spots), avg_r / len(spots), rms_r / len(spots)


def _show_spot(results: ResultFile, field_id: int, wave_id: int, axes=None, box_size: float = 20.0):
    if axes is None:
        fig, axes = plt.subplots(1)
        axes.set_title(f"SPOT | FIELD: {'ALL' if field_id == -1 else field_id} |"
                       f" WL: {'ALL' if wave_id == -1 else wave_id}",  y=1.0, pad=-14)
    axes.set_xlabel("x, [mm]")
    axes.set_ylabel("y, [mm]")
    axes.grid      (True)
    spot = results.get_spot(field_id, wave_id)
    if not isinstance(spot, list):
        return show_spt_data(results, spot, axes)
    color = color_map_quad(len(spot))
    for item_id, mtf in enumerate(spot):
        show_spt_data(results, mtf, axes, color[item_id])
        axes.set_title(f"SPOT | FIELD: {'ALL' if field_id == -1 else field_id} |"
                       f" WL: {'ALL' if wave_id == -1 else wave_id}",  y=1.0, pad=-14)
    if len(axes.texts) != 0:
        Artist.remove(axes.texts[-1])
    x0, y0, avg_r, rms_r = _spot_geo_info(results, spot)
    axes.set_aspect('equal', 'box')
    text = f"GEO R = {avg_r:<.4f} [mm], RMS R = {rms_r:<.4f} [mm]\n" \
           f"СENTER, [mm] = {{{x0:>.4f}, {y0:>.4f}}}\n" \
           f"BOX SIZE, [mm] = {{{box_size:<.2f}, {box_size:<.2f}}}"
    axes.set_yticklabels([])
    axes.set_xticklabels([])
    _re_append_text(axes, text)
    return axes.figure


def show_psf_data(results: ResultFile, psf: PSFDiagram, axes=None):
    if axes is None:
        fig, axes = plt.subplots()
        axes.set_title(f"PSF | FIELD: {psf.FIELD_ID} |"
                       f" WL: {psf.WAVE_ID}",  y=1.0, pad=-14)
    side_half = psf.width * 0.5
    ray = results.get_chief_ray(psf.FIELD_ID, psf.WAVE_ID)
    x0, y0 = ray.POSITION.x, ray.POSITION.y
    axes.imshow(psf.PSF_DATA[:, 0: psf.cols // 2, 0],
                extent=[-side_half + x0, side_half + x0, -side_half + y0, side_half + y0])
    axes.set_xlabel("x, [mm]")
    axes.set_ylabel("y, [mm]")
    axes.set_aspect('equal', 'box')
    text = f"WL,[$\mu$M]    = {str(results.wavelengths[psf.WAVE_ID - 1]):5>}\n" \
           f"CHIEF_RAY,[mm] = {{{x0:>.4f}, {y0:>.4f}}}\n" \
           f"PSF_MAX,  [mm] = {{{psf.PSF_MAX.x + x0:>.4f}, {psf.PSF_MAX.y + y0:>.4f}}}\n" \
           f"BOX SIZE, [mm] = {{{psf.width:<.2f}, {psf.height:<.2f}}}"
    _re_append_text(axes, text)
    axes.set_yticklabels([])
    axes.set_xticklabels([])
    axes.grid(True)
    return axes.figure


def _show_psf(results: ResultFile,  field_id: int, wave_id: int, axes=None):
    # TODO FIX field_id == -1 or wave_id == -1
    psf = results.get_psf(field_id, wave_id)
    if axes is None:
        fig, axes = plt.subplots()
    if not psf:
        return
    if len(psf) == 1:
        n_points = psf.PSF_DATA.shape[0]
        delta = psf.PSF_DELTA
        side_half = n_points * delta * 0.5 * 0.001
        ray = results.get_chief_ray(field_id, wave_id)
        x0, y0 = ray.POSITION.x, ray.POSITION.y
        axes.imshow(psf.PSF_DATA[:, 0: n_points // 2, 0],
                    extent=[-side_half + x0, side_half + x0, -side_half + y0, side_half + y0])
        axes.set_xlabel("x, [mm]")
        axes.set_ylabel("y, [mm]")
        axes.set_aspect('equal', 'box')
        text = f"WL,[$\mu$M]    = {str(results.wavelengths[psf.WAVE_ID - 1]):5>}\n" \
               f"CHIEF_RAY,[mm] = {{{x0:>.4f}, {y0:>.4f}}}\n" \
               f"PSF_MAX,  [mm] = {{{psf.PSF_MAX.x + x0:>.4f}, {psf.PSF_MAX.y + y0:>.4f}}}\n" \
               f"BOX SIZE, [mm] = {{{psf.width:<.2f}, {psf.height:<.2f}}}"
        _re_append_text(axes, text)
        axes.set_yticklabels([])
        axes.set_xticklabels([])
        axes.grid(True)
        return axes.figure

    for psf_i in psf:
        n_points = psf_i.PSF_DATA.shape[0]
        delta = psf_i.PSF_DELTA
        side_half = n_points * delta * 0.5 * 0.001
        ray = results.get_chief_ray(field_id, wave_id)
        x0, y0 = ray.POSITION.x, ray.POSITION.y
        axes.imshow(psf_i.PSF_DATA[:, 0: n_points // 2, 0],
                    extent=[-side_half + x0, side_half + x0,
                            -side_half + y0, side_half + y0])
        axes.set_xlabel("x, [mm]")
        axes.set_ylabel("y, [mm]")
        axes.set_aspect('equal', 'box')
        text = f"WL,[$\mu$M]    = {str(results.wavelengths[psf.WAVE_ID - 1]):5>}\n" \
               f"CHIEF_RAY,[mm] = {{{x0:>.4f}, {y0:>.4f}}}\n" \
               f"PSF_MAX,  [mm] = {{{psf.PSF_MAX.x + x0:>.4f}, {psf.PSF_MAX.y + y0:>.4f}}}\n" \
               f"BOX SIZE, [mm] = {{{psf.width:<.2f}, {psf.height:<.2f}}}"
        _re_append_text(axes, text)
        axes.set_yticklabels([])
        axes.set_xticklabels([])
        axes.grid(True)
    return axes.figure


def show_psf_cross_sect_data(results: ResultFile, psf: PSFDiagram, axes=None, color="#0000ff", legend_info: int = 0):
    if axes is None:
        fig, axes = plt.subplots(1)
    if not psf:
        return axes.figure
    x_cross, y_cross = psf.cross_section_at_center
    x0, y0 = results.get_chief_ray(psf.FIELD_ID, psf.WAVE_ID).POSITION
    dx = psf.width  / (x_cross.size - 1)
    dy = psf.height / (y_cross.size - 1)
    x = np.array([-psf.width  * 0.5 + dx * i for i in range(x_cross.size)])
    y = np.array([-psf.height * 0.5 + dy * i for i in range(y_cross.size)])
    line_x = axes.plot(x, x_cross, color=color)
    line_y = axes.plot(y, y_cross, color=color)
    line_y[-1].set_linestyle('--')
    axes.set_xlabel("x, [mm]")
    axes.set_ylabel("I, [n.a.]")
    axes.set_title(f"FFT PSF | WL: {psf.WAVE_ID} | FIELD: {psf.FIELD_ID}",  y=1.0, pad=-14)
    _, labels = axes.get_legend_handles_labels()
    legend = {*labels}
    if legend_info == 0:
        legend.update({f"Cross - X. Ax = {str(results.fields[psf.FIELD_ID].FLDX):5>}",
                       f"Cross - Y. Ay = {str(results.fields[psf.FIELD_ID].FLDY):5>}"})
    if legend_info == 1:
        legend.update({f"Cross - X. lam = {str(results.wavelengths[psf.WAVE_ID]):5>}, $\mu$M",
                       f"Cross - Y. lam = {str(results.wavelengths[psf.WAVE_ID]):5>}, $\mu$M"})
    if legend_info == 2:
        legend.update({f"Cross - X. Ax = {str(results.fields[psf.FIELD_ID].FLDX):5>}, "
                       f"lam = {str(results.wavelengths[psf.WAVE_ID]):5>}, $\mu$M",
                       f"Cross - Y. Ay = {str(results.fields[psf.FIELD_ID].FLDY):5>},"
                       f" lam = {str(results.wavelengths[psf.WAVE_ID]):5>}, $\mu$M"})

    text = f"Center at x = {str(x0) : >5} mm\nCenter at y = {str(y0) : >5} mm\nReference : chief ray"
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    axes.text(0.05, 0.05, text, horizontalalignment='left',
              verticalalignment='top', transform=axes.transAxes, bbox=props)

    axes.legend(legend, loc=1)
    axes.grid(True)
    return axes.figure


def _show_psf_cross_section(results: ResultFile, field_id: int, wave_id: int, axes=None):
    psf = results.get_psf(field_id, wave_id)
    if axes is None:
        fig, axes = plt.subplots()
    if not psf:
        return
    if len(psf) == 1:
        show_psf_cross_sect_data(results, psf)
        return axes.figure
    color = color_map_quad(len(psf))
    if field_id == -1:
        for item_id, spt in enumerate(psf):
            show_psf_cross_sect_data(results, spt, axes, color[item_id], legend_info=1)
            axes.set_title(f"FFT MTF | WL: {wave_id} | FIELD: 'ALL'",  y=1.0, pad=-14)
    if wave_id == -1:
        for item_id, spt in enumerate(psf):
            show_psf_cross_sect_data(results, spt, axes, color[item_id], legend_info=0)
            axes.set_title(f"FFT MTF | WL: 'ALL' | FIELD: {field_id}",  y=1.0, pad=-14)
    return axes.figure


def draw_mtf(results: ResultFile, visual_settings: ResultVisualSettings, show: bool = True):
    fig, axes = visual_settings.build_figure()
    if visual_settings.subplots_count == 1:
        _show_mtf(results, -1, -1, axes)
        axes.grid(True)
    else:
        for axes_id, ax in enumerate(axes.flat):
            _show_mtf(results, axes_id + 1, -1, ax)
            ax.grid(True)
    if show:
        plt.show()
    return fig


def draw_spot(results: ResultFile, visual_settings: ResultVisualSettings, show: bool = True):
    fig, axes = visual_settings.build_figure()
    if visual_settings.subplots_count == 1:
        _show_spot(results, -1, -1, axes)
        axes.grid(True)
    else:
        for axes_id, ax in enumerate(axes.flat):
            _show_spot(results, axes_id + 1, -1, ax)
            ax.grid(True)
    if show:
        plt.show()
    return fig


def draw_psf(results: ResultFile, visual_settings: ResultVisualSettings, show: bool = True):
    fig, axes = visual_settings.build_figure()
    for axes_id in range(visual_settings.subplots_count):
        row, col = divmod(axes_id, visual_settings.x_subplots)
        field_id = min(1 + int(results.n_fields       * row / visual_settings.y_subplots), results.n_fields)
        wave_id  = min(1 + int(results.n_wave_lengths * col / visual_settings.x_subplots), results.n_wave_lengths)
        _show_psf(results, field_id, wave_id, axes[row, col])
        axes[row, col].grid(True)
    if show:
        plt.show()
    return fig


def draw_psf_cross_section(results: ResultFile, visual_settings: ResultVisualSettings, show: bool = True):
    fig, axes = visual_settings.build_figure()
    for axes_id in range(visual_settings.subplots_count):
        row, col = divmod(axes_id, visual_settings.x_subplots)
        field_id = min(1 + int(results.n_fields * axes_id / visual_settings.subplots_count), results.n_fields)
        _show_psf_cross_section(results, field_id, -1, axes[row, col])
        axes[row, col].grid(True)
    if show:
        plt.show()
    return fig
