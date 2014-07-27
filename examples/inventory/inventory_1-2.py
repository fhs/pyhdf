from pyhdf.HDF import *
from pyhdf.VS import *

f = HDF('inventory.hdf',         # Open file 'inventory.hdf'
        HC.WRITE|HC.CREATE)      # creating it if it does not exist
vs = f.vstart()                  # init vdata interface
vd = vs.attach('INVENTORY', 1)   # attach vdata 'INVENTORY' in write mode

# Update the `status' vdata attribute. The attribute length must not
# change. We call the attribute info() method, which returns a list where
# number of values (eg string length) is stored at index 2.
# We then assign a left justified string of exactly that length.
len = vd.attr('status').info()[2]
vd.status = '%-*s' % (len, 'phase 2 done')

vd[vd._nrecs:] =     (                     # append 2 records
          ('A4321', 'axe', 5, 1.5, 25),    # first record
          ('C3214', 'cup', 100, 0.1, 3.25) # second record
                    )
vd.detach()               # "close" the vdata

vs.end()                  # terminate the vdata interface
f.close()                 # close the HDF file
