# $Id: setup.py,v 1.4 2004-08-02 15:29:52 gosselin Exp $
# $Log: not supported by cvs2svn $
# Revision 1.3  2004/08/02 15:16:38  gosselin
# pyhdf 0.6-1
#
# Revision 1.2  2004/08/02 15:05:02  gosselin
# pyhdf 0.5.2
#
# Revision 1.1  2004/08/02 14:45:56  gosselin
# Initial revision
#

# distutils setup file for the pyhdf package
# Version: 0.7-1
# Date: FIXDATE

from distutils.core import setup, Extension

_hdfext =    Extension('pyhdf._hdfext', 
                       sources   = ["pyhdf/hdfext_wrap.c"],
		       #include_dirs=["non standard path where hdf includes live"],

		       # Uncomment if your version of Numeric does not support
		       # unsigned shorts or unsigned ints. Only versions 22 and above
		       # support those types.
		       #extra_compile_args=["-DNOUINT"],

		       #library_dirs=["non standard path where hdf libs live"],
		       #extra_link_args=["extra stuff passed to the linker"],
		       libraries = ["mfhdf", "df", "jpeg", "z"])

setup(name         = 'pyhdf',
      author       = 'Andre Gosselin',
      author_email = 'gosselina@dfo-mpo.gc.ca',
      description  = 'Python interface to the NCSA HDF4 library',
      keywords     = ['hdf', 'netcdf', 'Numeric', 'python'],
      license      = 'public',
      long_description = 'The pyhdf package wraps the functionality\n '
                         'of the NCSA HDF version 4 library inside a Python OOP\n '
			 'framework. The SD (scientific dataset), VS\n '
			 '(Vdata) and V (Vgroup) APIs are currently implemented.\n '
			 'Other APIs should be covered in the\n '
			 'near future. SD datasets are read/written\n '
			 'through Numeric arrays. netCDF files can also\n '
			 'be read and modified with pyhdf.',
      url          = 'ftp://nordet.qc.dfo-mpo.gc.ca/pub/soft/pyhdf',
      version      ='0.7-1',
      packages     = ['pyhdf'],
      ext_modules  = [_hdfext]
      )
