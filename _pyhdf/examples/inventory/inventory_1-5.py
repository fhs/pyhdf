from __future__ import print_function

from pyhdf.HDF import *
from pyhdf.VS import *

f = HDF('inventory.hdf')         # open 'inventory.hdf' in read mode
vs = f.vstart()                  # init vdata interface
vd = vs.attach('INVENTORY')      # attach vdata 'INVENTORY' in read mode

# Display some vdata attributes
print("status:", vd.status)
print("vdata: ", vd._name)        # predefined attribute: vdata name
print("nrecs: ", vd._nrecs)       # predefined attribute:  num records

# Display value of attribute 'unit' for all fields on which
# this attribute is set
print("units: ", end=' ')
for fieldName in vd._fields:     # loop over all field names
    try:
        # instantiate field and obtain value of attribute 'unit'
        v = vd.field(fieldName).unit
        print("%s: %s" % (fieldName, v), end=' ')
    except:                      # no 'unit' attribute: ignore
        pass
print("")
print("")

# Display table header.
header = "%-7s %-12s %3s %4s %8s" % tuple(vd._fields)
print("-" * len(header))
print(header)
print("-" * len(header))

# Read all records at once, and loop over the sequence.
for rec in vd[:]:
    print("%-7s %-12s %3d %4.1f %8.2f" % tuple(rec))

vd.detach()               # "close" the vdata
vs.end()                  # terminate the vdata interface
f.close()                 # close the HDF file
