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
      version      ='0.5-2',
      packages     = ['pycdf'],
      ext_modules  = [_pycdf_ext]
      )
