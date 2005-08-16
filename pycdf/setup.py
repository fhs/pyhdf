# $Id: setup.py,v 1.4 2005-08-16 02:39:04 gosselin_a Exp $
# $Name: not supported by cvs2svn $
# $Log: not supported by cvs2svn $
# Revision 1.3  2005/08/15 02:00:29  gosselin_a
# pycdf-0.5-4 bug fix release. See CHANGES file.
#
# Revision 1.2  2005/07/16 17:01:18  gosselin_a
# pycdf-0.5-3
#   pycdf classes are now 'new-style' classes (they derive from 'object').
#   Updated documentation and admin files.
#

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
      url          = 'http://pysclint.sourceforge.net/pycdf',
      version      ='0.5-5',
      packages     = ['pycdf'],
      ext_modules  = [_pycdf_ext]
      )
