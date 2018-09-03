from __future__ import division
import sys
from iotbx.reflection_file_reader import any_reflection_file
from iotbx import merging_statistics
from matplotlib import pylab
from matplotlib import cm
from math import sqrt, floor
from cctbx import miller
from collections import defaultdict


if __name__ == '__main__':

  # Read the mtz file
  reader = any_reflection_file(sys.argv[1])

  # Get the columns as miller arrays
  miller_arrays = reader.as_miller_arrays(merge_equivalents=False)

  # Select the desired columns
  intensities = None
  batches = None
  for array in miller_arrays:
    if array.info().labels == ['I', 'SIGI']:
      intensities = array
    if array.info().labels == ['BATCH']:
      batches = array
  assert intensities is not None
  assert batches is not None
  assert len(batches.data()) == len(intensities.data())

  # Compute the resolution of each reflection
  unit_cell = intensities.unit_cell()
  D = [unit_cell.d(h) for h in intensities.indices()]
  D2 = [1.0 / (d*d) for d in D]

  # Create the resolution bins
  print "Resolution Bins"
  min_D2, max_D2 = min(D2), max(D2)
  nbins = 1
  bin_range = max_D2 - min_D2
  bin_size = bin_range / nbins
  bins = []
  for i in range(nbins):
    b0, b1 = min_D2 + i * bin_size, min_D2 + (i+1)*bin_size
    print 1/sqrt(b0), 1/sqrt(b1)
    bins.append((b0,b1))

  def get_bin_index(h):
    d = unit_cell.d(h)
    d2 = 1/d**2
    bin_index = int(floor((d2 - min_D2) / bin_size))
    if bin_index == nbins:
      bin_index = nbins-1
    return bin_index

  cs = intensities.crystal_symmetry()
  ms = miller.set(cs, intensities.indices())
  ms_asu = ms.map_to_asu()
  asu_indices = ms_asu.indices()

  hkl = []
  batch = []
  intensity = []
  for i in range(len(asu_indices)):
    hkl.append(asu_indices[i])
    batch.append(batches.data()[i])
    intensity.append(intensities.data()[i])

  class Item(object):
    def __init__(self, h, batch, intensity):
      self.h = h
      self.batch = batch
      self.intensity = intensity

  data = defaultdict(list)
  data2 = defaultdict(list)
  for h, b, i in zip(hkl, batch, intensity):
    data[h].append(Item(h, b, i))
    data2[b].append(Item(h, b, i))

  class ReflectionSum(object):
    def __init__(self, sum_x=0, sum_x2=0, n=0):
      self.sum_x = sum_x
      self.sum_x2 = sum_x2
      self.n = n
  
  # Compute the Overall Sum(X) and Sum(X^2) for each reflection
  reflection_sums = defaultdict(ReflectionSum)
  for h in data.keys():
    I = [item.intensity for item in data[h]]
    sum_x = sum(I)
    sum_x2 = sum(II**2 for II in I)
    n = len(I)
    reflection_sums[h] = ReflectionSum(sum_x, sum_x2, n)
  
  class BinData(object):
    def __init__(self):
      self.mean = []
      self.var = []

  # Compute Mean and variance of reflection intensities
  bin_data = [BinData() for i in range(nbins)]
  for h in reflection_sums.keys():
    sum_x = reflection_sums[h].sum_x
    sum_x2 = reflection_sums[h].sum_x2
    n = reflection_sums[h].n
    mean = sum_x / n
    var = (sum_x2 - (sum_x)**2 / n) / (n-1)
    index = get_bin_index(h)
    bin_data[index].mean.append(mean)
    bin_data[index].var.append(var)

  def compute_cchalf(mean, var):
    assert len(mean) == len(var)
    n = len(mean)
    mean_of_means = sum(mean) / n
    sigma_e = sum(var) / n
    sigma_y = sum([(m - mean_of_means)**2 for m in mean]) / (n-1)
    cchalf = (sigma_y - 0.5*sigma_e)/(sigma_y + 0.5*sigma_e)
    return cchalf

  def compute_mean_cchalf_in_bins(bin_data):

    # Compute cchalf_overall
    mean_cchalf = 0
    count = 0
    for i in range(nbins):
      mean = bin_data[i].mean
      var = bin_data[i].var
      n = len(mean)
      # print mean, var
      cchalf = compute_cchalf(mean, var)
      #print cchalf, n
      mean_cchalf += n*cchalf
      count += n
    mean_cchalf /= count
    return mean_cchalf

  mean_cchalf = compute_mean_cchalf_in_bins(bin_data)
  cchalf_overall = mean_cchalf
  print ""
  print "# Reflections: ", len(D)
  print "# Unique: ", len(reflection_sums.keys())
  print "CC 1/2 Overall: ", mean_cchalf

  # Compute CC1/2 minus each batch
  cchalf_i = {}
  for batch in data2.keys():

    lookup = defaultdict(list)
    for item in data2[batch]:
      lookup[item.h].append(item)
  
    # Compute Mean and variance of reflection intensities
    bin_data = [BinData() for i in range(nbins)]
    for h in reflection_sums.keys():
      sum_x = reflection_sums[h].sum_x
      sum_x2 = reflection_sums[h].sum_x2
      n = reflection_sums[h].n

      for item in lookup[h]:
        sum_x -= item.intensity
        sum_x2 -= item.intensity**2
        n -= 1
      
      if n > 0:
        mean = sum_x / n
        var = (sum_x2 - (sum_x)**2 / n) / (n-1)
        index = get_bin_index(h)
        bin_data[index].mean.append(mean)
        bin_data[index].var.append(var)
  
    # Compute cchalf_overall
    mean_cchalf = compute_mean_cchalf_in_bins(bin_data)
    cchalf_i[batch] = mean_cchalf - cchalf_overall
    print "CC 1/2 %d" % batch, mean_cchalf

  batches = list(cchalf_i.keys())
  sorted_index = sorted(range(len(batches)), key=lambda x: cchalf_i[batches[x]])

  for i in sorted_index:
    print batches[i], cchalf_i[batches[i]]
  

  from matplotlib import pylab
  X = list(cchalf_i.values())
  pylab.hist(X)
  pylab.xlabel("CC 1/2")
  pylab.show()
