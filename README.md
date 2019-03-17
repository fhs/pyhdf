[![Build Status](https://travis-ci.org/fhs/pyhdf.svg?branch=master)](https://travis-ci.org/fhs/pyhdf)
[![Build status](https://ci.appveyor.com/api/projects/status/4a8pf8vo8nrjgxol/branch/master?svg=true)](https://ci.appveyor.com/project/fhs/pyhdf/branch/master)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/pyhdf/badges/version.svg)](https://anaconda.org/conda-forge/pyhdf)

# pyhdf

pyhdf is a python wrapper around the NCSA HDF version 4 library.
The SD (Scientific Dataset), VS (Vdata) and V (Vgroup) API's 
are currently implemented. NetCDF files can also be
read and modified. It supports both Python 2 and Python 3.

*Note:* The sourceforge pyhdf
[website](http://pysclint.sourceforge.net/pyhdf/) and
[project](https://sourceforge.net/projects/pysclint/) are out-of-date.
The original author of pyhdf have abandoned the project and it is
currently maintained in [github](https://github.com/fhs/pyhdf).

Version 0.9.x was called
[python-hdf4](https://pypi.org/project/python-hdf4/)
in PyPI because at that time we didn't have
[access](https://github.com/pypa/warehouse/issues/5157) to the
[pyhdf package](https://pypi.org/project/pyhdf/) in PyPI.  For version
0.10.0 and onward, please install `pyhdf` instead of `python-hdf4`.

## Installation

See [pyhdf installation instructions](http://fhs.github.io/pyhdf/install.html)
or [doc/install.rst](doc/install.rst).

## Documentation

See [pyhdf documentation](http://fhs.github.io/pyhdf/).

Additional documentation on the HDF4 format can be found in the
[HDF4 Support Page](https://portal.hdfgroup.org/display/HDF4/HDF4).

## Examples

Example python programs using the pyhdf package
can be found inside the [examples/](examples/) subdirectory.
