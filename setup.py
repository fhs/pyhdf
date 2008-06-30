# $Id: setup.py,v 1.7 2008-06-30 02:41:44 gosselin_a Exp $
# $Log: not supported by cvs2svn $
# Revision 1.6  2005/07/14 01:36:41  gosselin_a
# pyhdf-0.7-3
# Ported to HDF4.2r1.
# Support for SZIP compression on SDS datasets.
# All classes are now 'new-style' classes, deriving from 'object'.
# Update documentation.
#
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
# Version: 0.8
# Date: July 1 2008

from numpy.distutils.core import setup, Extension

# Configure the appropriate include and library directories here.
include_dirs = ["/usr/include/hdf"]
library_dirs = ["/usr/lib/hdf"]

_hdfext =    Extension('pyhdf._hdfext', 
                       sources      = ["pyhdf/hdfext_wrap.c"],
		       include_dirs = include_dirs,

		       # Define NOSZIP if your HDF4.2 library was compiled without SZIP
		       # support. Define NOCOMPRESS if your HDF library reports errors
                       # related to SDgetcompress() / SDsetcompress() compression functions 
                       # (this may help users of Debian-based linux distributions). 
		       #extra_compile_args=["-DNOSZIP", "-DNOCOMPRESS"],
		       #extra_compile_args=["-DNOSZIP"],

		       library_dirs = library_dirs,
		       #extra_link_args=["extra stuff passed to the linker"],

		       # 'libraries' is set to the list of libraries to link
		       # against.
		       # Starting with version 4.2, the HDF distribution provides
		       # only the 'libmfhdf' and 'libdf' libraries. The 'libjpeg'
		       # and 'libz' libraries must be installed separately (on Linux
		       # those two libraries are generally part of a standard 
		       # distribution).
		       # Omit the "sz" entry (eg library 'libsz') if you have set
                       # either NOSZIP or NOCOMPRESS above.
		       libraries = ["mfhdf", "df", "jpeg", "z", "sz"]
		       # HDF built without SZIP support.
		       #libraries = ["mfhdf", "df", "jpeg", "z"]
		       
		       )

setup(name         = 'pyhdf',
      author       = 'Andre Gosselin',
      author_email = 'Andre.Gosselin@dfo-mpo.gc.ca',
      maintainer   = 'Robert Kern',
      maintainer_email = 'robert.kern@enthought.com',
      description  = 'Python interface to the NCSA HDF4 library',
      keywords     = ['hdf', 'netcdf', 'numpy', 'python', 'pyhdf', 'parse_odl'],
      license      = 'public',
      long_description = 'The pyhdf package wraps the functionality\n '
                         'of the NCSA HDF version 4 library inside a Python OOP\n '
			 'framework. The SD (scientific dataset), VS\n '
			 '(Vdata) and V (Vgroup) APIs are currently implemented.\n '
			 'SD datasets are read/written\n '
			 'through numpy arrays. netCDF files can also\n '
			 'be read and modified with pyhdf.'
                         '\n'
                         'The function parse_odl is also provided to\n'
                         'deal specifically with data in the ODL\n'
                         '(Object Desdription Language) format.',
      url          = 'www.sourceforge.net/projects/pysclint',
      version      = '0.8',
      packages     = ['pyhdf'],
      ext_modules  = [_hdfext]
      )
