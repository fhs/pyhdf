#!/usr/bin/env python
"""\
Suppose we have a series of text files each defining a 2-dimensional real
matrix. First line holds the matrix dimensions, and following lines hold
matrix values, one row per line. The following procedure will transfer to
a netCDF variable the contents of any one of those text files. The
procedure also computes the matrix min and max values, storing them as
variable attributes. It also assigns to the variable the group of
attributes passed as a dictionnary by the calling program. Note how simple
such an assignment becomes with pycdf: the dictionnary can contain any
number of attributes, of different types, single or multi-valued. Doing
the same in a conventional language would be much more challenging.

You can later use the "cdfstruct" program to analyse the contents of
the netCDF file produced by this example.

Error checking is minimal, to keep example as simple as possible
(admittedly a rather poor excuse ...).
"""

from pycdf import *

import os

def txtToCDF(txtFile, ncFile, varName, attr):

    try:
        # Open netCDF file in update mode, creating it if inexistent.
        nc = CDF(ncFile, NC.WRITE|NC.CREATE)
        # Automatically set define and data modes.
        nc.automode()
        # Open text file and get matrix dimensions on first line.
        txt = open(txtFile)
        ni, nj = map(int, txt.readline().split())
        # Defined netCDF dimensions.
        dimi = nc.def_dim(varName + '_i', ni)
        dimj = nc.def_dim(varName + '_j', nj)
        # Define netCDF variable of type FLOAT with those dimensions.
        var = nc.def_var(varName, NC.FLOAT, (dimi, dimj))
        # Assign attributes passed as argument inside dict `attr'.
        for attrName in attr.keys():
            setattr(var, attrName, attr[attrName])
        # Load variable with lines of data. Compute min and max
        # over the whole matrix.
        i = 0
        while i < ni:
            elems = map(float, txt.readline().split())
            var[i] = elems
            minE = min(elems)
            maxE = max(elems)
       	    if i:
	        minVal = min(minVal, minE)
	        maxVal = max(maxVal, maxE)
	    else:
	        minVal = minE
	        maxVal = maxE
            i += 1
        # Set variable min and max attributes.
        var.minVal = minVal
        var.maxVal = maxVal
        # Close files (not really necessary, since closing is
        # automatic when file objects go out of scope.
        nc.close()
        txt.close()
    except CDFError, msg:
        print "CDFError:", msg

if __name__ == '__main__':
    ncFile  = 'table.nc'
    try:  # Delete if exists.
        os.remove(ncFile)
    except:
        pass
    txtToCDF('temp.txt', ncFile, 'temperature',
             {'title'      : 'temperature matrix',
	      'units'      : 'celsius',
	      'valid_range': (-2.8,27.0)})

    txtToCDF('depth.txt', ncFile, 'depth',
             {'title'      : 'depth matrix',
	      'units'      : 'meters',
	      'valid_range': (0, 500.0)})
    
