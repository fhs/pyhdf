This example demonstrates creation of an HDF file from data in text files.  Specifically, the files temp.txt and depth.txt each store a table of scientific data (first line of text giving table's dimensions).  The HDF file table.hdf is created (being deleted first if it already existed), filled with the information in temp.txt in the SD (Scientific Dataset) format, and closed.  It is then reopened and the information in depth.txt is added (without overwriting temp.txt).

TODO: Include more code which accesses, in table.hdf, the information in tempt.txt and depth.txt.
