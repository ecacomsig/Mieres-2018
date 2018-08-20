#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''SrFit example for two Gaussian peaks to a noisy data.
This script can be run in IPython "demo" mode.  To use the demo mode,
start IPython and execute the following commands:

In [1]: %run ex03.py demo
In [2]: demo()
...
In [3]: demo()

'''

# Define "demo" object and exit if run with a single argument "demo".
from __future__ import print_function
import sys
if __name__ == '__main__' and sys.argv[1:] == ['demo']:
    from IPython.lib.demo import ClearDemo
    demo = ClearDemo(__file__)
    demo.seek(1)
    print('Created "demo" object.  Use "demo()" to run the next section.')
    sys.exit()

# <demo> auto_all
# <demo> silent
# <demo> --- stop ---

# Simulate linear data with some random Gaussian noise.

import numpy as np
xobs = np.arange(0,1024,1)*0.1
yobs = np.loadtxt('../data/two_peaks.txt', delimiter=',')


# Plot the generated "observed" data (xobs, yobs).
import matplotlib.pyplot as plt
plt.ion(); plt.clf(); plt.hold(False)
plt.plot(xobs, yobs, 'x')
plt.title('Two peaks simulated')
plt.show()

# <demo> --- stop ---

# We are going to define a line fitting regression using SrFit.
# At first we create a SrFit Profile object that holds the observed data.

from diffpy.srfit.fitbase import Profile
profile = Profile()
profile.setObservedProfile(xobs, yobs)

# The second step is to create a FitContribution object, which associates
# observed profile with a mathematical model for the dependent variable.

from diffpy.srfit.fitbase import FitContribution
large_gaussian = FitContribution("g1")
large_gaussian.setProfile(profile, xname="x")
large_gaussian.registerStringFunction(
        '1/sqrt(2 * pi * lgsig**2)', name='gaussnorm')
large_gaussian.setEquation(
        "lgA * gaussnorm * exp(-0.5 * (x - lgx0)**2/lgsig**2)")

small_gaussian = FitContribution("g2")
small_gaussian.setProfile(profile, xname="x")
small_gaussian.registerStringFunction(
        '1/sqrt(2 * pi * sgsig**2)', name='gaussnorm')
small_gaussian.setEquation(
        "sgA * gaussnorm * exp(-0.5 * (x - sgx0)**2/sgsig**2)")

# SrFit objects can be examined by calling their show() function.  SrFit
# parses the model equation and finds two parameters A, B at independent
# variable x.  The values of parameters A, B are at this stage undefined.

large_gaussian.show()
small_gaussian.show()

# <demo> --- stop ---

# We can set A and B to some specific values and calculate model
# observations.  The x and y attributes of the FitContribution are
# the observed values, which may be re-sampled or truncated to a shorter
# fitting range.

large_gaussian.lgA = 25000
large_gaussian.lgx0 = 40
large_gaussian.lgsig = 20
small_gaussian.sgA = 500
small_gaussian.sgx0 = 71
small_gaussian.sgsig = 3

print(large_gaussian.lgA, large_gaussian.lgA.value)
print(large_gaussian.lgx0, large_gaussian.lgx0.value)
print(large_gaussian.lgsig, large_gaussian.lgsig.value)
print(small_gaussian.sgA, small_gaussian.sgA.value)
print(small_gaussian.sgx0, small_gaussian.sgx0.value)
print(small_gaussian.sgsig, small_gaussian.sgsig.value)

# <demo> --- stop ---

# linefit.evaluate() returns the modeled values and linefit.residual
# the difference between observed and modeled data scaled by estimated
# standard deviations.

print("large_gaussian.evaluate() =", large_gaussian.evaluate())
print("large_gaussian.residual() =", large_gaussian.residual())
print("small_gaussian.evaluate() =", small_gaussian.evaluate())
print("small_gaussian.residual() =", small_gaussian.residual())
plt.plot(xobs, yobs, 'x', profile.x, large_gaussian.evaluate(), '-', profile.x, small_gaussian.evaluate())
plt.title('Two Gaussians simulated at A=25000, x0=40, sig=20 and A=500, x0=68, sig=3')

# <demo> --- stop ---

# We want to find optimum model parameters that fit the simulated curve
# to the observations.  This is done by associating FitContribution with
# a FitRecipe object.  FitRecipe can manage multiple fit contributions and
# optimize all models to fit their respective profiles.

from diffpy.srfit.fitbase import FitRecipe
recipe = FitRecipe()

# clearFitHooks suppresses printout of iteration number
recipe.clearFitHooks()

recipe.addContribution(large_gaussian)
recipe.addContribution(small_gaussian)

recipe.show()

# <demo> --- stop ---

# FitContributions may have many parameters.  We need to tell the recipe
# which of them should be tuned by the fit.

recipe.addVar(large_gaussian.lgA)
recipe.addVar(large_gaussian.lgx0)
recipe.addVar(large_gaussian.lgsig)

recipe.addVar(small_gaussian.sgA)
recipe.addVar(small_gaussian.sgx0)
recipe.addVar(small_gaussian.sgsig)


# The addVar function created two attributes A, B for the rec object
# which link ot the A and B parameters of the large Gaussian contribution.

# print("recipe.A =", recipe.A)
# print("recipe.A.value =", recipe.A.value)

# The names of the declared variables are stored in a rec.names
# and the corresponding values in rec.values.

# print("recipe.values =", recipe.values)
# print("recipe.names =", recipe.names)

# Finally the recipe objects provides a residual() function to calculate
# the difference between the observed and simulated values.  The residual
# function can accept a list of new variable values in the same order as
# rec.names.

print("recipe.residual() =", recipe.residual())
print("recipe.residual([290000, 51, 29, 500, 71, 3]) =", recipe.residual([290000, 51, 29, 500, 68, 3]))

# <demo> --- stop ---

# The FitRecipe.residual function can be directly used with the scipy
# leastsq function for minimizing a sum of squares.

from scipy.optimize import leastsq
leastsq(recipe.residual, recipe.values)

# Recipe variables and the linked line-function parameters are set to the
# new optimized values.

print(recipe.names, "-->", recipe.values)
large_gaussian.show()
small_gaussian.show()

# The calculated function is available in the ycalc attribute of the profile.
# It can be also accessed from the "linefit" contribution attribute of the
# recipe as "rec.linefit.profile.ycalc".
plt.plot(profile.x, profile.y, 'x', profile.x, profile.ycalc, '-')
plt.title('Line fit using the leastsq least-squares optimizer')

# <demo> --- stop ---

# The FitRecipe.scalarResidual function returns the sum of squares and can
# be used with a minimizer that expects scalar function:

from scipy.optimize import fmin
fmin(recipe.scalarResidual, [1, 1])
print(recipe.names, "-->", recipe.values)
plt.plot(profile.x, profile.y, 'x', profile.x, profile.ycalc, '-')
plt.title('Line fit using the fmin scalar optimizer')

# <demo> --- stop ---

# For a converged fit recipe, the details of the fit can be extracted
# with the FitResults class.

from diffpy.srfit.fitbase import FitResults
res = FitResults(recipe)
print(res)

# <demo> --- stop ---

# Variables defined in the recipe can be fixed to a constant value.

recipe.fix(lgx0=51)

# The fixed variables can be checked using the "fixednames" and
# "fixedvalues" attributes of a recipe.
print("free:", recipe.names, "-->", recipe.names)
print("fixed:", recipe.fixednames, "-->", recipe.fixedvalues)

# The fit can be rerun with a constant variable B.
leastsq(recipe.residual, recipe.values)
print(FitResults(recipe))
plt.plot(profile.x, profile.y, 'x', profile.x, profile.ycalc, '-')
plt.title('Line fit for variable x0 fixed to x0=51')

# <demo> --- stop ---

# Fixed variables may be released with the "free" function.
# free("all") releases all fixed variables.
recipe.free('all')

arst = recipe.restrain(recipe.lgx0, lb=48, ub=52, sig=0.01)

# Perform fit with the line slope restrained to a maximum value of 0.2:
leastsq(recipe.residual, recipe.values)
print(FitResults(recipe))
plt.plot(profile.x, profile.y, 'x', profile.x, profile.ycalc, '-')
plt.title('Line fit with x0 restrained to the range 48 to 52')
