#!/usr/bin/env python
"""
This defines the class GaussianFit defining a diffpy recipe for fitting a Gaussian curve to data.
A method is included to perform a leastsq fit.

Example usage is:

import numpy as np
x = np.arange(-10, 10, 0.1)
x0, sig = -2, 1.5
noise = 0.2 * np.ones_like(x)
y = np.exp(-0.5*(x-x0)**2/sig**2) + noise * np.random.randn(*x.shape)
gfit = GaussianFit(x, y, noise)
gfit.refine()
gfit.plot()

x, y, dy are the data to be fitted with Gaussian peak (dy may be omitted)
A, sig, and x0 are initial values.  If omitted the program will estimate
their starting values.

"""

from __future__ import print_function
from diffpy.srfit.fitbase import FitContribution, FitRecipe, Profile, FitResults
import numpy as np
import matplotlib.pyplot as plt

class GaussianFit(object):
    '''Least-squares fit of Gauss function to the specified data.

    Input and simulated data (read-only):

    x    --  input x values
    y    --  input y values
    dy   --  estimated standard deviations for the y-values
    yg   --  Gauss function calculated for the current A, sig, x0

    Parameters of the Gauss function:

    A    --  integrated area of the fitted peak
    sig  --  width of curve (parameter sigma in the Gauss distribution
             function)
    x0   --  x-position of the peak center

    Fit-related objects:

    results -- result report from the last refinement, refined values,
             and their estimated errors, parameter correlations, etc.
    recipe -- FitRecipe from SrFit that manages this refinement
    '''

    def __init__(self, x, y, dy=None, A=None, sig=None, x0=None):
        '''Create new GaussianFit object

        x, y -- curve to be fitted with Gaussian peak.
        dy   -- estimated standard deviations for the y-values
                (may be omitted).
        A, sig, x0   -- optional initial parameters for the Gauss function.
                Omitted parameters will be estimated from the input data.
        '''
        self.results = None
        self._makeRecipe(x, y, dy)
        if None in (A, sig, x0):
            self._getStartingValues()
        if A is not None:  self.A = A
        if sig is not None:  self.sig = sig
        if x0 is not None:  self.x0 = x0
        print('Initial parameter values:')
        self.printValues()
        return

    @property
    def x(self):
        return self.recipe.g1.profile.x

    @property
    def y(self):
        return self.recipe.g1.profile.y

    @property
    def dy(self):
        return self.recipe.g1.profile.dy

    @property
    def A(self):
        return self.recipe.A.value

    @A.setter
    def A(self, value):
        self.recipe.A = value
        return

    @property
    def sig(self):
        return self.recipe.sig.value

    @sig.setter
    def sig(self, value):
        self.recipe.sig = value
        return

    @property
    def x0(self):
        return self.recipe.x0.value

    @x0.setter
    def x0(self, value):
        self.recipe.x0 = value
        return

    @property
    def yg(self):
        return self.recipe.g1.evaluate()

    def _getStartingValues(self):
        '''Estimate starting values for A, sig, and x0
        '''
        from numpy import sqrt, log, pi
        x, y = self.x, self.y
        peakIndex = y.argmax()
        peakValue = y[peakIndex]
        self.x0 = x[peakIndex]
        halfmaxlo = (y < peakValue/2) & (x < self.x0)
        xhalflo = x[halfmaxlo][-1] if halfmaxlo.any() else x.min()
        halfmaxhi = (y < peakValue/2) & (x > self.x0)
        xhalfhi = x[halfmaxhi][0] if halfmaxhi.any() else x.max()
        fwhm = xhalfhi - xhalflo
        self.sig = fwhm / (2 * sqrt(2 * log(2)))
        self.A = peakValue * sqrt(2 * pi) * self.sig
        return


    def _makeRecipe(self, x, y, dy):
        '''Make a FitRecipe for fitting a Gaussian curve to data.
        '''
        profile = Profile()
        profile.setObservedProfile(x, y, dy)
        contribution = FitContribution("g1")
        contribution.setProfile(profile, xname="x")
        contribution.registerStringFunction(
                '1/sqrt(2 * pi * sig**2)', name='gaussnorm')
        contribution.setEquation(
                "A * gaussnorm * exp(-0.5 * (x - x0)**2/sig**2)")
        recipe = FitRecipe()
        recipe.addContribution(contribution)
        recipe.addVar(contribution.A)
        recipe.addVar(contribution.x0)
        recipe.addVar(contribution.sig)
        recipe.clearFitHooks()
        self.recipe = recipe
        return


    def printValues(self):
        '''Print out values of Gaussian parameters
        '''
        print('A =', self.A)
        print('sig =', self.sig)
        print('x0 =', self.x0)
        return


    def get_plot(self):
        '''Plot the input data and the best fit.
        '''
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.plot(self.x, self.y, 'b.', label="observed Gaussian")
        ax.plot(self.x, self.yg, 'g-', label="calculated Gaussian")
        ax.legend()
        return ax


    def refine(self):
        '''Optimize the recipe created above using scipy.
        '''
        from scipy.optimize.minpack import leastsq
        leastsq(self.recipe.residual, self.recipe.values)
        self.results = FitResults(self.recipe)
        print("Fit results:\n")
        print(self.results)
        return

# end of class GaussianFit

# Define functions that are used in gaussian fitting workflows

plt.ion()
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)
 
def generate_data(x0):
    x = np.arange(-20, 20, 0.1)
    sig = 1.5
    noise = 0.2 * np.ones_like(x)
    y = np.exp(-0.5*(x-x0)**2/sig**2) + noise * np.random.randn(*x.shape)
    plt.pause(1)
    dat = (x, y)
    return dat

def plot_data(dat):
    x, y = dat[0], dat[1]
    #f1 = plt.figure(1)
    #plt.ion(); plt.clf()
    ax1.cla()
    line1 = ax1.plot(x, y, 'x')
    fig.canvas.draw()
    plt.pause(0.1)

def fit_data(dat):
    x, y = dat[0], dat[1]
    gfit = GaussianFit(x,y)
    gfit.refine()
    plt.pause(1)
    return gfit

def plot_fit(gfit):
    ax2.cla()
    l2a = ax2.plot(gfit.x, gfit.y, 'b.', label="observed Gaussian")
    l2b = ax2.plot(gfit.x, gfit.yg, 'g-', label="calculated Gaussian")
    ax2.legend()
    fig.canvas.draw()
    plt.pause(0.1)
