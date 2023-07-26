from collections import namedtuple
from ZFile import ZFileRaw


class ZSequentialSettings(namedtuple('ZSequentialSettings',
                                     'max_intersections_per_ray, max_segments_per_ray, max_nested_or_touching_objects, '
                                     'minimum_relative_ray_intensity, minimum_absolute_ray_intensity, '
                                     'glue_distance_in_lens_unit, missed_ray_draw_distance_in_lens_unit,'
                                     'maximum_source_file_rays_in_memory, retrace_source_file_upon_file_open,'
                                     'simple_ray_splitting')):

    def __new__(cls, z_file: ZFileRaw):
        assert 'NSCD' in z_file.params
        raw_info = z_file.params['NSCD'][0].split(' ')
        return super.__new__(cls, int(raw_info[1]), int(raw_info[4]), float(raw_info[3]), float(raw_info[2]),
                                  float(raw_info[6]), float(raw_info[10]), int(raw_info[12]),
                                  True if raw_info[6] == '1' else False, True if raw_info[13] == '1' else False)

    def __repr__(self):
        return "{{\n"\
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

    def __str__(self):
        return f"NSCD"\
               f" {self.max_intersections_per_ray}"\
               f" {self.max_segments_per_ray}"\
               f" {self.max_nested_or_touching_objects}"\
               f" {self.minimum_relative_ray_intensity}"\
               f" {self.minimum_absolute_ray_intensity}"\
               f" {self.glue_distance_in_lens_unit}"\
               f" {self.missed_ray_draw_distance_in_lens_unit}"\
               f" {self.maximum_source_file_rays_in_memory}"\
               f" {1 if self.retrace_source_file_upon_file_open else 0 }"\
               f" {1 if self.simple_ray_splitting else 0}"
