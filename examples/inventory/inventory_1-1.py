from pyhdf.HDF import *
from pyhdf.VS import *

# Open HDF file and initialize the VS interface
f = HDF('inventory.hdf',    # Open file 'inventory.hdf' in write mode
        HC.WRITE|HC.CREATE) # creating it if it does not exist
vs = f.vstart()           # init vdata interface

# Create vdata and define its structure
vd = vs.create(             # create a new vdata
               'INVENTORY', # name of the vdata
                          # fields of the vdata follow
               (('partid',HC.CHAR8, 5),       # 5 char string
                ('description',HC.CHAR8, 10), # 10 char string field
                ('qty',HC.INT16, 1),          # 1 16 bit int field
                ('wght',HC.FLOAT32, 1),       # 1 32 bit float
                ('price',HC.FLOAT32,1)        # 1 32 bit float
               ))         # 5 fields allocated in the vdata

# Set attributes on the vdata and its fields
vd.field('wght').unit = 'lb'
vd.field('price').unit = '$'
# In order to be able to update a string attribute, it must
# always be set to the same length. This sets 'status' to a 20
# char long, left-justified string, padded with spaces on the right.

vd.status = "%-20s" % 'phase 1 done'

# Store records
vd.write((                # write 3 records
          ('Q1234', 'bolt',12, 0.01, 0.05),   # record 1
          ('B5432', 'brush', 10, 0.4, 4.25),  # record 2
          ('S7613', 'scissor', 2, 0.2, 3.75)  # record 3
         ))
vd.detach()               # "close" the vdata

vs.end()                  # terminate the vdata interface
f.close()                 # close the HDF file
