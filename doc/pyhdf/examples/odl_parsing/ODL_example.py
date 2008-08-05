"""
ODL Parsing Example (using an ASTER HDF file)

This module demonstrates the use of the ODL parser to extract
information from the hdf dataset.  The parser returns a
dictionary of dictionaries, where subdictionaries correspond
to objects (the dictionary values being their attributes) or
groups thereof (values then being additional dictionaries)
"""

# This is a demonstration of the use of the pyhdf module to
# analyze data from the aster satellite.  Use is made of the
# function parse_odl, which parses the ODL dialect used in the
# datasets.

# import necessary modules
from pyhdf.SD import *
from pyhdf.odl_parser import parse_odl

# load an example dataset
# (the real file can be obtained from the maintainer)
Dataset1 = SD('AST5_file.hdf')

# At this point, Dataset1 is an instance of the SD class
print "Dataset1's type: ", type(Dataset1)
#output: <class 'SD.SD'>

# Dataset1.attributes() is a dictionary
print "Type of Dataset1's attributes: ", type( Dataset1.attributes() )
# output: <type 'dict'>

# So is Dataset1.datasets()
print "Type of Dataset1's datasets: ", type( Dataset1.datasets() )
# output: <type 'dcit'>
print "Dataset1.attributes' keys: ", Dataset1.attributes().keys()
#output: ['HDFEOSVersion', 'act_specific', 'StructMetadata.0',...

# The value of productmetadata.0 is a dictionary
print "productmetadata.0 is a key for Dataset1."
print "The type of its value is: ", \
      type(Dataset1.attributes()['productmetadata.0'])
# output: <type 'str'>


# It is, in fact, a dictionary of ODL (Object Description Language) code
# that we can parse into a dictionary using the function parse_odl

# load the parse_odl function
Dict = parse_odl(Dataset1.attributes()['productmetadata.0'])
print "Type of the dictionary made from the ODL data: ", type( Dict )
# output: <type 'dict'>


# Relevant data can now be conveniently accessed with this structure
print "A value of one of Dict's subdictionaries: ", \
      Dict['ASTERGDSGENERICMETADATA']['GROUPTYPE']
# output: 'MASTERGROUP'
