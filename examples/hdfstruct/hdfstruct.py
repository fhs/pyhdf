#!/usr/bin/env python

from __future__ import print_function

import sys
from pyhdf.SD import *

# Dictionary used to convert from a numeric data type to its symbolic
# representation
typeTab = {
           SDC.CHAR:    'CHAR',
           SDC.CHAR8:   'CHAR8',
           SDC.UCHAR8:  'UCHAR8',
           SDC.INT8:    'INT8',
           SDC.UINT8:   'UINT8',
           SDC.INT16:   'INT16',
           SDC.UINT16:  'UINT16',
           SDC.INT32:   'INT32',
           SDC.UINT32:  'UINT32',
           SDC.FLOAT32: 'FLOAT32',
           SDC.FLOAT64: 'FLOAT64'
           }

printf = sys.stdout.write

def eol(n=1):
    printf("%s" % chr(10) * n)

hdfFile = sys.argv[1]    # Get first command line argument

try:  # Catch pyhdf.SD errors
    # Open HDF file named on the command line
    f = SD(hdfFile)
    # Get global attribute dictionary
    attr = f.attributes(full=1)
    # Get dataset dictionary
    dsets = f.datasets()

    # File name, number of attributes and number of variables.
    printf("FILE INFO"); eol()
    printf("-------------"); eol()
    printf("%-25s%s" % ("File:", hdfFile)); eol()
    printf("%-25s%d" % ("  file attributes:", len(attr))); eol()
    printf("%-25s%d" % ("  datasets:", len(dsets))); eol()
    eol();

    # Global attribute table.
    if len(attr) > 0:
        printf("File attributes"); eol(2)
        printf("  name                 idx type    len value"); eol()
        printf("  -------------------- --- ------- --- -----"); eol()
        # Get list of attribute names and sort them lexically
        attNames = sorted(attr.keys())
        for name in attNames:
            t = attr[name]
                # t[0] is the attribute value
                # t[1] is the attribute index number
                # t[2] is the attribute type
                # t[3] is the attribute length
            printf("  %-20s %3d %-7s %3d %s" %
                   (name, t[1], typeTab[t[2]], t[3], t[0])); eol()
        eol()


    # Dataset table
    if len(dsets) > 0:
        printf("Datasets (idx:index #, na:# attributes, cv:coord var)"); eol(2)
        printf("  name                 idx type    na cv dimension(s)"); eol()
        printf("  -------------------- --- ------- -- -- ------------"); eol()
        # Get list of dataset names and sort them lexically
        dsNames = sorted(dsets.keys())
        for name in dsNames:
            # Get dataset instance
            ds = f.select(name)
            # Retrieve the dictionary of dataset attributes so as
            # to display their number
            vAttr = ds.attributes()
            t = dsets[name]
                # t[0] is a tuple of dimension names
                # t[1] is a tuple of dimension lengths
                # t[2] is the dataset type
                # t[3] is the dataset index number
            printf("  %-20s %3d %-7s %2d %-2s " %
                   (name, t[3], typeTab[t[2]], len(vAttr),
                    ds.iscoordvar() and 'X' or ''))
            # Display dimension info.
            n = 0
            for d in t[0]:
                printf("%s%s(%d)" % (n > 0 and ', ' or '', d, t[1][n]))
                n += 1
            eol()
        eol()

        # Dataset info.
        printf("DATASET INFO"); eol()
        printf("-------------"); eol(2)
        for name in dsNames:
            # Access the dataset
            dsObj = f.select(name)
            # Get dataset attribute dictionary
            dsAttr = dsObj.attributes(full=1)
            if len(dsAttr) > 0:
                printf("%s attributes" % name); eol(2)
                printf("  name                 idx type    len value"); eol()
                printf("  -------------------- --- ------- --- -----"); eol()
                # Get the list of attribute names and sort them alphabetically.
                attNames = sorted(dsAttr.keys())
                for nm in attNames:
                    t = dsAttr[nm]
                        # t[0] is the attribute value
                        # t[1] is the attribute index number
                        # t[2] is the attribute type
                        # t[3] is the attribute length
                    printf("  %-20s %3d %-7s %3d %s" %
                           (nm, t[1], typeTab[t[2]], t[3], t[0])); eol()
                eol()
            # Get dataset dimension dictionary
            dsDim = dsObj.dimensions(full=1)
            if len(dsDim) > 0:
                printf ("%s dimensions" % name); eol(2)
                printf("  name                 idx len   unl type    natt");eol()
                printf("  -------------------- --- ----- --- ------- ----");eol()
                # Get the list of dimension names and sort them alphabetically.
                dimNames = sorted(dsDim.keys())
                for nm in dimNames:
                    t = dsDim[nm]
                        # t[0] is the dimension length
                        # t[1] is the dimension index number
                        # t[2] is 1 if the dimension is unlimited, 0 if not
                        # t[3] is the the dimension scale type, 0 if no scale
                        # t[4] is the number of attributes
                    printf("  %-20s %3d %5d  %s  %-7s %4d" %
                           (nm, t[1], t[0], t[2] and "X" or " ",
                            t[3] and typeTab[t[3]] or "", t[4])); eol()
                eol()


except HDF4Error as msg:
    print("HDF4Error", msg)
