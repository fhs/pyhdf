# $Id: pycdfext_array.py,v 1.2 2007-02-11 22:09:06 gosselin_a Exp $
# $Name: not supported by cvs2svn $
# $Log: not supported by cvs2svn $
# Revision 1.1  2006/01/02 18:51:15  gosselin_a
# The 'pycdf' directory has been restructured so as to allow
# installing pycdf with either the Numeric or numarray array packages.
# The directory top level now holds the package-independent
# python code. 'numeric' and 'numarray' directories hold the
# package-dependent parts.
#

# Those imports are dependent on the 'numarray' package.
# They will be imported in turn by 'pycdf.py'.

__all__ = ["_ARRAYPKGNAME", "array", "_arrayPkg"]

_ARRAYPKGNAME = "numarray"
from numarray import array
import numarray as _arrayPkg
