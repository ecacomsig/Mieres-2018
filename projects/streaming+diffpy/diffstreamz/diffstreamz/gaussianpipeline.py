from streamz_ext import Stream
from streamz_ext.graph import node_style, run_vis
import matplotlib.pyplot as plt

from diffstreamz.gaussianfitlib import generate_data, plot_data, fit_data, plot_fit

#Define the pipeline for gaussian fitting
def pipeline():
    pipeline = Stream()

    b = pipeline.map(generate_data)
    b.sink(plot_data)

    c = b.map(fit_data)
    c.sink(plot_fit)
    return pipeline
