#!/usr/bin/env cctbx.python

__author__ = "Adam Simpkin & Felix Simkovic"

from cctbx import crystal
from cctbx import miller
from cctbx import sgtbx
from cctbx.xray import observation_types
from iotbx import reflection_file_reader
from iotbx.reflection_file_utils import looks_like_r_free_flags_info


class ReflectionData(object):
    def __init__(self, reflection_file):
        self.reflection_file = reflection_file
        self.reflection_data = reflection_file_reader.any_reflection_file(file_name=reflection_file)

    def get(self, labels):
        for m_a in self.miller_arrays:
            if m_a.info().labels == labels:
                return m_a
        raise RuntimeError("{} columns not found in {}".format(labels, self.reflection_file))

    def i2f(self, labels):
        m_a = self.get(labels)
        if not m_a.is_intensity_array():
            raise ValueError('Array is not an intensity array')
        array_info = miller.array_info()
        array_info.labels = ['Fobs', 'Sigma-Fobs']
        amplitude_m_a = m_a.customized_copy(observation_type=observation_types.amplitude(), info=array_info)
        return amplitude_m_a

    def reindex(self, sg):
        for m_a in self.miller_arrays:
            if not looks_like_r_free_flags_info(m_a.info()):
                m_a.change_symmetry(sg)

    def checkhkl(self):
        def unique_reflections(m_a):
            indices = m_a.indices()
            return len({tuple(r) for r in indices.as_vec3_double()}) == indices.size()

        # return all(unique_reflections(m_a) for m_a in self.miller_arrays)

        self.miller_arrays[0].show_comprehensive_summary()

        self.miller_arrays[0].analyze_intensity_statistics().show()

    @property
    def labels(self):
        return [m_a.info().labels for m_a in self.miller_arrays]

    @property
    def miller_arrays(self):
        return self.reflection_data.as_miller_arrays()
