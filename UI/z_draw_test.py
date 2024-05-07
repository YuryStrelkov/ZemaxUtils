from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from UI.UIStyle import load_style
import matplotlib.pyplot as plt
from UI import UIImageWidget
from UI.z_draw import test
from matplotlib import cm
from ZFile import ZFile
import numpy as np
import sys


def tri_surf_test():
    # plt.style.use('_mpl-gallery')

    n_radii = 8
    n_angles = 36

    # Make radii and angles spaces
    radii = np.linspace(0.125, 1.0, n_radii)
    angles = np.linspace(0, 2 * np.pi, n_angles, endpoint=False)[..., np.newaxis]

    # Convert polar (radii, angles) coords to cartesian (x, y) coords.
    x = np.append(0, (radii * np.cos(angles)).flatten())
    y = np.append(0, (radii * np.sin(angles)).flatten())
    z = np.sin(-x * y)

    # Plot
    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
    ax.plot_trisurf(x, y, z, vmin=z.min() * 2, cmap=cm.Blues)

    ax.set(xticklabels=[],
           yticklabels=[],
           zticklabels=[])

    plt.show()


def ui_items_test():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    load_style('dark_theme_palette.json', app)
    container = QWidget()
    container.setLayout(QVBoxLayout())
    container.layout().addWidget(UIImageWidget("image1.jpg"))
    container.setMinimumWidth(0)
    container.setMinimumHeight(0)
    container.show()
    # window = UIMainWindow()
    sys.exit(app.exec())


if __name__ == '__main__':
    ui_items_test()
    # tri_surf_test()
    # mirror_trace_test()
    # exit()
    # lens_trace_test()
    # exit()
    scheme = ZFile()
    # scheme.load("../ZemaxSchemes/fullMicro.ZMX")
    scheme.load("../ZemaxSchemes/F_07g_04_Blenda_PI_Fin.ZMX")
    test(scheme)