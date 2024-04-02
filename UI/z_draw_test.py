from TaskBuilder import SchemeParams, SurfaceParams
from UI.z_draw import test
from ZFile import ZFile


if __name__ == '__main__':
    # mirror_trace_test()
    # exit()
    # lens_trace_test()
    # exit()
    scheme = ZFile()
    scheme.load("../ZemaxSchemes/fullMicro.ZMX")
    # scheme.load("../ZemaxSchemes/F_07g_04_Blenda_PI_Fin.ZMX")
    test(scheme)