********
*Processing ASTER HDF files
********

This example presents a case-in-point of the need for pyhdf even when HDF4 format has been superceded by HDF5.  
ASTER (Advanced Spaceborne Thermal Emission and Reflection Radiometer) is an imaging instrument flying on the 
satellite Terra, which was launched in December 1999 as part of NASA's Earth Observing System (EOS).
ASTER has gathered invaluable data about the Earth's surface, including temperature, elevation and reflectance.  
However, as it was launched before the rise of HDF5, all of its data files are stored in HDF4.

This example uses pyhdf to process the data files, and several domain-specific functions to make the ASTER data 
easily accessible.  Parts of the Aster files are stored in ODL (Object Description Language), which is processed
in the directory examples/ODL_parsing.

The example itself is ASTER_example.py; the other .py files are helper files containing domain-specific functions.

Note that this example depends on PyProj.
