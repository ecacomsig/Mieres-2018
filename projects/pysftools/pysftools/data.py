import collections
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
        self.miller_arrays = self.reflection_data.as_miller_arrays()

    def get(self, labels):
        """Get the :obj:`cctbx.miller.array` given a ``label``

        Parameters
        ----------
        labels : list, tuple
           A :obj:`list` or :obj:`tuple` of labels

        Returns
        -------
        :obj:`cctbx.miller.array`

        Raises
        ------
        :exc:`RuntimeError`
           Columns not found in MTZ

        """
        for m_a in self.miller_arrays:
            if m_a.info().labels == labels:
                return m_a
        raise RuntimeError("{} columns not found in {}".format(labels, self.reflection_file))

    def i2f(self, labels):
        """Intensities to amplitudes

        Parameters
        ----------
        labels : list, tuple
           A :obj:`list` or :obj:`tuple` of labels

        Returns
        -------
        :obj:`cctbx.miller.array`

        Raises
        ------
        :exc:`ValueError`
           Array is not an intensity array 

        """
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
    
    def write(self, fname):
        """Write the current data to a MTZ file

        Parameters
        ----------
        fname : str
           The file name to write the data to

        Raises
        ------
        :exc:`ValueError`
           Need more than 0 Miller array(s) 

        """
        if len(self.miller_arrays) < 1:
            raise ValueError('Need more than 0 Miller array(s)')
        base = self.miller_arrays[0]
        dataset = base.as_mtz_dataset(base.info().labels[0])
        for m_a in self.miller_arrays[1:]:
            dataset.add_miller_array(m_a, m_a.info().labels[0])
        dataset.mtz_object().write(file_name=fname)

    def checkhkl(self):
        """Print a summary

        Raises
        ------
        :exc:`NotImplementedError`

        """

        raise NotImplementedError
        #  stats = collections.defaultdict(dict)
        #  for m_a in self.miller_arrays:
        #      labels = tuple(m_a.info().labels)
        #      stats[labels]['minimum'] = min(m_a.data())
        #      stats[labels]['maximum'] = max(m_a.data())
        #      stats[labels]['average'] = sum(m_a.data()) / len(m_a.data())
        #      stats[labels]['resmax'],  stats[labels]['resmin'] = m_a.resolution_range()

    @property
    def labels(self):
        return [m_a.info().labels for m_a in self.miller_arrays]
