from __future__ import division

import math

from scitbx.array_family import flex
from scitbx.lstbx import normal_eqns, normal_eqns_solving

n = 45 # data points

# 4 model parameters
# Model M(x, t) = x2 e^{x0 t} + x3 e^{x1 t}
# Problem 18 from Nielsen's collection
def model(x, t, only_value):
  exp_x0_t = math.exp(x[0]*t)
  exp_x1_t = math.exp(x[1]*t)
  value = x[2]*exp_x0_t + x[3]*exp_x1_t
  if not only_value:
    derivatives = (t*x[2]*exp_x0_t,
                   t*x[3]*exp_x1_t,
                   exp_x0_t,
                   exp_x1_t)
    return (value, derivatives)
  else:
    return value

# t: independent variable (like hkl in intro)
# = [0.02, 0.04, 0.06, ..., 0.9]
t = 0.02*flex.double_range(1, n + 1)

#noise = flex.double(n) # zeroes
noise = 1e-5*(2*flex.random_double(n) - 1) # between -1 and 1

# Generate data
x_star = (-4, -5, 4, -4)
yo = flex.double(n)
for i in xrange(n):
  yo[i] = model(x_star, t[i], only_value=True) + noise[i]
print "Data"
for ind, dep in zip(t, yo):
  print ind, dep
print

x_0 = (-1, -2, 1, -1) # starting point
print "Start from {}".format(x_0)
print

class my_fit(normal_eqns.non_linear_ls,
             normal_eqns.non_linear_ls_mixin):
  """ Describe the problem above to lstbx

      We could have used non_linear_ls_with_separable_scale_factor
  """

  def __init__(self, independent, dependent, model, start):
    """ Specific to this class """
    super(my_fit, self).__init__(n_parameters=len(start))
    self.t = independent
    self.yo = dependent
    self.model = model
    self.x_0 = start
    self.restart()

  def restart(self):
    """ Called when the L.S. needs to restart from scratch """
    self.x = self.x_0.deep_copy()
    self.old_x = None

  def step_forward(self):
    """ Called after a step has been computed """
    self.old_x = self.x.deep_copy()
    self.x += self.step()

  def step_backward(self):
    """ Called when a step has to be reverted """
    self.x, self.old_x = self.old_x, None

  def parameter_vector_norm(self):
    """ Euclidean length of parameter vector """
    return self.x.norm()

  def build_up(self, objective_only=False):
    """ Workhorse: compute least-squares
    and derivatives if asked """
    self.reset()
    n = self.n_parameters
    m = self.t.size() # number of data points
    residuals = flex.double(m) #
    if objective_only:
      for i in xrange(m):
        yc_i = self.model(self.x, t[i], only_value=True)
        residuals[i] = yc_i - self.yo[i]
      self.add_residuals(residuals, weights=None)
    else:
      # each row = derivatives of one L.S. term
      derivatives = flex.double(flex.grid(m, n))
      for i in xrange(m):
        yc_i, der_yc_i = self.model(self.x, t[i],
                                    only_value=False)
        residuals[i] = yc_i - self.yo[i]
        for j in xrange(n):
          derivatives[i, j] = der_yc_i[j]
      self.add_equations(residuals, derivatives, weights=None)


test = my_fit(t, yo, model, flex.double(x_0))
runs = normal_eqns_solving.levenberg_marquardt_iterations(
  test,
  track_all=True,
  gradient_threshold=1e-8,
  step_threshold=1e-8,
  tau=1e-4,
  n_max_iterations=200)
# other choices:`
# - naive_iterations
# - naive_iterations_with_damping
# - naive_iterations_with_damping_and_shift_limit
print "#iterations: {}".format(runs.n_iterations)
print "Fitted parameters: {}".format(tuple(test.x))
print
print 'OK'
