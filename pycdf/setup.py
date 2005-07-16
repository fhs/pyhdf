# $Id: setup.py,v 1.2 2005-07-16 17:01:18 gosselin_a Exp $
# $Name: not supported by cvs2svn $
# $Log: not supported by cvs2svn $

# distutils setup file for the pycdf package.

from distutils.core import setup, Extension

_pycdf_ext = Extension('pycdf._pycdfext', 
                       sources   = ["pycdf/pycdfext_wrap.c"],
		       #library_dirs=["non standard path where libs live"],
		       libraries = ["netcdf"])

setup(name         = 'pycdf',
      author       ='Andre Gosselin',
      author_email = 'gosselina@dfo-mpo.gc.ca',
      description  = 'Python interface to the Unidata netCDF library',
      keywords     = ['netcdf', 'python'],
      license      = 'public',
      long_description = 'The pycdf package wraps the complete '
                         'functionality of the Unidata netcdf library '
                         'inside a Python OOP framework. Variables are'
			 'read/written through Numeric arrays.',
      url          = 'ftp://nordet.qc.dfo-mpo.gc.ca/pub/soft/pycdf',
      version      ='0.5-3',
      packages     = ['pycdf'],
      ext_modules  = [_pycdf_ext]
      )
