# $Id: setup.py,v 1.2 2004-08-02 15:05:02 gosselin Exp $
# $Log: not supported by cvs2svn $
# Revision 1.1  2004/08/02 14:45:56  gosselin
# Initial revision
#

# distutils setup file for the pyhdf package

from distutils.core import setup, Extension

# SD API
_hdfext =    Extension('pyhdf._hdfext', 
                       sources   = ["pyhdf/hdfext_wrap.c"],
		       #include_dirs=["non standard path where hdf includes live"],
		       #library_dirs=["non standard path where hdf libs live"],
		       #extra_objects=["extra stuff passed to the linker"],
		       libraries = ["mfhdf", "df", "jpeg", "z"])

setup(name         = 'pyhdf',
      author       = 'Andre Gosselin',
      author_email = 'gosselina@dfo-mpo.gc.ca',
      description  = 'Python interface to the NCSA HDF4 library',
      keywords     = ['hdf', 'netcdf', 'Numeric', 'python'],
      license      = 'public',
      long_description = 'The pyhdf package wraps the functionality '
                         'of the NCSA HDF4 library inside a Python OOP '
			 'framework. Only the SD API is implemented for '
			 'now, but other APIs will be covered in the '
			 'near future. SD variables are read/written '
			 'through Numeric arrays. netCDF files can also '
			 'be read and modified with pyhdf.',
      url          = 'ftp://nordet.qc.dfo-mpo.gc.ca/pub/soft/pyhdf',
      version      ='0.5-2',
      packages     = ['pyhdf'],
      ext_modules  = [_hdfext]
      )
