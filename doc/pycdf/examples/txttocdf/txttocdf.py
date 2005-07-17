#!/usr/bin/env python

from Numeric import *
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
    
