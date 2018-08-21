from streamz_ext import Stream
from streamz_ext.graph import node_style, run_vis
import matplotlib.pyplot as plt

import numpy as np
from gaussianfit import GaussianFit

source = Stream()


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
    plt.ion(); plt.clf()
    plt.plot(x, y, 'x')
    plt.title('Two peaks simulated')
    plt.show()
    plt.pause(1)

def fit_data(dat):
    x, y = dat[0], dat[1]
    gfit = GaussianFit(x,y)
    gfit.refine()
    plt.pause(1)
    return gfit

def plot_fit(gfit):
    gfit.plot()
    plt.pause(1)


b = source.map(generate_data)
b.sink(plot_data)

c = b.map(fit_data)
c.sink(plot_fit)


gv = run_vis(
    source,
    source_node=True,
    edge_style={"color": "k"},
    node_label_style={"font_size": 15},
    edge_label_style=lambda x: {"label": x["label"], "font_size": 15},
    node_style=node_style,
    force_draw=True,
)
plt.pause(.1)

for i in range(10):
    try:
        source.emit(i)
        # plt.pause(10)
    except RuntimeError:
        pass
plt.show()
