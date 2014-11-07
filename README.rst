.. image:: https://travis-ci.org/fhs/python-hdf4.svg?branch=master
    :target: https://travis-ci.org/fhs/python-hdf4

Overview
========

Python-HDF4 is a fork of pyhdf_ with some improvements:

- Various bug fixes: removes use of deprecated numpy API, python 2.7 compatibility, etc.
- Adds support for Python 3, while keeping compatibility with Python 2.
- Sphinx documentation

Python-HDF4 is a python wrapper around the NCSA HDF version 4 library.
The SD (Scientific Dataset), VS (Vdata) and V (Vgroup) API's 
are currently implemented. NetCDF files can also be
read and modified.

.. _pyhdf: http://pysclint.sourceforge.net/pyhdf/

Installation
============

To install, see http://fhs.github.io/python-hdf4/install.html
or file `doc/install.rst <doc/install.rst>`_.

Documentation
=============

For documentation, see http://fhs.github.io/python-hdf4/

Additional documentation on the HDF4 format can be
found in the User Guide:
http://www.hdfgroup.org/release4/doc/UsrGuide_html/UG_Top.html

Examples
========

Example python programs using the pyhdf package
can be found inside the examples/ subdirectory.
