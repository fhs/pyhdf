# $Id: setup.py,v 1.7 2007-02-11 22:14:52 gosselin_a Exp $
# $Name: not supported by cvs2svn $
# $Log: not supported by cvs2svn $
# Revision 1.6  2006/01/03 23:20:04  gosselin_a
# A bug was found in the pycdf-0.6-0 release shortly after it
# was made public. The new pycdf-0.6-1 release corrects that.
#
# Revision 1.5  2006/01/02 20:37:56  gosselin_a
# New pycdf-0.6-0 release.
#
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
NUMPY     = 3

nameDir = {
            NUMARRAY: "numarray",
            NUMERIC:  "numeric",
            NUMPY:    "numpy",
            }

USE  = NUMPY            # use the numpy package (default)
#USE = NUMERIC          # use the numeric package
#USE = NUMARRAY         # use the numarray package

import os, os.path, sys, shutil
from distutils.core import setup, Extension

if not USE in nameDir:
    print "USE set to an illegal value; set to one of: NUMPY (default), NUMERIC, NUMARRAY"
    sys.exit(1)
          
extName = "pycdf._pycdfext"
extDir  = os.path.join("pycdf", "pycdfext", nameDir[USE])
CCode   = [os.path.join(extDir, "pycdfext_wrap.c")]

if USE == NUMERIC:
    _pycdf_ext = Extension(extName, 
                           sources   = CCode,
                           #library_dirs=["non standard path where libs live"],
                           libraries = ["netcdf"])

elif USE == NUMARRAY:
    _pycdf_ext = Extension(extName, 
                           sources   = CCode,
                           #library_dirs=["non standard path where libs live"],
                           libraries = ["netcdf"])

elif USE == NUMPY:
    from numpy.distutils.misc_util import get_numpy_include_dirs
    _pycdf_ext = Extension(extName, 
                           sources   = CCode,
                           #library_dirs=["non standard path where libs live"],
                           include_dirs = get_numpy_include_dirs(), 
                           libraries = ["netcdf"])

toDir   = "pycdf"
shutil.copy(os.path.join(extDir, "pycdfext.py"), toDir)
shutil.copy(os.path.join(extDir, "pycdfext_array.py"), toDir)

setup(name         = 'pycdf',
      author       = 'Andre Gosselin',
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
      version      ='0.6-3',
      packages     = ['pycdf'],
      ext_modules  = [_pycdf_ext]

      )

# Cleanup
os.remove("pycdf/pycdfext.py")
os.remove("pycdf/pycdfext_array.py")
