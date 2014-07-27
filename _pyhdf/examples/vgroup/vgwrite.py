from pyhdf.HDF import *
from pyhdf.V   import *
from pyhdf.VS  import *
from pyhdf.SD  import *

def vdatacreate(vs, name):

    # Create vdata and define its structure
    vd = vs.create(name,
                   (('partid',HC.CHAR8, 5),       # 5 char string
                    ('description',HC.CHAR8, 10), # 10 char string field
                    ('qty',HC.INT16, 1),          # 1 16 bit int field
                    ('wght',HC.FLOAT32, 1),       # 1 32 bit float
                    ('price',HC.FLOAT32,1)        # 1 32 bit float
                   ))

    # Store records
    vd.write((('Q1234', 'bolt',12, 0.01, 0.05),   # record 1
              ('B5432', 'brush', 10, 0.4, 4.25),  # record 2
              ('S7613', 'scissor', 2, 0.2, 3.75)  # record 3
             ))
    # "close" vdata
    vd.detach()

def sdscreate(sd, name):

    # Create a simple 3x3 float array.
    sds = sd.create(name, SDC.FLOAT32, (3,3))
    # Initialize array
    sds[:] = ((0,1,2),(3,4,5),(6,7,8))
    # "close" dataset.
    sds.endaccess()

# Create HDF file
filename = 'inventory.hdf'
hdf = HDF(filename, HC.WRITE|HC.CREATE)

# Initialize the SD, V and VS interfaces on the file.
sd = SD(filename, SDC.WRITE)  # SD interface
vs = hdf.vstart()             # vdata interface
v  = hdf.vgstart()            # vgroup interface

# Create vdata named 'INVENTORY'.
vdatacreate(vs, 'INVENTORY')
# Create dataset named "ARR_3x3"
sdscreate(sd, 'ARR_3x3')

# Attach the vdata and the dataset.
vd = vs.attach('INVENTORY')
sds = sd.select('ARR_3x3')

# Create vgroup named 'TOTAL'.
vg = v.create('TOTAL')

# Add vdata to the vgroup
vg.insert(vd)
# We could also have written this:
# vgroup.add(vd._tag, vd._refnum)
# or this:
# vgroup.add(HC.DFTAG_VH, vd._refnum)

# Add dataset to the vgroup
vg.add(HC.DFTAG_NDG, sds.ref())

# Close vgroup, vdata and dataset.
vg.detach()       # vgroup
vd.detach()       # vdata
sds.endaccess()   # dataset

# Terminate V, VS and SD interfaces.
v.end()           # V interface
vs.end()          # VS interface
sd.end()          # SD interface

# Close HDF file.
hdf.close()
