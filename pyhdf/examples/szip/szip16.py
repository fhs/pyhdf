#!/usr/bin/env python

from pyhdf.SD import *
import Numeric

SZIP = True

FILE_NAME16 = "SDS_16_sziped.hdf"
SDS_NAME    = "SzipedData"

LENGTH      = 150
WIDTH       = 100
fill_value  = 0

#data = Numeric.array(((100,100,200,200,300,400),
#                      (100,100,200,200,300,400),
#                      (100,100,200,200,300,400),
#                      (300,300,  0,400,300,400),
#                      (300,300,  0,400,300,400),
#                      (300,300,  0,400,300,400),
#                      (0,  0,600,600,300,400),
#                      (500,500,600,600,300,400),
#                      (0,  0,600,600,300,400)), Numeric.Int16)

data = Numeric.zeros((LENGTH, WIDTH), Numeric.Int16)
for i in range(LENGTH):
    for j in range(WIDTH):
        data[i,j] = i+j


# Create HDF file.
sd_id = SD(FILE_NAME16, SDC.WRITE | SDC.CREATE | SDC.TRUNC)

# Create dataset.
sds_id = sd_id.create(SDS_NAME, SDC.INT16, (LENGTH, WIDTH))

# Fill dataset will fill value.
sds_id.setfillvalue(0)

# Apply SZIP.
if SZIP:
    sds_id.setcompress(SDC.COMP_SZIP,
                       32,                    # pixels_per_block
                       SDC.COMP_SZIP_NN)

sds_id[:] = data

# Close dataset
sds_id.endaccess()

# Close hdf file to flush compressed data.
sd_id.end()

# Verify compressed data.

# Reopen file and select first dataset.
sd_id = SD(FILE_NAME16, SDC.READ)
sds_id = sd_id.select(0)

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


