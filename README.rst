OVERVIEW
========

python-hdf4 is a fork of pyhdf_ with some improvements:
  * Removes use of deprecated numpy API
  * Adds support for Python 3, while keeping compatibility with Python 2.
  * Planned: unit tests
  * Planned: better (sphinx) documentation

python-hdf4 is a python wrapper around the NCSA HDF version 4 library.
The SD (Scientific Dataset), VS (Vdata) and V (Vgroup) API's 
are currently implemented. netCDF files can also be 
read and modified.

.. _pyhdf: http://pysclint.sourceforge.net/pyhdf/

INSTALLATION
============

  To install, see file INSTALL.

DOCUMENTATION
=============

  For documentation, see the doc/ subdirectory:
    * pyhdf.HDF.txt  text format
    * pyhdf.HDF.html html format
    * pyhdf.SD.txt   text format
    * pyhdf.SD.html  html format
    * pyhdf.VS.txt   text format
    * pyhdf.VS.html  html format
    * pyhdf.V.txt    text format
    * pyhdf.V.html   html format

  Additional documentation on the HDF4 format can be
  found in the User Guide:
    http://hdf.ncsa.uiuc.edu/training/HDFtraining/UsersGuide/

EXAMPLES
========

  Example python programs using the pyhdf package
  can be found inside the examples/ subdirectory.
