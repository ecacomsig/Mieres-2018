from streamz_ext.graph import node_style, run_vis
import matplotlib.pyplot as plt

from diffstreamz.gaussianpipeline import pipeline

#Define the pipeline
pipeline = pipeline()

#Emit data into pipeline source node
def main():
    for i in range(10):
        try:
            pipeline.emit(i)
        except RuntimeError:
            pass
    plt.show()

#Define visualisation kwargs
gvkwargs = dict(source_node=True,
                edge_style={"color": "k"},
                node_label_style={"font_size": 15},
                edge_label_style=lambda x: {"label": x["label"], "font_size": 15},
                node_style=node_style,
                force_draw=True)

#Run pipeline and visualisation
if __name__ == "__main__":
    run_vis(pipeline, **gvkwargs)
    main()
