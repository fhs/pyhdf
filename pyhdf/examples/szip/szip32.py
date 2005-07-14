#!/usr/bin/env python

# Generate a compressed dataset using SZIP.
# Adapted from example "hdf.ncsa.uiuc.edu/doc_resource/SZIP/h4_examples/szip32.c".
# A bigger dataset is defined to better show the size reduction achieved by the SZIP
# compression. Pixels per block is set to 8, which seems to produce best results.
# Note that when applied to HDF4 SDS, the word "pixels" as used inside the SZIP
# documentation should really be understood as a "data element", eg a cell
# value inside a multidimensional array.
#
# The following table shows the size in bytes of the resulting HDF file
# for different combinations of SZIP encoding scheme and pixels per block,
# when applied to the dataset used inside this example.
#
#   scheme   pixels/block   HDF file size (bytes)
#   -------  ------------   ---------------------
#     none       n/a            102912
#     NN          2              42434
#     NN          8              38093
#     NN         16              39835
#     NN         32              44554
#     EC          2              71953
#     EC          8              66985
#     EC         16              71039
#     EC         32              79053
# 

from pyhdf.SD import *
import Numeric

# Set SZIP to True to compress data using SZIP. Set to False to bypass compression.
SZIP = True

FILE_NAME32 = "SDS_32_sziped.hdf"
SDS_NAME    = "SzipedData"

fill_value  = 0

#LENGTH      = 9
#WIDTH       = 6
#
#data = Numeric.array(((100,100,200,200,300,400),
#                      (100,100,200,200,300,400),
#                      (100,100,200,200,300,400),
#                      (300,300,  0,400,300,400),
#                      (300,300,  0,400,300,400),
#                      (300,300,  0,400,300,400),
#                      (0,  0,600,600,300,400),
#                      (500,500,600,600,300,400),
#                      (0,  0,600,600,300,400)), Numeric.Int32)

# The above dataset is too small to show a significant size reduction after
# compression. Try the following for a more realistic example.
LENGTH      = 250
WIDTH       = 100
data = Numeric.zeros((LENGTH, WIDTH), Numeric.Int32)
for i in range(LENGTH):
   for j in range(WIDTH):
        data[i,j] = (i+j)*(i-j)

# Create HDF file, wiping it out it it already exists.
sd_id = SD(FILE_NAME32, SDC.WRITE | SDC.CREATE | SDC.TRUNC)

# Create dataset.
sds_id = sd_id.create(SDS_NAME, SDC.INT32, (LENGTH, WIDTH))

# Fill dataset will fill value.
sds_id.setfillvalue(0)

# Apply SZIP.
if SZIP:
    sds_id.setcompress(SDC.COMP_SZIP,        # compression type
                       SDC.COMP_SZIP_NN,     # encoding scheme
		       8)                    # pixels per block

# Load data in the dataset.
sds_id[:] = data

# Close dataset.
sds_id.endaccess()

# Close hdf file to flush compressed data.
sd_id.end()

# Verify compressed data.
# ######################

# Reopen file and select first dataset.
sd_id = SD(FILE_NAME32, SDC.READ)
sds_id = sd_id.select(0)

# Obtain compression info.
if not SZIP:
   print "no compression"
else:
   compType, optionMask, pixelsPerBlock, pixelsPerScanline, bitsPerPixel, pixels  = \
             sds_id.getcompress()
   print "compression info :"
   print "  compType = %d" % compType
   print "  optionMask = %x" % optionMask,
   if optionMask & SDC.COMP_SZIP_NN:
      print "  NN compression mode"
   elif optionMask & SDC.COMP_SZIP_EC:
      print "  EC compression mode"
   else:
      print "  unknown compression mode"
   print "  pixelsPerBlock = %d" % pixelsPerBlock
   print "  pixelsPerScanline = %d" % pixelsPerScanline
   print "  bitsPerPixel = %d" % bitsPerPixel
   print "  pixels = %d" % pixels

# Read dataset contents.
out_data = sds_id[:]

# Compare with original data.
num_errs = 0
for i in range(LENGTH):
    for j in range(WIDTH):
        if data[i,j] != out_data[i,j]:
            print "bad value at %d,%d expected: %d got: %d" % (i,j,data[i,j],out_data[i,j])
            num_errs += 1

# Close dataset and hdf file.
sds_id.endaccess()
sd_id.end()

print "%d errors" % num_errs


