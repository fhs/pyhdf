#!/usr/bin/env python

from Numeric import *
from pyhdf.SD import *

import os

def txtToHDF(txtFile, hdfFile, varName, attr):

    try:  # Catch pyhdf errors
        # Open HDF file in update mode, creating it if non existent.
        d = SD(hdfFile, SDC.WRITE|SDC.CREATE)
        # Open text file and get matrix dimensions on first line.
        txt = open(txtFile)
        ni, nj = map(int, txt.readline().split())
        # Define HDF dataset of type SDC.FLOAT32 with those dimensions.
        v = d.create(varName, SDC.FLOAT32, (ni, nj))
        # Assign attributes passed as argument inside dict `attr'.
        for attrName in attr.keys():
            setattr(v, attrName, attr[attrName])
        # Load variable with lines of data. Compute min and max
        # over the whole matrix.
        i = 0
        while i < ni:
            elems = map(float, txt.readline().split())
            v[i] = elems
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
        v.minVal = minVal
        v.maxVal = maxVal
        # Close dataset and file objects (not really necessary, 
	# since closing is automatic when objects go out of scope.
	v.endaccess()
        d.end()
        txt.close()
    except HDF4Error, msg:
        print "HDF4Error:", msg

if __name__ == '__main__':
    hdfFile  = 'table.hdf'
    try:  # Delete if exists.
        os.remove(hdfFile)
    except:
        pass

    # Transfer contents of file 'temp.txt' to dataset 'temperature'
    # an assign the attributes 'title', 'units' and 'valid_range'.
    txtToHDF('temp.txt', hdfFile, 'temperature',
             {'title'      : 'temperature matrix',
	      'units'      : 'celsius',
	      'valid_range': (-2.8,27.0)})

    # Transfer contents of file 'depth.txt' to dataset 'depth'
    # an assign the same attributes as above.
    txtToHDF('depth.txt', hdfFile, 'depth',
             {'title'      : 'depth matrix',
	      'units'      : 'meters',
	      'valid_range': (0, 500.0)})
    
