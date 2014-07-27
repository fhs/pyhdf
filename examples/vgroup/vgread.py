from __future__ import print_function

from pyhdf.HDF import *
from pyhdf.V   import *
from pyhdf.VS  import *
from pyhdf.SD  import *

import sys

def describevg(refnum):

    # Describe the vgroup with the given refnum.

    # Open vgroup in read mode.
    vg = v.attach(refnum)
    print("----------------")
    print("name:", vg._name, "class:",vg._class, "tag,ref:",vg._tag, vg._refnum)

    # Show the number of members of each main object type.
    print("# members:  ", vg._nmembers,\
           "# datasets:", vg.nrefs(HC.DFTAG_NDG),\
           "# vdatas:  ", vg.nrefs(HC.DFTAG_VH),\
           "# vgroups: ", vg.nrefs(HC.DFTAG_VG))

    # Read the contents of the vgroup.
    members = vg.tagrefs()

    # Display info about each member.
    index = -1
    for tag, ref in members:
        index += 1
        print("member index", index)
        # Vdata tag
        if tag == HC.DFTAG_VH:
            vd = vs.attach(ref)
            nrecs, intmode, fields, size, name = vd.inquire()
            print("  vdata:",name, "tag,ref:",tag, ref)
            print("    fields:",fields)
            print("    nrecs:",nrecs)
            vd.detach()

        # SDS tag
        elif tag == HC.DFTAG_NDG:
            sds = sd.select(sd.reftoindex(ref))
            name, rank, dims, type, nattrs = sds.info()
            print("  dataset:",name, "tag,ref:", tag, ref)
            print("    dims:",dims)
            print("    type:",type)
            sds.endaccess()

        # VS tag
        elif tag == HC.DFTAG_VG:
            vg0 = v.attach(ref)
            print("  vgroup:", vg0._name, "tag,ref:", tag, ref)
            vg0.detach()

        # Unhandled tag
        else:
            print("unhandled tag,ref",tag,ref)

    # Close vgroup
    vg.detach()

# Open HDF file in readonly mode.
filename = sys.argv[1]
hdf = HDF(filename)

# Initialize the SD, V and VS interfaces on the file.
sd = SD(filename)
vs = hdf.vstart()
v  = hdf.vgstart()

# Scan all vgroups in the file.
ref = -1
while True:
    try:
        ref = v.getid(ref)
    except HDF4Error as msg:    # no more vgroup
        break
    describevg(ref)

# Terminate V, VS and SD interfaces.
v.end()
vs.end()
sd.end()

# Close HDF file.
hdf.close()
