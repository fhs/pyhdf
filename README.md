[![Build Status](https://travis-ci.org/fhs/pyhdf.svg?branch=master)](https://travis-ci.org/fhs/pyhdf)

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
0.10.0 and onwards, please install `pyhdf` instead of `python-hdf4`.

## Installation

To install, see http://fhs.github.io/pyhdf/install.html
or file [doc/install.rst](doc/install.rst).

## Documentation

For documentation, see http://fhs.github.io/pyhdf/

Additional documentation on the HDF4 format can be
found in the User Guide:
http://www.hdfgroup.org/release4/doc/UsrGuide_html/UG_Top.html

## Examples

Example python programs using the pyhdf package
can be found inside the examples/ subdirectory.
