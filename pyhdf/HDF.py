# $Id: HDF.py,v 1.1 2004-08-02 15:22:59 gosselin Exp $
# $Log: not supported by cvs2svn $

"""A module of the pyhdf package implementing the basic API of the
NCSA HDF4 library.
(see: hdf.ncsa.uiuc.edu)

Author: Andre Gosselin
        Maurice-Lamontagne Institute
        gosselina@dfo-mpo.gc.ca
        
Version: 0.6-1
Date:    December 3 2003

Introduction
------------
The role of the HDF module is to provide support to other modules of the
pyhdf package. It defines constants specifying file opening modes and
various data types, methods for accessing files, plus a few utility
functions to query library version and check if a file is an HDF one.

It should be noted that, among the modules of the pyhdf package, SD is
special in the sense that it is self-contained and does not need support
from the HDF module. For example, SD provides its own file opening and
closing methods, whereas VS uses methods of the HDF.HDF class for that.

Functions and classes summary
-----------------------------
The HDF module provides the following classes.

  HC
      The HC class holds constants defining opening modes and
      various data types.

  HDF
      The HDF class provides methods to open and close an HDF file,
      and return instances of the major HDF APIs (except SD).

      To instantiate an HDF class, call the HDF() constructor.

      methods:
        constructors:
          HDF()    open an HDF file, creating the file if necessary,
                   and return an HDF instance
          vstart() initialize the VS API over the HDF file and return a
                   VS instance (see the VS module documentation)
          

        closing file
          close()  close the HDF file

        inquiry
          getfileversion()  return info about the version of the  HDF file 
                   
The HDF module also offers the following functions.

  inquiry
    getlibversion()    return info about the version of the library
    ishdf()            determine whether a file is an HDF file
  
          
"""

import os, sys, types

import hdfext as _C

import VS

from error import HDF4Error, _checkErr

# List of names we want to be imported by an "from pyhdf import *"
# statement

__all__ = ['HDF', 'HDF4Error',
           'HC',
           'getlibversion', 'ishdf']



class HC:
    """The HC class holds contants defining opening modes and data types.

File opening modes (flags ORed together)

    CREATE   4     create file if it does not exist
    READ     1     read-only mode
    TRUNC  256     truncate if it exists
    WRITE    2     read-write mode

Data types

    CHAR     4    8-bit char
    CHAR8    4    8-bit char
    UCHAR    3    unsigned 8-bit integer (0 to 255)
    UCHAR8   3    unsigned 8-bit integer (0 to 255)
    INT8    20    signed 8-bit integer (-128 to 127)
    UINT8   21    unsigned 8-bit integer (0 to 255)
    INT16   23    signed 16-bit integer
    UINT16  23    unsigned 16-bit integer
    INT32   24    signed 32-bit integer
    UINT32  25    unsigned 32-bit integer
    FLOAT32  5    32-bit floating point
    FLOAT64  6    64-bit floating point



    """

    CREATE       = _C.DFACC_CREATE
    READ         = _C.DFACC_READ
    TRUNC        = 0x100          # specific to pyhdf
    WRITE        = _C.DFACC_WRITE

    CHAR         = _C.DFNT_CHAR8
    CHAR8        = _C.DFNT_CHAR8
    UCHAR        = _C.DFNT_UCHAR8
    UCHAR8       = _C.DFNT_UCHAR8
    INT8         = _C.DFNT_INT8
    UINT8        = _C.DFNT_UINT8
    INT16        = _C.DFNT_INT16
    UINT16       = _C.DFNT_UINT16
    INT32        = _C.DFNT_INT32
    UINT32       = _C.DFNT_UINT32
    FLOAT32      = _C.DFNT_FLOAT32
    FLOAT64      = _C.DFNT_FLOAT64

    FULL_INTERLACE = 0
    NO_INTERLACE   =1
    

# NOTE:
#  INT64 and UINT64 are not yet supported py pyhdf


def getlibversion():
    """Get the library version info.

    Args:
      no argument
    Returns:
      4-element tuple with the following components:
        -major version number (int)
        -minor version number (int)
        -complete library version number (int)
        -additional information (string)

    C library equivalent : Hgetlibversion
                                                   """

    status, major_v, minor_v, release, info = _C.Hgetlibversion()
    _checkErr('getlibversion', status, "cannot get lib version")
    return major_v, minor_v, release, info

def ishdf(filename):
    """Determine whether a file is an HDF file.

    Args:
      filename  name of the file to check
    Returns:
      1 if the file is an HDF file, 0 otherwise

    C library equivalent : Hishdf
                                            """

    return _C.Hishdf(filename)

class HDF:
    """The HDF class encapsulates the basic HDF functions.
    Its main use is to open and close an HDF file, and return
    instances of the major HDF APIs (except for SD).
    To instantiate an HDF class, call the HDF() constructor. """

    def __init__(self, path, mode=HC.READ, nblocks=0):
        """HDF constructor: open an HDF file, creating the file if
        necessary.
 
        Args:
          path    name of the HDF file to open
          mode    file opening mode; this mode is a set of binary flags
	          which can be ored together
		      
		      HC.CREATE   combined with HC.WRITE to create file 
                                  if it does not exist
                      HC.READ     open file in read-only access (default)
                      HC.TRUNC    if combined with HC.WRITE, overwrite
                                  file if it already exists
                      HC.WRITE    open file in read-write mode; if file
                                  exists it is updated, unless HC.TRUNC is
                                  set, in which case it is erased and
                                  recreated; if file does not exist, an
                                  error is raised unless HC.CREATE is set,
                                  in which case the file is created

                   Note an important difference in the way CREATE is
                   handled by the HDF C library and the pyhdf package.
                   In the C library, CREATE indicates that a new file should
                   always be created, overwriting an existing one if
                   any. For pyhdf, CREATE indicates a new file should be
                   created only if it does not exist, and the overwriting
                   of an already existing file must be explicitly asked
                   for by setting the TRUNC flag.

                   Those differences were introduced so as to harmonize
                   the way files are opened in the pycdf and pyhdf
                   packages. Also, this solves a limitation in the
                   hdf (and netCDF) library, where there is no easy way
                   to implement the frequent requirement that an existent
                   file be opened in read-write mode, or created
                   if it does not exist.

          nblocks  number of data descriptor blocks in a block wit which
                   to create the file; the parameter is ignored if the file
                   is not created; 0 asks to use the default
	
        Returns:
          an HDF instance
 
        C library equivalent : Hopen
	                                             """
	# Private attributes:
	#  _id:       file id (NOTE: not compatile with the SD file id)
                                                   
        # See if file exists.
        exists = os.path.exists(path)

        if HC.WRITE & mode:
            if exists:
                if HC.TRUNC & mode:
                    try:
                        os.remove(path)
                    except Exception, msg:
                        raise HDF4Error, msg
                    mode = HC.CREATE
                else:
                    mode = HC.WRITE
            else:
                if HC.CREATE & mode:
                    mode = HC.CREATE
                else:
                    raise HDF4Error, "HDF: no such file"
        else:
            if exists:
                if mode & HC.READ:
                    mode = HC.READ     # clean mode
                else:
                    raise HDF4Error, "HDF: invalid mode"
            else:
                raise HDF4Error, "HDF: no such file"
                
        id = _C.Hopen(path, mode, nblocks)
        _checkErr('HDF', id, "cannot open %s" % path)
        self._id = id
        

    def __del__(self):
        """Delete the instance, first calling the end() method 
        if not already done.          """

        try:
            if self._id:
                self.close()
        except:
            pass

    def close(self):
        """Close the HDF file.

        Args:
          no argument
        Returns:
          None

        C library equivalent : Hclose
                                                """

        _checkErr('close', _C.Hclose(self._id), "cannot close file")
        self._id = None

    def getfileversion(self):
        """Get file version info.
        
        Args:
          no argument
        Returns:
          4-element tuple with the following components:
            -major version number (int)
            -minor version number (int)
            -complete library version number (int)
            -additional information (string)
            
        C library equivalent : Hgetlibversion
                                                   """

        status, major_v, minor_v, release, info = _C.Hgetfileversion(self._id)
        _checkErr('getfileversion', status, "cannot get file version")
        return major_v, minor_v, release, info

    def vstart(self):
        """Initialize the VS API over the file and return a VS instance.

        Args:
          no argument
        Returns:
          VS instance

        C library equivalent : Vstart (in fact: Vinitialize)
                                                              """
        return VS.VS(self)



###########################
# Support functions
###########################


def _array_to_ret(buf, nValues):

    # Convert array 'buf' to a scalar or a list.

    if nValues == 1:
        ret = buf[0]
    else:
        ret = []
        for i in xrange(nValues):
            ret.append(buf[i])
    return ret

def _array_to_str(buf, nValues):

    # Convert array of bytes 'buf' to a string.

    # Return empty string if there is no value.
    if nValues == 0:
        return ""
    # When there is just one value, _array_to_ret returns a scalar
    # over which we cannot iterate.
    if nValues == 1:
        chrs = [chr(buf[0])]
    else:
        chrs = [chr(b) for b in _array_to_ret(buf, nValues)]
    # Strip NULL at end
    if chrs[-1] == '\0':
        del chrs[-1]
    return ''.join(chrs)


