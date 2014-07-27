from pyhdf.HDF import *
from pyhdf.VS import *

f = HDF('inventory.hdf',         # Open file 'inventory.hdf' in write mode
            HC.WRITE|HC.CREATE)  # creating it if it does not exist
vs = f.vstart()                  # init vdata interface
vd = vs.attach('INVENTORY', 1)   # attach vdata 'INVENTORY' in write mode

# Update the `status' vdata attribute. The attribute length must not
# change. We call the attribute info() method, which returns a list where
# number of values (eg string length) is stored at index 2.
# We then assign a left justified string of exactly that length.
len = vd.attr('status').info()[2]
vd.status = '%-*s' % (len, 'phase 3 done')

# Update record at index 1 (second record)
vd[1]  = ('Z4367', 'surprise', 10, 3.1, 44.5)
# Update record at index 4, and those after
vd[4:] = (
          ('QR231', 'toy', 12, 2.5, 45),
          ('R3389', 'robot', 3, 45, 2000),
          ('R3390', 'robot2', 8, 55, 2050)
         )
vd.detach()               # "close" the vdata
vs.end()                  # terminate the vdata interface
f.close()                 # close the HDF file
