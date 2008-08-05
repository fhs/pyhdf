This example demonstrates the use of the ODL (Object Description Language) parser module in pyhdf.  The sample file provided comes from the ASTER satellite instrument (see the aster example's README for more information).  It returns a dictionary-of-dictionaries, where the keys are either group names or object names.  The value of an object name is a dictionary containing its attributes.  The value of a group name is a dictionary containing its objects or subgroups.

Note that the parser in pyhdf is not perfect; while it supports all commonly-used aspects of the ODL language, more esoteric aspects (such as arbitrary bases) are not supported.  Also, a BEGIN_GROUP can be closed by an END_OBJECT, and vice versa.

TODO: update parser to support full specifications of ODL language.
TODO: example switching between text files of ODL and HDF files.
