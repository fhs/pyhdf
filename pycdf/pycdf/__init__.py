# $Id: __init__.py,v 1.4 2007-02-11 22:12:46 gosselin_a Exp $
# $Name: not supported by cvs2svn $
# $Log: not supported by cvs2svn $
# Revision 1.3  2006/01/02 18:51:15  gosselin_a
# The 'pycdf' directory has been restructured so as to allow
# installing pycdf with either the Numeric or numarray array packages.
# The directory top level now holds the package-independent
# python code. 'numeric' and 'numarray' directories hold the
# package-dependent parts.
#
# Revision 1.2  2005/07/16 16:22:35  gosselin_a
# pycdf classes are now 'new-style' classes (they derive from 'object').
# Added CVS keywords.
#

# Bring at the package level visible references from the
# pycdf module.
from pycdf import *

# Get rid of now useless references to the modules making up
# the package
del _pycdfext, pycdf, pycdfext, pycdfext_array


