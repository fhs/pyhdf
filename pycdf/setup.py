# $Id: setup.py,v 1.5 2006-01-02 20:37:56 gosselin_a Exp $
# $Name: not supported by cvs2svn $
# $Log: not supported by cvs2svn $
# Revision 1.4  2005/08/16 02:39:04  gosselin_a
# Addition of new features in preparation of release 0.6-0
#   -Support of CDF2 file format (64 bit file offsets).
#    Requires netCDF 3.6+.
#
# Revision 1.3  2005/08/15 02:00:29  gosselin_a
# pycdf-0.5-4 bug fix release. See CHANGES file.
#
# Revision 1.2  2005/07/16 17:01:18  gosselin_a
# pycdf-0.5-3
#   pycdf classes are now 'new-style' classes (they derive from 'object').
#   Updated documentation and admin files.
#

# distutils setup file for the pycdf package.


NUMERIC   = 1
NUMARRAY  = 2

USE = NUMERIC         # use the Numeric package (default)
#USE = NUMARRAY         # use the numarray package

import os, sys, shutil
from distutils.core import setup, Extension

if USE == NUMERIC:
    _pycdf_ext = Extension('pycdf._pycdfext', 
                           sources   = ["pycdf/pycdfext/numeric/pycdfext_wrap.c"],
                           #library_dirs=["non standard path where libs live"],
                           libraries = ["netcdf"])
    shutil.copy("pycdf/pycdfext/numeric/pycdfext.py", "pycdf")
    shutil.copy("pycdf/pycdfext/numeric/pycdfext_array.py", "pycdf")

elif USE == NUMARRAY:
    _pycdf_ext = Extension('pycdf._pycdfext', 
                           sources   = ["pycdf/pycdfext/numarray/pycdfext_wrap.c"],
                           #library_dirs=["non standard path where libs live"],
                           libraries = ["netcdf"])
    shutil.copy("pycdf/pycdfext/numarray/pycdfext.py", "pycdf")
    shutil.copy("pycdf/pycdfext/numarray/pycdfext_array.py", "pycdf")

else:
    print "USE set to an illegal value, please use NUMERIC or NUMARRAY"
    sys.exit(1)

setup(name         = 'pycdf',
      author       ='Andre Gosselin',
      author_email = 'gosselina@dfo-mpo.gc.ca',
      description  = 'Python interface to the Unidata netCDF library',
      keywords     = ['netcdf', 'python'],
      license      = 'public',
      long_description = 'The pycdf package wraps the complete '
                         'functionality of the Unidata netcdf library '
                         'inside a Python OOP framework. Variables are'
			 'read/written through arrays provided by the '
			 'Numeric or numarray package.',
      url          = 'http://pysclint.sourceforge.net/pycdf',
      version      ='0.6-0',
      packages     = ['pycdf'],
      ext_modules  = [_pycdf_ext]

      )
# Cleanup
os.remove("pycdf/pycdfext.py")
os.remove("pycdf/pycdfext_array.py")
