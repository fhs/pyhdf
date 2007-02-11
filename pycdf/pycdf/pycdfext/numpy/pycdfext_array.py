# $Id: pycdfext_array.py,v 1.1 2007-02-11 22:07:33 gosselin_a Exp $
# $Name: not supported by cvs2svn $
# $Log: not supported by cvs2svn $

# Those imports are dependent on the 'numpy' package.
# They will be imported in turn by 'pycdf.py'.

__all__ = ["_ARRAYPKGNAME", "array", "_arrayPkg"]

_ARRAYPKGNAME = "numpy"
from numpy import array
import numpy as _arrayPkg
