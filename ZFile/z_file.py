from typing import List, Dict, Union, Tuple, Any
import os.path
import os
from TaskBuilder import SchemeParams
from .z_surface import ZFileField
from .z_file_raw import ZFileRaw
from .z_surface import ZSurface
from .z_fields import ZFields
from .z_waves import ZWaves


MAX_ZERNIKE_TERM = 8
MAX_EVEN_ASPHERIC_TERM = 8
Z_FILE_INDENT = '  '
Z_MAX_WL_COUNT = 24
COMMON_SCHEME_INFO = 1
SCHEME_SPOT_DIAGRAM = 2
SCHEME_MTF = 4
SCHEME_PSF = 8
INCLUDE_ZMX_PROTO = 16
SCHEME_ALL_CALCULATIONS = COMMON_SCHEME_INFO | SCHEME_SPOT_DIAGRAM | SCHEME_MTF | SCHEME_PSF | INCLUDE_ZMX_PROTO


class ZFile:
    _NO_FIELDS = {'WAVM', 'FTYP', 'XFLN', 'YFLN', 'FWGN', 'VDXN', 'VDYN', 'VCXN', 'VCYN', 'VANN'}

    def __init__(self, file_path: str = None):
        self._surfaces: Dict[int, ZSurface] = {}
        self._header_params: Dict[str, ZFileField] = {}
        self._footer_fields: Dict[str, ZFileField] = {}
        self._fields: Union[ZFields, None] = None
        self._waves: Union[ZWaves, None] = None
        self.load(file_path)

    @property
    def surfaces(self) -> Dict[int, ZSurface]:
        return self._surfaces

    @property
    def surfaces_params(self) -> Tuple[Tuple[Tuple[str, Any], ...], ...]:
        return tuple(tuple(param for param in surface) for surface in self.surfaces.values())

    @property
    def waves(self) -> ZWaves:
        return self._waves

    @property
    def fields(self) -> ZFields:
        return self._fields

    def __str__(self):
        nl = '\n'
        surfs = self._surfaces.values()
        data = [f"{nl.join(str(v) for v in self._header_params.values())}\n",
                f"{self._fields}", f"{self._waves}",
                f"{''.join(f'SURF {nl.join(str(v) for v in (s_id, s))}' for s_id, s in enumerate(surfs))}",
                f"{nl.join(str(v) for v in self._footer_fields.values())}\n"]
        return ''.join(v for v in data)

    def save(self, file_path: str):
        with open(file_path, 'wt') as output_file:
            print(self, file=output_file)

    def load(self, file_path: str) -> bool:
        if file_path is None:
            return False
        try:
            _zf: ZFileRaw = ZFileRaw(file_path)
            if _zf is None:
                return False
            self._fields = ZFields(_zf)
            self._waves = ZWaves(_zf)
            for v_id, v in _zf.header_params.items():
                if v_id in ZFile._NO_FIELDS:
                    continue
                self._header_params.update({v_id: ZFileField(v_id + " " + v[0])})
            for v_id, v in _zf.footer_params.items():
                if v_id in ZFile._NO_FIELDS:
                    continue
                self._footer_fields.update({v_id: ZFileField(v_id + " " + v[0])})
            for v_id, v in _zf.surfaces.items():
                self._surfaces.update({v_id: ZSurface(v)})
            return True
        except AssertionError as er:
            return False
        except ValueError as er:
            return False
        except KeyError as er:
            return False

    def contains_surf(self, surf_id: int) -> bool:
        assert isinstance(surf_id, int)
        return surf_id in self._surfaces

    @property
    def common_params(self):
        yield ('param', 'version'), ('value', ':'.join(str(int(v))for v in self.version.params) if self.version else '-')
        yield ('param', 'mode'), ('value', self.mode.params[0] if self.mode else '-')
        yield ('param', 'name'), ('value', self.name.params[0] if self.name else '-')
        yield ('param', 'units'), ('value', self.units.params[0] if self.units else '-')
        yield ('param', 'enter_pupil_diameter'), ('value', self.enter_pupil_diameter.params[0] if self.enter_pupil_diameter else '-')

    @property
    def version(self) -> Union[ZFileField, None]:
        return self._header_params['VERS'] if 'VERS' in self._header_params else None

    @property
    def mode(self) -> Union[ZFileField, None]:
        return self._header_params['MODE'] if 'MODE' in self._header_params else None

    @property
    def name(self) -> Union[ZFileField, None]:
        return self._header_params['NAME'] if 'NAME' in self._header_params else None

    @property
    def units(self) -> Union[ZFileField, None]:
        return self._header_params['UNIT'] if 'UNIT' in self._header_params else None

    @property
    def enter_pupil_diameter(self) -> Union[ZFileField, None]:
        return self._header_params['ENPD'] if 'ENPD' in self._header_params else None

    def get_dist_z(self, surf_id: int):
        if not self.contains_surf(surf_id):
            return 0.0
        return self._surfaces[surf_id].dist_z

    def dist_between_surfs(self, surf_id_1: int, surf_id_2: int):
        assert self.contains_surf(surf_id_1)
        assert self.contains_surf(surf_id_2)
        surf_id_1, surf_id_2 = (surf_id_1, surf_id_2) if (surf_id_1 < surf_id_2) else (surf_id_2, surf_id_1)
        return sum(self.get_dist_z(surf_id) for surf_id in range(surf_id_1, surf_id_2))

    def apply_settings(self, params: SchemeParams):
        surfaces = params.surf_params
        if params.fields is not None:
            fields_data = [v.to_list for v in params.fields.fields]
            for index, value in enumerate(fields_data):
                self.fields.xfln[index] = value[0]
                self.fields.yfln[index] = value[1]
                self.fields.fwgn[index] = value[2]
                self.fields.vdxn[index] = value[3]
                self.fields.vdyn[index] = value[4]
                self.fields.vcxn[index] = value[5]
                self.fields.vcyn[index] = value[6]
                self.fields.vann[index] = value[7]
        self._header_params.update({'NOTE': ZFileField(f'NOTE 0 {params.description_long}')})
        self._header_params.update({'NAME': ZFileField(f'NAME {params.description_short}')})

        if params.waves:
            self._waves = [ZWaves(v.lam, v.weight) for v in params.waves]

        remap = params.surf_remap
        for surf in surfaces:
            surf_id = surf.surf_n
            if remap:
                # TODO убрать surf_id + 1
                # surf_id = remap[surf_id + 1] if surf_id + 1 in remap else -1
                surf_id = remap[surf_id] if surf_id in remap else -1
            if not self.contains_surf(surf_id):
                continue
            surface: ZSurface = self._surfaces[surf_id]
            # if surf.decenter is not None:
            #     surface.decenter_before = surf.decenter
            # if surf.tilt is not None:
            #     surface.tilt_before = Vector3(surf.tilt.x, surf.tilt.y, 0.0)
                # surf.set_surf_tilt_before    (surf_id, Vector3(surf.tilt.x, surf.tilt.y, 0.0))
            # if surf.aperture is not None:
            #     surface.aperture = surf.aperture
            # if surf.curvature is not None:
            #     surface.curvature = surf.curvature
            if surf.zernike is None and surf.even_asph is None:
                continue
            if surf.zernike is None:
                surface.convert_to_even_aspheric(surf.even_asph)
                continue
            surface.convert_to_zernike(surf.zernike)

    def create_task(self, task_settings: List[SchemeParams], task_name: str = "Task", task_dir: str = None,
                    task_info: int = COMMON_SCHEME_INFO | SCHEME_SPOT_DIAGRAM | SCHEME_MTF | SCHEME_PSF):
        if task_dir is None:
            task_dir = os.getcwd() + "\\" + task_name + "\\"
        results_dir = task_dir + "RESULTS\\" if task_dir.endswith("\\") else task_dir + "\\RESULTS\\"

        if not os.path.isdir(task_dir):
            os.mkdir(task_dir)
        else:
            for file in os.listdir(task_dir):
                if file.endswith(("json", "txt", "zmx", "ses", "TXT", "ZMX", "SES")):
                    os.remove(task_dir + file)

        if not os.path.isdir(results_dir):
            os.mkdir(results_dir)
        else:
            for file in os.listdir(results_dir):
                if file.endswith("json"):
                    os.remove(results_dir + file)

        task_files = [task_dir + "zemax_proto_file.zmx"]
        with open(task_files[-1], "wt") as zmx:
            print(self, file=zmx)
        with open(results_dir + "zemax_proto_file.json", "wt"):
            pass

        for task in task_settings:
            task_files.append(task_dir + task.description_short.replace(" ", "_") + ".zmx")
            self.apply_settings(task)
            with open(task_files[-1], "wt") as zmx:
                print(self, file=zmx)
            with open(results_dir + task.description_short.replace(" ", "_") + ".json", "wt"):
                pass
        with open(task_dir + "SCHEMES_LIST.TXT", "wt") as task_list:
            print('\n'.join(v + " " + " ".join("1" if task_info & v == v
                                               else "0" for v in (1, 2, 4, 8)) for v in task_files), file=task_list)


def set_up_zmx(zmx_file_proto: str, zmx_file_settings: str, zmx_file_new: str):
    zf = ZFile()
    if zmx_file_proto.split('.')[-1] != "zmx":
        return
    if zmx_file_settings.split('.')[-1] != "json":
        return
    zf.load(zmx_file_proto)
    settings = SchemeParams.read(zmx_file_settings)
    zf.apply_settings(settings[-1])
    if zmx_file_new.split('.')[-1] != "zmx":
        zmx_file_new += ".zmx"
    with open(zmx_file_new, "wt") as zmx:
        print(zf, file=zmx)

