# /usr/bin/env python

# $Id: setup.py,v 1.2 2005-02-10 23:11:12 gosselin_a Exp $
# $Name: not supported by cvs2svn $
# $Log: not supported by cvs2svn $
# Revision 1.1.1.1  2005/02/10 22:54:03  gosselin_a
# Initial import of the mpy package
#
# Folowing logs refer to an earlier CVS repository used to
# host "mpy" at the Maurice-Lamontagne Institute.

# Revision 1.2  2005/01/08 18:13:44  gosselin_a
# First version of the mpy package.
# Supports almost all functions in the point-to-point and collective
# message passing category, plus those for group manipulation.
#
# Revision 1.1.1.1  2005/01/07 22:40:32  gosselin_a
# First release of the mpy python package.
# Still lacks most of the communicator-related functions.
#

from distutils.core import setup, Extension
from Pyrex.Distutils import build_ext

mpy  = Extension("mpy",         # <-- replace with the basename of the pyrex file
                 sources = ["mpy.pyx"],
		 libraries= ['pthread', 
		             'lammpio',         # Lam environment
			     'lamf77mpi', 
			     'mpi',             # the mpi library
			     'lam', 
			     'util', 
			     'dl'] 
	         )

setup(name = 'mpy',
      ext_modules = [mpy],      # must match the name of the Extension object
                                # created above
      cmdclass    = {'build_ext': build_ext}   # use the Pyrex.Distutils.build_ext rules
     )
