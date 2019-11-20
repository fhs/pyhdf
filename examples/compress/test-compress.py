#!/usr/bin/env python

from __future__ import print_function

# Generate test HDF files using different compression configurations,
# and validate each resulting file to make sure its contents is OK.
# Adapted from example:
# "https://support.hdfgroup.org/doc_resource/SZIP/h4_examples/szip32.c".
# A bigger dataset is defined to better show the size reduction achieved
# by the SZIP compression.
# Note that when applied to HDF4 SDS, the word "pixels" as used inside
# the SZIP documentation should really be understood as a "data element",
# eg a cell value inside a multidimensional array.
#
# On our systems, the program produced the following file sizes :
#
# $ ls -l *.hdf
#    -rw-r--r-- 1 root root  53389 Jun 29 14:20 SDS.COMP_DEFLATE.1.hdf
#    -rw-r--r-- 1 root root  56524 Jun 29 14:24 SDS.COMP_DEFLATE.2.hdf
#    -rw-r--r-- 1 root root  60069 Jun 29 14:24 SDS.COMP_DEFLATE.3.hdf
#    -rw-r--r-- 1 root root  59725 Jun 29 14:24 SDS.COMP_DEFLATE.4.hdf
#    -rw-r--r-- 1 root root  59884 Jun 29 14:24 SDS.COMP_DEFLATE.5.hdf
#    -rw-r--r-- 1 root root  58596 Jun 29 14:24 SDS.COMP_DEFLATE.6.hdf
#    -rw-r--r-- 1 root root  58450 Jun 29 14:24 SDS.COMP_DEFLATE.7.hdf
#    -rw-r--r-- 1 root root  58437 Jun 29 14:24 SDS.COMP_DEFLATE.8.hdf
#    -rw-r--r-- 1 root root  58446 Jun 29 14:24 SDS.COMP_DEFLATE.9.hdf
#    -rw-r--r-- 1 root root 102920 Jun 29 14:20 SDS.COMP_NONE.hdf
#    -rw-r--r-- 1 root root 103162 Jun 29 14:20 SDS.COMP_RLE.hdf
#    -rw-r--r-- 1 root root  60277 Jun 29 14:20 SDS.COMP_SKPHUFF.2.hdf
#    -rw-r--r-- 1 root root  52085 Jun 29 14:20 SDS.COMP_SKPHUFF.4.hdf
#    -rw-r--r-- 1 root root  52085 Jun 29 14:20 SDS.COMP_SKPHUFF.8.hdf
#    -rw-r--r-- 1 root root  71039 Jun 29 14:20 SDS.COMP_SZIP.EC.16.hdf
#    -rw-r--r-- 1 root root  79053 Jun 29 14:20 SDS.COMP_SZIP.EC.32.hdf
#    -rw-r--r-- 1 root root  66636 Jun 29 14:20 SDS.COMP_SZIP.EC.4.hdf
#    -rw-r--r-- 1 root root  66984 Jun 29 14:20 SDS.COMP_SZIP.EC.8.hdf
#    -rw-r--r-- 1 root root  39835 Jun 29 14:20 SDS.COMP_SZIP.NN.16.hdf
#    -rw-r--r-- 1 root root  44554 Jun 29 14:20 SDS.COMP_SZIP.NN.32.hdf
#    -rw-r--r-- 1 root root  38371 Jun 29 14:20 SDS.COMP_SZIP.NN.4.hdf
#    -rw-r--r-- 1 root root  38092 Jun 29 14:20 SDS.COMP_SZIP.NN.8.hdf
#
# For the chosen data set, the best results were attained using
# SZIP compression with NN compression scheme and 8 pixels per block.
# Mileage will vary with the data set used.

import sys
import os.path

from pyhdf.SD import *
import numpy

# Array shape and data type.
LENGTH      = 250
WIDTH       = 100
NUMPY_DATATYPE = numpy.int32
HDF_DATATYPE   = SDC.INT32

def doCompress(compType, value=0, v2=0):
    """Create and validate an HDF file using a compression scheme
    specified by the parameters"""

    # Build a significant file name
    if compType == SDC.COMP_NONE:
        fileName = "SDS.COMP_NONE"
    elif compType == SDC.COMP_RLE:
        fileName = "SDS.COMP_RLE"
    elif compType == SDC.COMP_SKPHUFF:
        fileName = "SDS.COMP_SKPHUFF.%d" % value
    elif compType == SDC.COMP_DEFLATE:
        fileName = "SDS.COMP_DEFLATE.%d" % value
    elif compType == SDC.COMP_SZIP:
        fileName = "SDS.COMP_SZIP"
        if value == SDC.COMP_SZIP_NN:
            fileName += ".NN"
        elif value == SDC.COMP_SZIP_EC:
            fileName += ".EC"
        else:
            print("illegal value")
            sys.exit(1)
        fileName += ".%s" % v2
    else:
        print("illegal compType")
        sys.exit(1)
    fileName += ".hdf"

    SDS_NAME    = "Data"

    fill_value  = 0

    #LENGTH      = 9
    #WIDTH       = 6
    #
    #data = numpy.array(  ((100,100,200,200,300,400),
    #                      (100,100,200,200,300,400),
    #                      (100,100,200,200,300,400),
    #                      (300,300,  0,400,300,400),
    #                      (300,300,  0,400,300,400),
    #                      (300,300,  0,400,300,400),
    #                      (0,  0,600,600,300,400),
    #                      (500,500,600,600,300,400),
    #                      (0,  0,600,600,300,400)), NUMPY_DATATYPE)

    # The above dataset is used in the original NCSA example.
    # It is too small to show a significant size reduction after
    # compression. The following is used for a more realistic example.
    data = numpy.zeros((LENGTH, WIDTH), NUMPY_DATATYPE)
    for i in range(LENGTH):
        for j in range(WIDTH):
            data[i,j] = (i+j)*(i-j)

    # Create HDF file, wiping it out it it already exists.
    sd_id = SD(fileName, SDC.WRITE | SDC.CREATE | SDC.TRUNC)

    # Create dataset.
    sds_id = sd_id.create(SDS_NAME, HDF_DATATYPE, (LENGTH, WIDTH))

    # Fill dataset will fill value.
    sds_id.setfillvalue(0)

    # Apply compression.
    try:
        sds_id.setcompress(compType,        # compression type
                           value, v2)         # args depend on compression type
    except HDF4Error as msg:
        print(("Error compressing the dataset with params: "
              "(%d,%d,%d) : %s" % (compType, value, v2, msg)))
        sds_id.endaccess()
        sd_id.end()
        os.remove(fileName)
        return

    # Load data in the dataset.
    sds_id[:] = data

    # Close dataset.
    sds_id.endaccess()

    # Close hdf file to flush compressed data.
    sd_id.end()

    # Verify compressed data.
    # ######################

    # Reopen file and select first dataset.
    sd_id = SD(fileName, SDC.READ)
    sds_id = sd_id.select(0)

    # Obtain compression info.
    compInfo = sds_id.getcompress()
    compType = compInfo[0]
    print("file : %s" % fileName)
    print("  size = %d" % os.path.getsize(fileName))
    if compType == SDC.COMP_NONE:
        print("  compType =  COMP_NONE")
    elif compType == SDC.COMP_RLE:
        print("  compType =  COMP_RLE")
    elif compType == SDC.COMP_SKPHUFF:
        print("  compType = COMP_SKPHUFF")
        print("  dataSize = %d" % compInfo[1])
    elif compType == SDC.COMP_DEFLATE:
        print("  compType = COMP_DEFLATE (GZIP)")
        print("  level = %d" % compInfo[1])
    elif compType == SDC.COMP_SZIP:
        print("  compType = COMP_SZIP")
        optionMask  = compInfo[1]
        if optionMask & SDC.COMP_SZIP_NN:
            print("  encoding scheme = NN")
        elif optionMask & SDC.COMP_SZIP_EC:
            print("  encoding scheme = EC")
        else:
            print("  unknown encoding scheme")
            sys.exit(1)
        pixelsPerBlock, pixelsPerScanline, bitsPerPixel, pixels  = compInfo[2:]
        print("  pixelsPerBlock = %d" % pixelsPerBlock)
        print("  pixelsPerScanline = %d" % pixelsPerScanline)
        print("  bitsPerPixel = %d" % bitsPerPixel)
        print("  pixels = %d" % pixels)
    else:
        print("  unknown compression type")
        sys.exit(1)

    # Read dataset contents.
    out_data = sds_id[:]

    # Compare with original data.
    num_errs = 0
    for i in range(LENGTH):
        for j in range(WIDTH):
            if data[i,j] != out_data[i,j]:
                print("bad value at %d,%d expected: %d got: %d" \
                      % (i,j,data[i,j],out_data[i,j]))
                num_errs += 1

    # Close dataset and hdf file.
    sds_id.endaccess()
    sd_id.end()

    if num_errs == 0:
        print("  file validated")
    else:
        print("  file invalid : %d errors" % num_errs)
    print("")

# Try different compression configurations in turn.

# All the following calls will fail with a "Cannot execute" exception if pyhdf
# was installed with the NOCOMPRESS macro set.

# No compression
print("no compression")
doCompress(SDC.COMP_NONE)

# RLE compression
print("run-length encoding")
doCompress(SDC.COMP_RLE)

# Skipping-Huffman compression.
print("Skipping-Huffman encoding")
for size in 2,4,8:
    doCompress(SDC.COMP_SKPHUFF, size)   # size in bytes of the data elements

# Gzip compression
print("GZIP compression")
for level in 1,2,3,4,5,6,7,8,9:
    doCompress(SDC.COMP_DEFLATE, level)   # compression level, from 1 to 9

# SZIP compression
# Those calls will fail with an "Encoder not available" exception if
# pyhdf was installed with the NOSZIP macro set.
print("SZIP compression")
for scheme in SDC.COMP_SZIP_NN, SDC.COMP_SZIP_EC:
    for ppb in 4,8,16,32:
        doCompress(SDC.COMP_SZIP, scheme, ppb)  # scheme, pixels per block
