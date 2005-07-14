# $Id: setup.py,v 1.6 2005-07-14 01:36:41 gosselin_a Exp $
# $Log: not supported by cvs2svn $
# Revision 1.5  2004/08/02 17:03:04  gosselin
# pyhdf-0.7-2
#
# Revision 1.4  2004/08/02 15:29:52  gosselin
# pyhdf-0.7-1
#
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
# Version: 0.7-3
# Date: July 13 2005

from distutils.core import setup, Extension
HDF_include  = "/usr/local/hdf-4.2r1/include"
HDF_lib      = "/usr/local/hdf-4.2r1/lib"

_hdfext =    Extension('pyhdf._hdfext', 
                       sources   = ["pyhdf/hdfext_wrap.c"],
		       include_dirs=[HDF_include],

		       # Define NOUINT if your version of Numeric does not support
		       # unsigned shorts or unsigned ints. Only versions 22 and above
		       # support those types.
		       # Define NOSZIP if your HDF4.2 library was compiled without SZIP
		       # support.
		       #extra_compile_args=["-DNOUINT"],
		       #extra_compile_args=["-DNOSZIP"],

		       library_dirs=[HDF_lib],
		       #extra_link_args=["extra stuff passed to the linker"],

		       # 'libraries' is set to the list of libraries to link
		       # against.
		       # Starting with version 4.2, the HDF distribution provides
		       # only the 'libmfhdf' and 'libdf' libraries. The 'libjpeg'
		       # and 'libz' libraires must be installed separately (on Linux
		       # those two libraries are generally part of a standard 
		       # distribution).
		       # Omit the "sz" entry (eg library 'libsz') if your HDF
		       # library was built without SZIP support.
		       # HDF built with SZIP support.
		       libraries = ["mfhdf", "df", "jpeg", "z", "sz"]
		       # HDF built without SZIP support.
		       #libraries = ["mfhdf", "df", "jpeg", "z"]
		       
		       )

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
      url          = 'www.sourceforge.net/projects/pysclint',
      version      = '0.7-3',
      packages     = ['pyhdf'],
      ext_modules  = [_hdfext]
      )
