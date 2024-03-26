from TaskBuilder import SchemeParams, SurfaceParams
from UI.z_draw import test
from ZFile import ZFile


if __name__ == '__main__':
    scheme = ZFile()
    scheme.load("../ZemaxSchemes/F_07g_04_Blenda_PI_Fin.ZMX")
    test(scheme)