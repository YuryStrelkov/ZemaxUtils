from .z_file import ZFileRaw
import dataclasses


@dataclasses.dataclass(frozen=True)
class ZSequentialSettings:
    max_intersections_per_ray: int
    max_segments_per_ray: int
    max_nested_or_touching_objects: int
    minimum_relative_ray_intensity: float
    minimum_absolute_ray_intensity: float
    glue_distance_in_lens_unit: float
    missed_ray_draw_distance_in_lens_unit: float
    maximum_source_file_rays_in_memory: int
    retrace_source_file_upon_file_open: bool
    simple_ray_splitting: bool

    @classmethod
    def create(cls, z_file: ZFileRaw) -> 'ZSequentialSettings':
        assert 'NSCD' in z_file.params
        raw_info = z_file.params['NSCD'][0].split(' ')
        return cls(int(raw_info[1]),
                   int(raw_info[4]),
                   int(raw_info[3]),
                   float(raw_info[2]),
                   float(raw_info[6]),
                   float(raw_info[10]),
                   0.0,
                   int(raw_info[12]),
                   True if raw_info[6] == '1' else False,
                   True if raw_info[13] == '1' else False)

    def __iter__(self):
        yield 'Setting', "max_intersections_per_ray"
        yield 'Value', self.max_intersections_per_ray
        yield 'Setting', "max_segments_per_ray"
        yield 'Value', self.max_segments_per_ray
        yield 'Setting', "max_nested_or_touching_objects"
        yield 'Value', self.max_nested_or_touching_objects
        yield 'Setting', "minimum_relative_ray_intensity"
        yield 'Value', self.minimum_relative_ray_intensity
        yield 'Setting', "minimum_absolute_ray_intensity"
        yield 'Value', self.minimum_absolute_ray_intensity
        yield 'Setting', "glue_distance_in_lens_unit"
        yield 'Value', self.glue_distance_in_lens_unit
        yield 'Setting', "missed_ray_draw_distance_in_lens_unit"
        yield 'Value', self.missed_ray_draw_distance_in_lens_unit
        yield 'Setting', "maximum_source_file_rays_in_memory"
        yield 'Value', self.maximum_source_file_rays_in_memory
        yield 'Setting', "retrace_source_file_upon_file_open"
        yield 'Value', self.retrace_source_file_upon_file_open
        yield 'Setting', "simple_ray_splitting"
        yield 'Value', self.simple_ray_splitting

    def __repr__(self) -> str:
        return "{{\n" \
               f"\t\"MaxIntersectionsPerRay\":          {self.max_intersections_per_ray            :>12},\n" \
               f"\t\"MaxSegmentsPerRay\":               {self.max_segments_per_ray                 :>12},\n" \
               f"\t\"MaxNestedOrTouchingObjects\":      {self.max_nested_or_touching_objects       :>12},\n" \
               f"\t\"MinimumRelativeRayIntensity\":     {self.minimum_relative_ray_intensity       :>12},\n" \
               f"\t\"MinimumAbsoluteRayIntensity\":     {self.minimum_absolute_ray_intensity       :>12},\n" \
               f"\t\"GlueDistanceInLensUnit\":          {self.glue_distance_in_lens_unit           :>12},\n" \
               f"\t\"MissedRayDrawDistanceInLensUnit\": {self.missed_ray_draw_distance_in_lens_unit:>12},\n" \
               f"\t\"MaximumSourceFileRaysInMemory\":   {self.maximum_source_file_rays_in_memory   :>12},\n" \
               f"\t\"RetraceSourceFileUponFileOpen\":   {self.retrace_source_file_upon_file_open   :>12},\n" \
               f"\t\"SimpleRaySplitting\":              {self.simple_ray_splitting                 :>12}\n}}"

    def __str__(self) -> str:
        return f"NSCD" \
               f" {self.max_intersections_per_ray}" \
               f" {self.max_segments_per_ray}" \
               f" {self.max_nested_or_touching_objects}" \
               f" {self.minimum_relative_ray_intensity}" \
               f" {self.minimum_absolute_ray_intensity}" \
               f" {self.glue_distance_in_lens_unit}" \
               f" {self.missed_ray_draw_distance_in_lens_unit}" \
               f" {self.maximum_source_file_rays_in_memory}" \
               f" {1 if self.retrace_source_file_upon_file_open else 0}" \
               f" {1 if self.simple_ray_splitting else 0}"
