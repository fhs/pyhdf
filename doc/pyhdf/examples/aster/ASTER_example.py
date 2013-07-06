"""
ASTER example 2

This module demonstrates the uses of the aster python module
to process data from the Aster (Advanced Spaceborne Thermal
Emission and Reflection Radiometer).
"""

# make functions available
#from aster.api import *
#from api import *
from aster_module import *
from pyhdf.odl_parser import parse_odl
#from pyhdf import odl_parser

#print "ODL parsing: ", parse_odl
#print "the parser mod: ", odl_parser

# choosing the file
# Copies of example files can be obtaned from the maintainer.
Emissivity_filename = "AST5_file.hdf"

# getting Surface Emissivity ASTER 05 Level 2 data
Emissivity_object = AST05(Emissivity_filename)

# The Emissivity_object now has the method
# lookup(latitude, longitude) to find data
# from a given point on the globe.
#
# Data is of the form

emis_10_15 = Emissivity_object.lookup(10, 15)
print "Emissivity data: ", emis_10_15

# choosing the file
Temperature_filename = "AST8_file.hdf"

# getting Kinetic Temperature ASTER 08 Level 2 data
Temperature_object = AST08(Temperature_filename)

# The Temperature_object now has the method
# lookup(latitude, longitude) to find data
# from a given point on the globe.

temp_12_50 = Temperature_object.lookup(12, 50)
print "Temperature data: ", temp_12_50
