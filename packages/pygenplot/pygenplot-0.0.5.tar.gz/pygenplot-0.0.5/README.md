# pygenplot

### Overview
pygenplot is a python application for inspecting/plotting NetCDF/HDF/NeXuS files.

### Supported OS
- Linux
- MaCOS
- Windows

### Installation
Using pip:
- create a virtual environment: _virtualenv -p python3 MY_ENV_PATH_
- activate that environment: _source MY_ENV_PATH_/bin/activate_
- install pygenplot: _pip install pygenplot_
- run pygenplot: _pygenplot_

Using conda (only if you are inside the Institut Laue Langevin network):
- setup the no_proxy environment variable: _export no_proxy=cs.ill.fr_ (Unix) or _set no_proxy=cs.ill.fr_ (Windows)
- create a conda environment: _conda create -n MY_ENV python=3_
- activate that environment: _conda activate MY_ENV_
- install pygenplot: _conda install pygenplot -c https://cs.ill.fr/condapkg_ -c conda-forge
- run pygenplot: _pygenplot_

### Authors
pygenplot is developed and maintained by:
- Eric Pellegrini, Institut Laue Langevin (pellegrini[at]ill.fr)
- Remi Perenon, Institut Laue Langevin (perenon[at]ill.fr)
