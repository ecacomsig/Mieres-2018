# Directory for streaming data project

People: Duncan, Simon Nadia

Goal: make a simple pipeline to learn how to code a simple streaming data pipeline

Approach: 
 1. Install ``streamz_ext`` from ``conda-forge`` channel of conda in a p3 env.
 1. try and run the ``live_plot.py`` example in the examples directory (this 
 was taken from the examples in the ``xpdAcq/streamz_ext`` GitHub repo)
 1. installation
   1. p3 conda environment for hyperspy, used to generate fake data
   1. p3 conda environment for diffpy and streamz_ext.  install diffpy using the instructions below.  Install streamz_ext from sources (clone ``xpdAcq/streamz_ext`` then in the directory with setup.py type ``python setup.py develop``).  Install grave from sources (clone ``networkx/grave`` then in the directory with setup.py type ``python setup.py develop``).
 
 Log:
 1. working on a bug....``live_plot`` won't install ``node_style`` and we have no
 idea why....
   1. must install using setup develop
   
 
 
 Diffpy development Python 3 install instructions:
 ```
 conda install -c diffpy/channel/dev -c diffpy diffpy-cmi
 ```
