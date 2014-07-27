#!/usr/bin/env python

from __future__ import print_function
from pyhdf.six.moves import map

from numpy import *
from pyhdf.SD import *

import os

def txtToHDF(txtFile, hdfFile, varName, attr):
    """Inputs:
        txtFile = name of .txt file (passed as string)
        hdfFile = name of .hdf file (passed as string)
        varName = name of dataset to be added (passed as string)
        attr = dataset attributes (passed as dictionary)
    txtFile indicates a dataset, and varName and attr give information
    about it.  txtToHDF puts this information into an SD (Scientific
    Dataset) object and stores that object as in hdfFile, creating
    hdfFile if need be, otherwise updating it.
    """

    try:  # Catch pyhdf errors
        # Open HDF file in update mode, creating it if non existent.
        d = SD(hdfFile, SDC.WRITE|SDC.CREATE)
        # Open text file and get matrix dimensions on first line.
        txt = open(txtFile)
        ni, nj = list(map(int, txt.readline().split()))
        # Define HDF dataset of type SDC.FLOAT32 with those dimensions.
        v = d.create(varName, SDC.FLOAT32, (ni, nj))
        # Assign attributes passed as argument inside dict `attr'.
        for attrName in list(attr.keys()):
            setattr(v, attrName, attr[attrName])
        # Load variable with lines of data. Compute min and max
        # over the whole matrix.
        i = 0
        while i < ni:
            elems = list(map(float, txt.readline().split()))
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
    except HDF4Error as msg:
        print("HDF4Error:", msg)

if __name__ == '__main__':
    hdfFile  = 'table.hdf'
    try:  # Delete if exists.
        os.remove(hdfFile)
    except:
        pass

    # Transfer contents of file 'temp.txt' to dataset 'temperature'
    # and assign the attributes 'title', 'units' and 'valid_range'.
    txtToHDF('temp.txt', hdfFile, 'temperature',
             {'title'      : 'temperature matrix',
              'units'      : 'celsius',
              'valid_range': (-2.8,27.0)})
    print("Temperature data successfully written to HDF file")

    # Transfer contents of file 'depth.txt' to dataset 'depth'
    # and assign the same attributes as above.
    txtToHDF('depth.txt', hdfFile, 'depth',
             {'title'      : 'depth matrix',
              'units'      : 'meters',
              'valid_range': (0, 500.0)})
    print("Depth data successfully written to HDF file")

    # TODO: open up hdfFile and access the information that
    # was in temp.txt and depth.txt
