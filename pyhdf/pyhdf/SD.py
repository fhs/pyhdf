# $Id: SD.py,v 1.1 2004-08-02 14:53:31 gosselin Exp $
# $Log: not supported by cvs2svn $
"""A python package to access HDF (v4) files.
(see: hdf.ncsa.uiuc.edu)

Author: Andre Gosselin
        Maurice-Lamontagne Institute
        gosselina@dfo-mpo.gc.ca
        
Version: 0.5-1
Date:    August 1 2003

Table of contents
  Introduction
  The SD API
  Package components
  Prerequisites
  Documentation
  Summary of differences between the pyhdf and C API
  Error handling
  High level attribute access
  High level variable access
  Reading/setting multivalued HDF attributes and variables
  netCDF files
  Classes summary
  Examples
  

Introduction
------------
The pyhdf package lets one manage HDF files from within a python program.
netCDF files can also be read and modified using the package.

Two versions of HDF currently exist, version 4 and version 5.
pyhdf only implements HDF version 4.

Many different APIs are found inside the HDF4 specification. Currently,
pyhdf implements just one of those: the SD API. Other APIs should be added
in the future (VS, V, GR, AN, etc).
  
The SD API
----------
pyhdf wraps the SD API using 4 different types of python objects:
  SD     HDF SD interface (almost synonimous with the HDF file)
  SDS    scientific dataset
  SDim   dataset dimension
  SDattr attribute (either at the file, dataset or dimension level)
  
To access the SD API a python program can say one of:

  >>> import phdf            # must prefix names with "pyhdf.SD."
  >>> from pyhdf import SD   # must prefix names with "SD."
  >>> from pyhdf.SD import * # names need no prefix

This document assumes the last import style is used.
  
pyhdf key features are as follows.
   
  -Almost every routine of the original SD API has been implemented inside
   pyhdf. Only a few have been ignored, most of them being of a rare use:
    - SDsetnbitdataset()
    - All chunking/tiling routines : SDgetchunkinfo(), SDreadchunk(),
      SDsetchunk(), SDsetchunkcache(), SDwritechunk()
    - SDsetblocksize()
    - SDisdimval_bwcomp(), SDsetdimval_comp()

  -It is quite straightforward to go from C to python and vice-versa, and
   to learn pyhdf usage by refering to the C API documentation.

  -A few high-level python methods have been developped to ease
   programmers task. Of greatest interest are those allowing HDF
   access through familiar python idioms:   
     -HDF attributes can be read/written like ordinary python class
      attributes
     -HDF datasets can be read/written like ordinary python lists using
      multidimensional indices and so-called "extended slice syntax", with
      strides allowed

      See "High level attribute access" and "High level variable access"
      sections for details.

     -pyhdf offers methods to retrieve a dictionnary of the attributes,
      dimensions and variables defined on a dataset, and of the attributes
      set on a variable and a dimension. Querying a dataset is thus geatly
      simplified.

  -HDF datasets are read/written through "Numeric", a sophisticated
   python package for efficiently handling multi-dimensional arrays of
   numbers. Numeric can nicely extend the HDF functionnality, eg.
   adding/subtracting arrays with the '+/-' operators.

 
Package components
------------------
pyhdf is a proper Python package, eg a collection of modules stored under
a directory named similarly to the package and holding an __init__.py 
file. For each HDF API there exists a corresponding set of modules.
The pyhdf package is currently composed of 3 modules defining the SD API.

  _sdext    C extension module responsible for wrapping the HDF
            SD API
  sdext     python module implementing some utility functions
            complementing the C extension module
  SD        python module which wraps the C extension module inside
            an OOP framework

_sdext and sdext were generated with the SWIG preprocessor.
SWIG is however *not* needed to run the package. Those two modules
are meant to do their work in the background, and should never be called
directly. Only 'pyhdf.SD' should be imported by the user program.

Prerequisites
-------------
The following software must be installed in order for pyhdf to
work.
  
  HDF (v4) library
    pyhdf does *not* include the HDF4 library, which must
    be installed separately. HDF is available at
    "http://hdf.ncsa.uiuc.edu/obtain.html".

  Numeric python package
    HDF variables are read/written using the array data type provided
    by the python Numeric package. It is available at
    "numpy.sourceforge.net".

Documentation
-------------
pyhdf has been written so as to stick as closely as possible to 
the naming conventions and calling sequences documented inside the
"HDF User s Guide" manual. Even if pyhdf gives an OOP twist
to the C API, the manual can be easily used as a documentary source
for pyhdf, once the class to which a function belongs has been
identified, and of course once requirements imposed by the Python
langage have been taken into account. Consequently, this documentation
will not attempt to provide an exhaustive coverage of the HDF
library. For this, the user is referred to the above mentioned manual.
  
This document (in both its text and html versions) has been completely
produced using "pydoc", the Python documentation generator (which
made its debut in the 2.1 release). pydoc can also be used
as an on-line help tool. For example, to know everything about
the SD.SDS class, say:
  
  >>> from pydoc import help
  >>> from pyhdf.SD import *
  >>> help(SDS)

To be more specific and get help only for the get() method of the
SDS class:

  >>> help(SDS.get)   # or...
  >>> help(vinst.get) # if vinst is an SDS instance
  
Summary of differences between the pyhdf and C SD API
-----------------------------------------------------
Most of the differences between the pyhdf and C SD API can
be summarized as follows.

  Return values
  
   -In the C API, every function returns an integer status code, and values
    computed by the function are returned through one or more pointers
    passed as arguments.
   -In pyhdf, error statuses are returned through the Python exception
    mechanism, and values are returned as the method result. When the
    C API specifies that multiple values are returned, pyhdf returns a 
    tuple of values, which are ordered similarly as the pointers in the
    C function argument list.
   
Error handling
--------------
All errors that the SD API reports with a SUCCESS/FAIL error code
are reported by pyhdf using the Python exception mechanism.
When the C library reports a FAIL status, pyhdf raises an HDF4Error
exception (a subclass of Exception) with a descriptive message. 
Unfortunately, the C library is rarely informative about the cause of 
the error. pyhdf does its best to try to document the error, but most 
of the time cannot do more than saying "execution error".
 
High level attribute access
---------------------------
HDF allows setting attributes either at the dataset, the variable
or the dimension level. With pyhdf, this can can be achieved in two ways.

  -By calling the get()/set() method of an attribute instance. In the
   following example, HDF file 'example.hdf' is created, and string
   attribute 'title' is attached to the file and given value
   'example'.
     >>> from pyhdf.SD import *
     >>> d = SD('example.hdf',SDC.WRITE|SDC.CREATE)  # create file
     >>> att = d.attr('title')            # create attribute instance
     >>> att.set(SDC.CHAR, 'example')     # set attribute type and value
     >>> att.get()                        # get attribute value
     'example'
     >>>

  -By handling the attribute like an ordinary Python class attribute.
   The above example can then be rewritten as follows:
     >>> from pyhdf.SD import *
     >>> d = SD('example.hdf',SDC.WRITE|SDC.CREATE)  # create dataset
     >>> d.title = 'example'              # set attribute type and value
     >>> d.title                          # get attribute value
     'example'
     >>>

  This applies as well to multi-valued attributes.
    >>> att = d.attr('values')               # With an attribute instance
    >>> att.set(SDC.INT32, (1,2,3,4,5))           
    >>> att.get()
    [1, 2, 3, 4, 5]

    >>> d.values = (1,2,3,4,5)               # As a Python class attribute
    >>> d.values
    [1, 2, 3, 4, 5]

When the attribute is known by its name through a string, standard
functions 'setattr()' and 'getattr()' can be used to replace the dot
notation. Above example becomes:
    >>> setattr(d, 'values', (1,2,3,4,5))
    >>> getattr(d, 'values')
    [1, 2, 3, 4, 5]

Handling a HDF attribute like a Python class attribute is admittedly
more natural, and also simpler. Some control is however lost in doing so.
  -Attribute type cannot be specified. pyhdf automatically selects one of
   three types according to the value(s) assigned to the attribute:
   SDC.CHAR if value is a string, SDC.INT32 if all values are integral,
   SDC.DOUBLE if one value is a float. 
  -Consequently, byte values cannot be assigned.
  -Attribute properties (length, type, index number) can only be queried
   through methods of an attribute instance.

High level variable access
--------------------------
With pyhdf, datasets can be read/written in two ways.

The first way is through the get()/set() methods of a dataset instance.
Those methods accept parameters to specify the starting indices, the count
of values to read/write, and the strides along each dimension. For example,
if 'v' is a 4x4 array:
    >>> v.get()                         # complete array
    >>> v.get(start=(0,0),count=(1,4))  # first row
    >>> v.get(start=(0,1),count=(2,2),  # second and third columns of
    ...       stride=(2,1))             # first and third row

The second way is by indexing and slicing the variable like a Python
sequence. pyhdf here follows most of the rules used to index and slice
Numeric arrays. Thus an HDF dataset can be seen almost as a Numeric,
array, except that data is read from/written to a file instead of memory.

Extended indexing let you access variable elements with the familiar
[i,j,...] notation, with one index per dimension. For example, if 'm' is a
3x3x3 HDF dataset, one could write:
    >>> m[0,3,5] = m[0,5,3]
    
When indexing is used to select a dimension in a 'get' operation, this
dimension is removed from the output array, thus reducing its rank by 1. A
rank 0 array is converted to a scalar. Thus, for a 3x3x3 'm' dataset
(rank 3) of integer type :
    >>> a = m[0]         # a is a 3x3 array (rank 2)
    >>> a = m[0,0]       # a is a 3 element array (rank 1)
    >>> a = m[0,0,0]     # a is an integer (rank 0 array becomes a scalar)

Had this rule not be followed, m[0,0,0] would have resulted in a single
element array, which could complicate computations.

Extended slice syntax allows slicing HDF datasets along each of its
dimensions, with the specification of optional strides to step through
dimensions at regular intervals. For each dimension, the slice syntax
is: "i:j[:stride]", the stride being optional. As with ordinary slices,
the starting and ending values of a slice can be omitted to refer to the
first and last element, respectively, and the end value can be negative to
indicate that the index is measured relative to the tail instead of the
beginning. Omitted dimensions are assumed to be sliced from beginning to
end. Thus:
    >>> m[0]             # treated as 'm[0,:,:]'.

Example above with get()/set() methods can thus be rewritten as follows:
    >>> v[:]             # complete array
    >>> v[:1]            # first row
    >>> v[::2,1:3]       # second and third columns of first and third row

Indexes and slices can be freely mixed, eg:
    >>> m[:2,3,1:3:2]
     
Note that, countrary to indexing, a slice never reduces the rank of the
output array, even if its length is 1. For example, given a 3x3x3 'm'
dataset:
    >>> a = m[0]         # indexing: a is a 3x3 array (rank 2)
    >>> a = m[0:1]       # slicing: a is a 1x3x3 array (rank 3)

As can easily be seen, extended slice syntax is much more elegant and
compact, and offers a few possibilities not easy to achieve with the
get()/sett() methods. Negative indices offer a nice example:
    >>> v[-2:]                         # last two rows
    >>> v[-3:-1]                       # second and third row
    >>> v[:,-1]                        # last column

Reading/setting multivalued HDF attributes and variables
--------------------------------------------------------
Multivalued HDF attributes are set using a python sequence (tuple or
list). Reading such an attribute returns a python list. The easiest way to
read/set am HDF attribute is by handling it like a Python class attribute
(see "High level attribute access"). For example:
    >>> d=SD('test.hdf',SDC.WRITE|SDC.CREATE)  # create file
    >>> d.integers = (1,2,3,4)         # define multivalued integer attr
    >>> d.integers                     # get the attribute value
    [1, 2, 3, 4]

The easiest way to set multivalued HDF datasets is to assign to an
indexed subset of the dataset, using "[:]" to assign to the whole dataset
(see "High level variable access"). The assigned value can be a python
sequence, which can be multi-leveled when assigning to a multdimensional
dataset. For example:
    >>> d=SD('test.hdf',SDC.WRITE|SDC.CREATE) # create file
    >>> v1=d.create('v1',SDC.INT32,3)         # 3-elem vector
    >>> v1[:]=[1,2,3]                         # assign 3-elem python list
    >>> v2=d.create('d2',SDC.INT32,(3,3))     # create 3x3 variable
           # The list assigned to v2 is composed
           # of 3 lists, each representing a row of v2.
    >>> v2[:]=[[1,2,3],[11,12,13],[21,22,23]]

The assigned value can also be a Numeric array. Rewriting example above:
    >>> v1=array([1,2,3])
    >>> v2=array([[1,2,3],[11,12,13],[21,22,23])

Note how we use indexing expressions 'v1[:]' and 'v2[:]' when assigning
using python sequences, and just the variable names when assigning Numeric
arrays.

Reading an HDF variable always returns a Numeric array, except if
indexing is used and produces a rank-0 array, in which case a scalar is
returned.

netCDF files
------------
Files written in the popular Unidata netCDF format can be read and updated
using the HDF SD API. Unfortunately, pyhdf cannot create netCDF formatted
files from scratch. The python 'pycdf' package can be used for that.

When accessing netCDF files through pyhdf, one should be aware of the
following differences between the netCDF and the HDF SD libraries.

  -Differences in terminology can be confusing. What netCDF calls a
   'dataset' is called a 'file' or 'SD interface' in HDF. What HDF calls
   a dataset is called a 'variable' in netCDF parlance.
  -In the netCDF API, dimensions are defined at the global (netCDF dataset)
   level. Thus, two netCDF variables defined over dimensions X and Y
   have the same rank and shape.
  -In the HDF SD API, dimensions are defined at the HDF dataset level.
   Dimensions can be named, but this is only a commodity. Dimension X for
   variable A can be totally different from dimension X of variable B.
  -A consequence of the global dimension definition feature in netCDF is
   that, when two netCDF variables are based on the unlimited dimension,
   they automatically grow in sync. If variables A and B use the unlimited
   dimension, adding "records" to A along its unlimited dimension
   implicitly adds records in B (which are left in an undefined state and
   filled with the fill_value when the file is refreshed).
  -In HDF, unlimited dimensions behave independently. If HDF datasets A and
   B are based on an unlimited dimension, adding records to A does not
   affect the number of records in B.


Classes summary
---------------
pyhdf defines the following classes.


  SD     The SD class implements the HDF SD interface as applied to a given
         file. This class encapsulates the "SD interface" identifier
         (referred to as "sd_id" in the C API documentation), and all
         the SD API top-level functions.

         To create an SD instance, call the SD() constructor.

         methods:
           constructors:
             SD()          open an existing HDF file or create a new one,
                           returning an SD instance
             attr()        create an SDAttr (attribute) instance to access
                           an existing file attribute or create a new one
             create()      create a new dataset, returning an SDS instance
             select()      locate an existing dataset given its name or
                           index number, returning an SDS instance

           file closing
             end()         end access to the SD interface and close the
                           HDF file

           inquiry
             attributes()  return a dictionnary describing every global
                           attribute attached to the HDF file
             datasets()    return a dictionnary describing every dataset
                           stored inside the file
             info()        get the number of datasets stored in the file
                           and the number of attributes attached to it
             nametoindex() get a dataset index number given the dataset
                           name
             reftoindex()  get a dataset index number given the dataset
                           reference number

           misc
             setfillmode() set the fill mode for all the datasets in
                           the file
             

  SDAttr The SDAttr class defines an attribute, either at the file (SD),
         dataset (SDS) or dimension (SDim) level. The class encapsulates
         the object to which the attribute is attached, and the attribute
         name.

         To create an SDAttr instance, obtain an instance for an SD (file),
         SDS (dataset) or dimension (SDim) object, and call its attr()
         method.

         methods:
           read/write value
             get()         get the attribute value
             set()         set the attribute value

                           An attribute can also be read/written like
                           a python class attribute, using the familiar
                           dot notation. See "High level attribute access".
           
           inquiry
             index()       get the attribute index number
             info()        get the attribute name, type and number of
                           values


  SDC    The SDC class holds contants defining file opening modes and
         data types. Constants are named after their C API counterparts.

           file opening modes:
             SDC.CREATE
             SDC.READ
             SDC.TRUNC      # specific to pyhdf
             SDC.WRITE

           data types:
             SDC.CHAR
             SDC.CHAR8
             SDC.UCHAR8
             SDC.INT8
             SDC.UINT8
             SDC.INT16
             SDC.UINT16
             SDC.INT32
             SDC.FLOAT32
             SDC.FLOAT64

           dataset fill mode:
             SDC.FILL
             SDC.NOFILL

           dimension:
             SDC.UNLIMITED

           data compression:
             COMP_NONE
             COMP_RLE
             COMP_NBIT
             COMP_SKPHUFF
             COMP_DEFLATE

  SDS    The SDS class implements an HDF scientific dataset (SDS) object.

         To create an SDS instance, call the create() or select() methods
         of an SD instance.

         methods:
           constructors
             attr()        create an SDAttr (attribute) instance to access
                           an existing dataset attribute or create a
                           new one
             dim()         return an SDim (dimension) instance for a given
                           dataset dimension, given the dimension index
                           number

           dataset closing
             endaccess()   terminate access to the dataset
           
           inquiry
             attributes()  return a dictionnary describing every 
                           attribute defined on the dataset
             checkempty()  determine whether the dataset is empty
             dimensions()  return a dictionnary describing all the
                           dataset dimensions
             info()        get the dataset name, rank, dimension lengths,
                           data type and number of attributes
             iscoordvar()  determine whether the dataset is a coordinate
                           variable (holds a dimension scale)
             isrecord()    determine whether the dataset is appendable
                           (the dataset dimension 0 is unlimited)
             ref()         get the dataset reference number
                           

           reading/writing data values
             get()         read data from the dataset
             set()         write data to the dataset

                           A dataset can also be read/written using the
                           familiar index and slice notation used to
                           access python sequences. See "High level
                           variable access".

           reading/writing  standard attributes
             getcal()       get the dataset calibration coefficients:
                              scale_factor, scale_factor_err, add_offset,
                              add_offset_err, calibrated_nt
             getdatastrs()  get the dataset standard string attributes:
                              long_name, units, format, coordsys
             getfillvalue() get the dataset fill value:
                              _FillValue
             getrange()     get the dataset min and max values:
                              valid_range
             setcal()       set the dataset calibration coefficients
             setdatastrs()  set the dataset standard string attributes
             setfillvalue() set the dataset fill value
             setrange()     set the dataset min and max values

           compression
             getcompress()  get the dataset compression type
             setcompress()  set the dataset compression type
             
           misc
             setexternalfile()  store the dataset in an external file

  SDim   The SDdim class implements a dimension object.

         To create an SDim instance, call the dim() method of an SDS
         (dataset) instance.

         Methods:
           constructors
             attr()         create an SDAttr (attribute) instance to access
                            an existing dimension attribute or create a
                            new one
           inquiry
             attributes()   return a dictionnary describing every 
                            attribute defined on the dimension
             info()         get the dimension name, length, scale data type
                            and number of attributes
             length()       return the current dimension length

           reading/writing dimension data
             getscale()     get the dimension scale values
             setname()      set the dimension name
             setscale()     set the dimension scale values

           reading/writing standard attributes
             getstrs()      get the dimension standard string attributes:
                              long_name, units, format
             setstrs()      set the dimension standard string attributes
             
Examples
--------

Example-1

The following simple example exercises some important pyhdf.SD methods. It
shows how to create an HDF dataset, define attributes and dimensions,
create variables, and assign their contents.

Suppose we have a series of text files each defining a 2-dimensional real-
values matrix. First line holds the matrix dimensions, and following lines
hold matrix values, one row per line. The following procedure will load
into an HDF dataset the contents of any one of those text files. The
procedure computes the matrix min and max values, storing them as
dataset attributes. It also assigns to the variable the group of
attributes passed as a dictionnary by the calling program. Note how simple
such an assignment becomes with pyhdf: the dictionnary can contain any
number of attributes, of different types, single or multi-valued. Doing
the same in a conventional language would be a much more challenging task.

Error checking is minimal, to keep example as simple as possible
(admittedly a rather poor excuse ...).


from Numeric import *
from pyhdf.SD import *

import os

def txtToHDF(txtFile, hdfFile, varName, attr):

    try:  # Catch pyhdf errors
        # Open HDF file in update mode, creating it if non existent.
        d = SD(hdfFile, SDC.WRITE|SDC.CREATE)
        # Open text file and get matrix dimensions on first line.
        txt = open(txtFile)
        ni, nj = map(int, txt.readline().split())
        # Define an HDF dataset of 32-bit floating type (SDC.FLOAT32)
        # with those dimensions.
        v = d.create(varName, SDC.FLOAT32, (ni, nj))
        # Assign attributes passed as argument inside dict 'attr'.
        for attrName in attr.keys():
            setattr(v, attrName, attr[attrName])
        # Load variable with lines of data. Compute min and max
        # over the whole matrix.
        i = 0
        while i < ni:
            elems = map(float, txt.readline().split())
            v[i] = elems  # load row i
            minE = min(elems)
            maxE = max(elems)
            if i:
                minVal = min(minVal, minE)
                maxVal = max(maxVal, maxE)
            else:
                minVal = minE
                maxVal = maxE
            i += 1
        # Set variable min and max attributes.
        v.minVal = minVal
        v.maxVal = maxVal
        # Close dataset and file objects (not really necessary, since
        # closing is automatic when objects go out of scope.
        v.endaccess()
        d.end()
        txt.close()
    except HDF4Error, msg:
        print "HDF4Error:", msg


We could now call the procedure as follows:

    hdfFile  = 'table.hdf'
    try:  # Delete if exists.
        os.remove(hdfFile)
    except:
        pass
    # Load contents of file 'temp.txt' into dataset 'temperature'
    # an assign the attributes 'title', 'units' and 'valid_range'.
    txtToHDF('temp.txt', hdfFile, 'temperature',
             {'title'      : 'temperature matrix',
              'units'      : 'celsius',
              'valid_range': (-2.8,27.0)})

    # Load contents of file 'depth.txt' into dataset 'depth'
    # and assign the same attributes as above.
    txtToHDF('depth.txt', hdfFile, 'depth',
             {'title'      : 'depth matrix',
              'units'      : 'meters',
              'valid_range': (0, 500.0)})


Example 2

This example shows a usefull python program that will display the
structure of the SD component of any HDF file whose name is given on
the command line. After the HDF file is opened, high level inquiry methods
are called to obtain dictionnaries descrybing attributes, dimensions and
datasets. The rest of the program mostly consists in nicely formatting
the contents of those dictionaries.

import sys
from pyhdf.SD import *
from Numeric import *

# Dictionnary used to convert from a numeric data type to its symbolic
# representation
typeTab = {
           SDC.CHAR:    'CHAR',
           SDC.CHAR8:   'CHAR8',
	   SDC.UCHAR8:  'UCHAR8',
           SDC.INT8:    'INT8',
           SDC.UINT8:   'UINT8',
           SDC.INT16:   'INT16',
           SDC.UINT16:  'UINT16',
           SDC.INT32:   'INT32',
           SDC.FLOAT32: 'FLOAT32',
           SDC.FLOAT64: 'FLOAT64'
	   }

printf = sys.stdout.write

def eol(n=1):
    printf("%s" % chr(10) * n)
    
hdfFile = sys.argv[1]    # Get first command line argument

try:  # Catch pyhdf.SD errors
  # Open HDF file named on the command line
  f = SD(hdfFile)
  # Get global attribute dictionnary
  attr = f.attributes(full=1)
  # Get dataset dictionnary
  dsets = f.datasets()

  # File name, number of attributes and number of variables.
  printf("FILE INFO"); eol()
  printf("-------------"); eol()
  printf("%-25s%s" % ("File:", hdfFile)); eol()
  printf("%-25s%d" % ("  file attributes:", len(attr))); eol()
  printf("%-25s%d" % ("  datasets:", len(dsets))); eol()
  eol();

  # Global attribute table.
  if len(attr) > 0:
      printf("File attributes"); eol(2)
      printf("  name                 idx type    len value"); eol()
      printf("  -------------------- --- ------- --- -----"); eol()
      # Get list of attribute names and sort them lexically
      attNames = attr.keys()
      attNames.sort()
      for name in attNames:
          t = attr[name]
              # t[0] is the attribute value
              # t[1] is the attribute index number
              # t[2] is the attribute type
              # t[3] is the attribute length
          printf("  %-20s %3d %-7s %3d %s" %
                 (name, t[1], typeTab[t[2]], t[3], t[0])); eol()
      eol()


  # Dataset table
  if len(dsets) > 0:
      printf("Datasets (idx:index num, na:n attributes, cv:coord var)"); eol(2)
      printf("  name                 idx type    na cv dimension(s)"); eol()
      printf("  -------------------- --- ------- -- -- ------------"); eol()
      # Get list of dataset names and sort them lexically
      dsNames = dsets.keys()
      dsNames.sort()
      for name in dsNames:
          # Get dataset instance
          ds = f.select(name)
          # Retrieve the dictionary of dataset attributes so as
          # to display their number
          vAttr = ds.attributes()
          t = dsets[name]
              # t[0] is a tuple of dimension names
              # t[1] is a tuple of dimension lengths
              # t[2] is the dataset type
              # t[3] is the dataset index number
          printf("  %-20s %3d %-7s %2d %-2s " %
                 (name, t[3], typeTab[t[2]], len(vAttr),
                  ds.iscoordvar() and 'X' or ''))
	  # Display dimension info.
          n = 0
          for d in t[0]:
              printf("%s%s(%d)" % (n > 0 and ', ' or '', d, t[1][n]))
              n += 1
          eol()
      eol()

  # Dataset info.
  if len(dsNames) > 0:
      printf("DATASET INFO"); eol()
      printf("-------------"); eol(2)
      for name in dsNames:
          # Access the dataset
          dsObj = f.select(name)
	  # Get dataset attribute dictionnary
          dsAttr = dsObj.attributes(full=1)
          if len(dsAttr) > 0:
              printf("%s attributes" % name); eol(2)
              printf("  name                 idx type    len value"); eol()
              printf("  -------------------- --- ------- --- -----"); eol()
	      # Get the list of attribute names and sort them alphabetically.
              attNames = dsAttr.keys()
              attNames.sort()
              for nm in attNames:
                  t = dsAttr[nm]
                      # t[0] is the attribute value
                      # t[1] is the attribute index number
                      # t[2] is the attribute type
                      # t[3] is the attribute length
                  printf("  %-20s %3d %-7s %3d %s" %
                         (nm, t[1], typeTab[t[2]], t[3], t[0])); eol()
              eol()
	  # Get dataset dimension dictionnary
          dsDim = dsObj.dimensions(full=1)
	  if len(dsDim) > 0:
	      printf ("%s dimensions" % name); eol(2)
              printf("  name                 idx len   unl type    natt");eol()
	      printf("  -------------------- --- ----- --- ------- ----");eol()
	      # Get the list of dimension names and sort them alphabetically.
	      dimNames = dsDim.keys()
	      dimNames.sort()
	      for nm in dimNames:
	          t = dsDim[nm]
		      # t[0] is the dimension length
		      # t[1] is the dimension index number
		      # t[2] is 1 if the dimension is unlimited, 0 if not
		      # t[3] is the the dimension scale type, 0 if no scale
		      # t[4] is the number of attributes
		  printf("  %-20s %3d %5d  %s  %-7s %4d" %
		         (nm, t[1], t[0], t[2] and "X" or " ", 
			  t[3] and typeTab[t[3]] or "", t[4])); eol()
	      eol()

      
except HDF4Error, msg:
    print "HDF4Error", msg



"""
import os, sys, types

import sdext as _C

# List of names we want to be imported by an "from pyhdf import *"
# statement

__all__ = ['SD', 'SDAttr', 'SDC', 'SDS', 'SDim',
           'HDF4Error']


class SDC:
    """The SDC class holds contants defining opening modes and data types."""

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
    FLOAT32      = _C.DFNT_FLOAT32
    FLOAT64      = _C.DFNT_FLOAT64

    FILL         = _C.SD_FILL
    NOFILL       = _C.SD_NOFILL

    UNLIMITED    = _C.SD_UNLIMITED

    COMP_NONE    = _C.COMP_CODE_NONE
    COMP_RLE     = _C.COMP_CODE_RLE
    COMP_NBIT    = _C.COMP_CODE_NBIT
    COMP_SKPHUFF = _C.COMP_CODE_SKPHUFF
    COMP_DEFLATE = _C.COMP_CODE_DEFLATE
    

# NOTE:
#  UCHAR8 and UINT8 are handled similarly (signed byte -128,...,0,...127)
#  UINT32, INT64 and UINT64 are not yet supported py pyhdf

class SDAttr:

    def __init__(self, obj, index_or_name):
        """Init an SDAttr instance. Should not be called directly by
        the user program. An SDAttr instance must be created through
        the attr() methos of the SD, SDS or SDim classes.
                                                """
        # Args
        #  obj   object instance to which the attribute refers
        #        (SD, SDS, SDDim)
        #  index_or_name attribute index or name
        #
        # Class private attributes:
        #  _obj   object instance
        #  _index attribute index or None
        #  _name  attribute name or None

        self._obj = obj
        # Name is given, may exist or not.
        if type(index_or_name) == type(''):
            self._name = index_or_name
            self._index = None
        # Index is given. Must exist.
        else:
            self._index = index_or_name
            status, self._name, data_type, n_values = \
                    _C.SDattrinfo(self._obj._id, self._index)
            _checkErr('set', status, 'illegal attribute index')
    
    def info(self):
        """Retrieve info about the attribute : name, data type and
        number of values.
 
        Args:
          no argument

        Returns: 
          3-element tuple holding:
            -attribute name
            -attribute data type (see constants SDC.xxx)
            -number of values in the attribute; for a string-valued
             attribute (data type SDC.CHAR8), the number of values
             corresponds to the string length
            
 
        C library equivalent : SDattrinfo
                               Note: The C function does not accept an
                               attribute name as argument.
                                                       """
        if self._index is None:
            try:
                self._index = self._obj.findattr(self._name)
            except HDF4Error:
                raise HDF4Error, "info: cannot convert name to index"
        status, self._name, data_type, n_values = \
                              _C.SDattrinfo(self._obj._id, self._index)
        _checkErr('info', status, 'illegal attribute index')
        return self._name, data_type, n_values

    def index(self):
        """Retrieve the attribute index number.
 
        Args:
          no argument
        Returns: 
          attribute index number (starting at 0)
 
        C library equivalent : SDfindattr 
                                             """

        self._index = _C.SDfindattr(self._obj._id, self._name)
        _checkErr('find', self._index, 'illegal attribute name')
        return self._index

    def get(self):
        """Retrieve the attribute value.
 
        Args:
          no argument
        Returns: 
          attribute value(s); a list is returned if the attribute
          is made up of more than one value, except in the case of a 
          string-valued attribute (data type SDC.CHAR8) where the 
          values are returned as a string
 
        C library equivalent : SDreadattr
                               Note: The C function does not accept an
                               attribute name as argument.

        Attributes can also be read like ordinary python attributes,
        using the dot notation. See "High level attribute access".
        
                                                """

        if self._index is None:
            try:
                self._index = self._obj.findattr(self._name)
            except HDF4Error:
                raise HDF4Error, "get: cannot convert name to index"

        # Obtain attribute type and the number of values.
        status, self._name, data_type, n_values = \
                    _C.SDattrinfo(self._obj._id, self._index)
        _checkErr('read', status, 'illegal attribute index')

        # Get attribute value.
        convert = _array_to_ret
        if data_type == SDC.CHAR8:
            buf = _C.array_byte(n_values)
            convert = _array_to_str

        elif data_type in [SDC.UCHAR8, SDC.UINT8]:
            buf = _C.array_byte(n_values)

        elif data_type == SDC.INT8:
            buf = _C.array_int8(n_values)

        elif data_type == SDC.INT16:
            buf = _C.array_int16(n_values)

        elif data_type == SDC.UINT16:
            buf = _C.array_uint16(n_values)

        elif data_type == SDC.INT32:
            buf = _C.array_int32(n_values)

        elif data_type == SDC.FLOAT32:
            buf = _C.array_float32(n_values)

        elif data_type == SDC.FLOAT64:
            buf = _C.array_float64(n_values)

        else:
            raise HDF4Error, "read: attribute index %d has an "\
                             "illegal or unupported type %d" % \
                             (self._index, data_type)

        status = _C.SDreadattr(self._obj._id, self._index, buf)
        _checkErr('read', status, 'illegal attribute index')
        return convert(buf, n_values)

    def set(self, data_type, values):
        """Update/Create a new attribute and set its value(s).
 
        Args:
          data_type    : attribute data type (see constants SDC.xxx)
          values       : attribute value(s); specify a list to create
                         a multi-valued attribute; a string valued
                         attribute can be created by setting 'data_type'
                         to SDC.CHAR8 and 'values' to the corresponding
                         string
                     
        Returns: 
          None
 
        C library equivalent : SDsetattr

        Attributes can also be written like ordinary python attributes,
        using the dot notation. See "High level attribute access".
        
                                                  """
        n_values = len(values)
        if data_type == SDC.CHAR8:
            buf = _C.array_byte(n_values)
            # Allow values to be passed as a string. 
            # Noop if a list is passed.
            values = list(values)
            for n in range(n_values):
                values[n] = ord(values[n])

        elif data_type in [SDC.UCHAR8, SDC.UINT8]:
            buf = _C.array_byte(n_values)

        elif data_type == SDC.INT8:
            # SWIG refuses negative values here. We found that if we
            # pass them as byte values, it will work.
            buf = _C.array_int8(n_values)
            values = list(values)
            for n in range(n_values):
                v = values[n]
                if v >= 0:
                    v &= 0x7f
                else:
                    v = abs(v) & 0x7f
                    if v:
                        v = 256 - v
                    else:
                        v = 128         # -128 in 2s complement
                values[n] = v

        elif data_type == SDC.INT16:
            buf = _C.array_int16(n_values)

        elif data_type == SDC.UINT16:
            buf = _C.array_uint16(n_values)

        elif data_type == SDC.INT32:
            buf = _C.array_int32(n_values)

        elif data_type == SDC.FLOAT32:
            buf = _C.array_float32(n_values)

        elif data_type == SDC.FLOAT64:
            buf = _C.array_float64(n_values)

        else:
            raise HDF4Error, "set: illegal or unimplemented data_type"

        for n in range(n_values):
            buf[n] = values[n]
        status = _C.SDsetattr(self._obj._id, self._name,
                              data_type, n_values, buf)
        _checkErr('set', status, 'illegal attribute')
        # Init index following attribute creation.
        self._index = _C.SDfindattr(self._obj._id, self._name)
        _checkErr('find', self._index, 'illegal attribute')


class SD:
    """The SD class implements an HDF SD interface.
    To instantiate an SD class, call the SD() constructor.
    To set attributes on an SD instance, call the SD.attr()
    method to create an attribute instance, then call the methods
    of this instance. """


    def __init__(self, path, mode=SDC.READ):
        """Initialize an SD interface on an HDF file,
        creating the file if necessary.
 
        Args:
          path    name of the HDF file on which to open the SD interface
          mode    file opening mode; this mode is a set of binary flags
	          which can be ored together
		      
		      SDC.CREATE  combined with SDC.WRITE to create file 
                                  if it does not exist
                      SDC.READ    open file in read-only access (default)
                      SDC.TRUNC   if combined with SDC.WRITE, overwrite
                                  file if it already exists
                      SDC.WRITE   open file in read-write mode; if file
                                  exists it is updated, unless SDC.TRUNC is
                                  set, in which case it is erased and
                                  recreated; if file does not exist, an
                                  error is raised unless SDC.CREATE is set,
                                  in which case the file is created

                   Note an important difference in the way CREATE is
                   handled by the HDF library and the pyhdf package.
                   For the library, CREATE indicates that a new file should
                   always be created, overwriting an existing one if
                   any. For pyhdf, CREATE indicates a new file should be
                   created only if it does not exist, and the overwriting
                   of an already existing file must be explicitly asked
                   for by setting the TRUNC flag.

                   Those differences were introduced so as to harmonize
                   the way files are opened in the pycdf and pyhdf
                   packages. Also, this solves a limitation in the
                   hdf (and netCDF) library, where there is no easy way
                   to implement the frequent requirement where
                   a file has to be opened in read-write mode, or created
                   if it does not exist.
	
        Returns:
          an SD instance
 
        C library equivalent : SDstart
	                                             """
	# Private attributes:
	#  _id:       file id
                                                   
        # See if file exists.
        exists = os.path.exists(path)

        if SDC.WRITE & mode:
            if exists:
                if SDC.TRUNC & mode:
                    try:
                        os.remove(path)
                    except Exception, msg:
                        raise HDF4Error, msg
                    mode = SDC.CREATE|SDC.WRITE
                else:
                    mode = SDC.WRITE
            else:
                if SDC.CREATE & mode:
                    mode |= SDC.WRITE
                else:
                    raise HDF4Error, "SD: no such file"
        else:
            if exists:
                mode = SDC.READ
            else:
                raise HDF4Error, "SD: no such file"
                
        id = _C.SDstart(path, mode)
        _checkErr('SD', id, "cannot open %s" % path)
        self._id = id
        

    def __del__(self):
        """Delete the instance, first calling the end() method 
        if not already done.          """

        try:
            if self._id:
                self.end()
        except:
            pass

    def __getattr__(self, name):
        # Get value(s) of SD attribute 'name'.

        return _getattr(self, name)

    def __setattr__(self, name, value):
        # Set value(s) of SD attribute 'name'.

        _setattr(self, name, value, ['_id'])

    def end(self):
        """End access to the SD interface and close the HDF file.
  
        Args:
            no argument
        Returns: 
            None
  
        The instance should not be used afterwards.
        The 'end()' method is implicitly called when the
        SD instance is deleted.
 
        C library equivalent : SDend
                                                      """

        status = _C.SDend(self._id)
        _checkErr('end', status, "cannot execute")
        self._id = None

    def info(self):
        """Retrieve information about the contents of the HDF file.
 
        Args:
          no argument
        Returns: 
          2-element tuple holding:
            number of datasets inside the file
            number of file attributes
 
        C library equivalent : SDfileinfo
                                                  """

        status, n_datasets, n_file_attrs = _C.SDfileinfo(self._id)
        _checkErr('info', status, "cannot execute")
        return n_datasets, n_file_attrs

    def nametoindex(self, sds_name):
        """Return the index number of a dataset given the dataset name.
   
        Args:
          sds_name  : dataset name
        Returns:
          index number of the dataset
 
        C library equivalent : SDnametoindex
                                                 """

        sds_idx = _C.SDnametoindex(self._id, sds_name)
        _checkErr('nametoindex', sds_idx, 'non existent SDS')
        return sds_idx

    def reftoindex(self, sds_ref):
        """Returns the index number of a dataset given the dataset 
        reference number.
 
        Args:
          sds_ref : dataset reference number
        Returns:
          dataset index number
  
        C library equivalent : SDreftoindex
                                             """

        sds_idx = _C.SDreftoindex(self._id, sds_ref)
        _checkErr('reftoindex', sds_idx, 'illegal SDS ref number')
        return sds_idx

    def setfillmode(self, fill_mode):
        """Set the fill mode for all the datasets in the file.
 
        Args:
          fill_mode : fill mode; one of :
                        SDC.FILL   write the fill value to all the datasets
                                  of the file by default
                        SDC.NOFILL do not write fill values to all datasets
                                  of the file by default
        Returns: 
          previous fill mode value
  
        C library equivalent: SDsetfillmode
                                                            """

        if not fill_mode in [SDC.FILL, SDC.NOFILL]:
            raise HDF4Error, "bad fill mode"
        old_mode = _C.SDsetfillmode(self._id, fill_mode)
        _checkErr('setfillmode', old_mode, 'cannot execute')
        return old_mode

    def create(self, name, data_type, dim_sizes):
        """Create a dataset.
        
        Args:
          name           dataset name
          data_type      type of the data, set to one of the SDC.xxx 
                         constants; 
          dim_sizes      lengths of the dataset dimensions; a one-
                         dimensional array is specified with an integer,
                         an n-dimensional array with an n-element sequence
                         of integers; the length of the first dimension can
                         be set to SDC.UNLIMITED to create a "record"
                         variable.

                         IMPORTANT:  netCDF and HDF differ in the way
                         the UNLIMITED dimension is handled. In netCDF,
                         all variables of a dataset with an unlimited
                         dimension grow in sync, eg adding a record to
                         a variable will implicitly extend other record
                         variables. In HDF, each record variable grows
                         independently of each other.
                    
        Returns: 
          SDS instance for the dataset

        C library equivalent : SDcreate
   
                                                                    """

        # Validate args.
        if type(dim_sizes) == type(1):  # allow k instead of [k] 
                                        # for a 1-dim arr
            dim_sizes = [dim_sizes]
        rank = len(dim_sizes)
        buf = _C.array_int32(rank)
        for n in range(rank):
            buf[n] = dim_sizes[n]
        id = _C.SDcreate(self._id, name, data_type, rank, buf)
        _checkErr('CREATE', id, "cannot execute")
        return SDS(self, id)

    def select(self, name_or_index):
        """Locate a dataset.
        
        Args:
          name_or_index  dataset name or index number
                    
        Returns: 
          SDS instance for the dataset

        C library equivalent : SDselect
                                                                    """

        if type(name_or_index) == type(1):
            idx = name_or_index
        else:
            try:
                idx = self.nametoindex(name_or_index)
            except HDF4Error:
                raise HDF4Error, "select: non-existent dataset"
        id = _C.SDselect(self._id, idx)
        _checkErr('select', id, "cannot execute")
        return SDS(self, id)

    def attr(self, name_or_index):
        """Create an SDAttr instance representing a global
        (file) attribute.

        Args:
          name_or_index   attribute name or index number; if a name is
                          given, the attribute may not exist; in that
                          case, it will be created when the SDAttr
                          instance set() method is called

        Returns:
          SDAttr instance for the attribute. Call the methods of this
          class to query, read or set the attribute.

        C library equivalent : no equivalent

                                """

        return SDAttr(self, name_or_index)


    def attributes(self, full=0):
        """Return a dictionnary describing every global
	attribute attached to the HDF file.

	Args:
          full      true to get complete info about each attribute
                    false to report only each attribute value
	Returns:
          Empty dictionnary if no global attribute defined
	  Otherwise, dictionnary where each key is the name of a
	  global attribute. If parameter 'full' is false,
	  key value is the attribute value. If 'full' is true,
	  key value is a tuple with the following elements:
	    - attribute value
	    - attribute index number
	    - attribute type
	    - attribute length

        C library equivalent : no equivalent
	                                            """

        # Get the number of global attributes.
	nsds, natts = self.info()

	# Inquire each attribute
	res = {}
	for n in range(natts):
            a = self.attr(n)
	    name, aType, nVal = a.info()
	    if full:
	        res[name] = (a.get(), a.index(), aType, nVal)
	    else:
	        res[name] = a.get()

        return res

    def datasets(self):
        """Return a dictionnary describing all the file datasets.

        Args:
          no argument
        Returns:
          Empty dictionnary if no dataset is defined.
          Otherwise, dictionnary whose keys are the file dataset names,
          and values are tuples describing the corresponding datasets.
          Each tuple holds the following elements in order:
            -tuple holding the names of the dimensions defining the
             dataset coordinate axes
            -tuple holding the dataset shape (dimension lengths);
             if a dimension is unlimited, the reported length corresponds
             to the dimension current length
            -dataset type
            -dataset index number

        C library equivalent : no equivalent
                                                """
        # Get number of datasets
        nDs = self.info()[0]

        # Inquire each var
        res = {}
        for n in range(nDs):
            # Get dataset info.
            v = self.select(n)
            vName, vRank, vLen, vType, vAtt = v.info()
            if vRank < 2:     # need a sequence
                vLen = [vLen]
            # Get dimension info.
            dimNames = []
            dimLengths = []
            for dimNum in range(vRank):
                d = v.dim(dimNum)
                dimNames.append(d.info()[0])
                dimLengths.append(vLen[dimNum])
            res[vName] = (tuple(dimNames), tuple(dimLengths),
                         vType, n)

        return res
        

class SDS:
    """The SDS class implements an HDF dataset object.
    To create an SDS instance, call the create() or select()
    methods of the SD class. To set attributes on an SDS instance,
    call the SDS.attr() method to create an attribute instance,
    then call the methods of this instance. """

    def __init__(self, sd, id):
        """This constructor should not be called by the user program.
        Call the SD.create() and SD.select() methods instead.
                                                  """

        # Args
        #  sd   : SD instance
        #  id   : SDS identifier
        

        # Private attributes
        #  _sd  SD intance
        #  _id  SDS identifier
        self._sd = sd
        self._id = id

    def __del__(self):

        # Delete the instance, first calling the endaccess() method
        # if not already done.

        try:
            if self._id:
                self.endaccess()
        except:
            pass

    def __getattr__(self, name):
        # Get value(s) of SDS attribute 'name'.

        return _getattr(self, name)

    def __setattr__(self, name, value):
        # Set value(s) of SDS attribute 'name'.

        _setattr(self, name, value, ['_sd', '_id'])

    def __len__(self):    # Needed for slices like "-2:" but why ?

        return 0

    def __getitem__(self, elem):

        # This special method is used to index the SDS dataset
        # using the "extended slice syntax". The extended slice syntax
        # is a perfect match for the "start", "count" and "stride"
        # arguments to the SDreaddara() function, and is much more easy
        # to use.

        # Compute arguments to 'SDreaddata_0()'.
        start, count, stride = self.__buildStartCountStride(elem)
        # Get elements.
        return self.get(start, count, stride)

    def __setitem__(self, elem, data):

        # This special method is used to assign to the SDS dataset
        # using "extended slice syntax". The extended slice syntax
        # is a perfect match for the "start", "count" and "stride"
        # arguments to the SDwritedata() function, and is much more easy
        # to use.

        # Compute arguments to 'SDwritedata_0()'.
        start, count, stride = self.__buildStartCountStride(elem)
        # A sequence type is needed. Convert a single number to a list.
        if type(data) in [types.IntType, types.FloatType]:
            data = [data]
        # Assign.
        self.set(data, start, count, stride)

    def endaccess(self):
        """Terminates access to the SDS.
 
        Args:
          no argument
        Returns: 
          None.
    
        The SDS instance should not be used afterwards.
        The 'endaccess()' method is implicitly called when
        the SDS instance is deleted.
 
        C library equivalent : SDendaccess
                                                 """

        status = _C.SDendaccess(self._id)
        _checkErr('endaccess', status, "cannot execute")
        self._id = None    # Invalidate identifier


    def dim(self, dim_index):
        """Get an SDim instance given a dimension index number.
  
        Args:
          dim_index index number of the dimension (numbering starts at 0)
 
        C library equivalent : SDgetdimid
                                                    """
        id = _C.SDgetdimid(self._id, dim_index)
        _checkErr('dim', id, 'invalid SDS identifier or dimension index')
        return SDim(self, id, dim_index)
    
    def get(self, start=None, count=None, stride=None):
        """Read data from the dataset.
 
        Args:
          start   : indices where to start reading in the data array;
                    default to 0 on all dimensions
          count   : number of values to read along each dimension;
                    default to the current length of all dimensions
          stride  : sampling interval along each dimension;
                    default to 1 on all dimensions
   
          For n-dimensional datasets, those 3 parameters are entered 
          using lists. For one-dimensional datasets, integers
          can also be used.
  
          Note that, to read the whole dataset contents, one should
          simply call the method with no argument.
   
        Returns: 
          Numeric array initialized with the data.
  
        C library equivalent : SDreaddata

        The dataset can also be read using the familiar indexing and
        slicing notation, like ordinary python sequences.
        See "High level variable access".
        
                                                       """
 
        # Obtain SDS info.
        try:
            sds_name, rank, dim_sizes, data_type, n_attrs = self.info()
            if type(dim_sizes) == type(1):
                dim_sizes = [dim_sizes]
        except HDF4Error:
            raise HDF4Error, 'get : cannot execute'

        # Validate args.
        if start is None:
            start = [0] * rank
        elif type(start) == type(1):
            start = [start]
        if count is None:
            count = dim_sizes
            if count[0] == 0:
                count[0] = 1
        elif type(count) == type(1):
            count = [count]
        if stride is None:
            stride = [1] * rank
        elif type(stride) == type(1):
            stride = [stride]
        if len(start) != rank or len(count) != rank or len(stride) != rank:
            raise HDF4Error, 'get : start, stride or count ' \
                             'do not match SDS rank'
        for n in range(rank):
            if start[n] < 0 or start[n] + \
                  (abs(count[n]) - 1) * stride[n] >= dim_sizes[n]:
                raise HDF4Error, 'get arguments violate ' \
                                 'the size (%d) of dimension %d' \
                                 % (dim_sizes[n], n)
        if not data_type in [SDC.FLOAT32, SDC.FLOAT64, SDC.INT8, SDC.UINT8,
                             SDC.INT16, SDC.INT32, SDC.CHAR8, SDC.UCHAR8]:
            raise HDF4Error, 'get cannot currrently deal with '\
                             'the SDS data type'

        return _C._SDreaddata_0(self._id, data_type, start, count, stride)

    def set(self, data, start=None, count=None, stride=None):
        """Write data to the dataset.
 
        Args:
          data    : array of data to write; can be given as a Numeric
                    array, or as Python sequence (whose elements can be
                    imbricated sequences)
          start   : indices where to start writing in the dataset;
                    default to 0 on all dimensions
          count   : number of values to write along each dimension;
                    default to the current length of dataset dimensions
          stride  : sampling interval along each dimension;
                    default to 1 on all dimensions
   
          For n-dimensional datasets, those 3 parameters are entered 
          using lists. For one-dimensional datasets, integers
          can also be used.
   
          Note that, to write the whole dataset at once, one has simply
          to call the method with the dataset values in parameter
          'data', omitting all other parameters.
 
        Returns: 
          None.
  
        C library equivalent : SDwritedata

        The dataset can also be written using the familiar indexing and
        slicing notation, like ordinary python sequences.
        See "High level variable access".
        
                                              """
  

        # Obtain SDS info.
        try:
            sds_name, rank, dim_sizes, data_type, n_attrs = self.info()
            if type(dim_sizes) == type(1):
                dim_sizes = [dim_sizes]
        except HDF4Error:
            raise HDF4Error, 'set : cannot execute'

        # Validate args.
        if start is None:
            start = [0] * rank
        elif type(start) == type(1):
            start = [start]
        if count is None:
            count = dim_sizes
            if count[0] == 0:
                count[0] = 1
        elif type(count) == type(1):
            count = [count]
        if stride is None:
            stride = [1] * rank
        elif type(stride) == type(1):
            stride = [stride]
        if len(start) != rank or len(count) != rank or len(stride) != rank:
            raise HDF4Error, 'set : start, stride or count '\
                             'do not match SDS rank'
        unlimited = self.isrecord()    
        for n in range(rank):
            ok = 1
            if start[n] < 0:
                ok = 0
            elif n > 0 or not unlimited:
                if start[n] + (abs(count[n]) - 1) * stride[n] >= dim_sizes[n]:
                    ok = 0
            if not ok:
                raise HDF4Error, 'set arguments violate '\
                                 'the size (%d) of dimension %d' \
                                 % (dim_sizes[n], n)
        # ??? Check support for UINT16
        if not data_type in [SDC.FLOAT32, SDC.FLOAT64, SDC.INT8, SDC.UINT8,
                             SDC.INT16, SDC.INT32, SDC.CHAR8, SDC.UCHAR8]:
            raise HDF4Error, 'set cannot currrently deal '\
                             'with the SDS data type'

        _C._SDwritedata_0(self._id, data_type, start, count, data, stride)

    def __buildStartCountStride(self, elem):

        # Create the 'start', 'count', 'slice' and 'stride' tuples that
        # will be passed to '_SDreaddata_0'/'_SDwritedata_0'.
        #   start     starting indices along each dimension
        #   count     count of values along each dimension; a value of -1
        #             indicates that and index, not a slice, was applied to
        #             the dimension; in that case, the dimension should be
        #             dropped from the output array.
        #   stride    strides along each dimension

        
        # Make sure the indexing expression does not exceed the variable
        # number of dimensions.
        dsName, nDims, shape, dsType, nAttr = self.info()
        if type(elem) == types.TupleType:
            if len(elem) > nDims:
                raise HDF4Error("get", 0,
                               "indexing expression exceeds variable "
                               "number of dimensions")
        else:   # Convert single index to sequence
            elem = [elem]
        if type(shape) == types.IntType:
            shape = [shape]

        start = []
        count = []
        stride = []
        n = -1
        unlimited = self.isrecord()
        for e in elem:
            n += 1
            # See if the dimension is unlimited (always at index 0)
            unlim = n == 0 and unlimited
            # Simple index
            if type(e) == types.IntType:
                slice = 0
                if e < 0 :
                    e += shape[n]
                # Respect standard python list behavior: it is illegal to
                # specify an out of bound index (except for the
                # unlimited dimension).
                if e < 0 or (not unlim and e >= shape[n]):
                    raise IndexError, "index out of range"
                beg = e
                end = e + 1
                inc = 1
            # Slice index. Respect Python syntax for slice upper bounds,
            # which are not included in the resulting slice. Also, if the
            # upper bound exceed the dimension size, truncate it.
            elif type(e) == types.SliceType:
                slice = 1
                # None or 0 means not specified
                if e.start:
                    beg = e.start
                    if beg < 0:
                        beg += shape[n]
                else:
                    beg = 0
                # None of maxint means not specified
                if e.stop and e.stop != sys.maxint:
                    end = e.stop
                    if end < 0:
                        end += shape[n]
                else:
                    end = shape[n]
                # None means not specified
                if e.step:
                    inc = e.step
                else:
                    inc = 1
            # Bug
            else:
                raise ValueError, \
                      "Bug: unexpected element type to __getitem__"

            # Clip end index (except if unlimited dimension)
            # and compute number of elements to get.
            if not unlim and end > shape[n]:
                end = shape[n]
            if slice:
                cnt = (end - beg) / inc
                if cnt * inc < end - beg:
                    cnt += 1
            else:
                cnt = -1
            start.append(beg)
            count.append(cnt)
            stride.append(inc)

        # Complete missing dimensions
        while n < nDims - 1:
            n += 1
            start.append(0)
            count.append(shape[n])
            stride.append(1)

        # Done
        return start, count, stride

    def info(self):
        """Retrieves information about the dataset.
       
        Args:
          no argument
        Returns: 
          5-element tuple holding :
            -dataset name
            -dataset rank (number of dimensions)
            -dataset shape, that is a list giving the length of each
             dataset dimension; if the first dimension is unlimited, then
             the first value of the list gives the current length of the
             unlimited dimension
            -data type (one of the SDC.xxx values)
            -number of attributes defined for the dataset
  
        C library equivalent : SDgetinfo
                                                       """

        buf = _C.array_int32(32)      # a rank higher than that is insane!
        status, sds_name, rank, data_type, n_attrs = \
                _C.SDgetinfo(self._id, buf)
        _checkErr('info', status, "cannot execute")
        dim_sizes = _array_to_ret(buf, rank)
        return sds_name, rank, dim_sizes, data_type, n_attrs

    def checkempty(self):
        """Determine whether the dataset is empty.
 
        Args:
          no argument
        Returns:
          True(1) if dataset is empty, False(0) if not
  
        C library equivalent : SDcheckempty
                                                 """

        status, emptySDS = _C.SDcheckempty(self._id)
        _checkErr('checkempty', status, 'invalid SDS identifier')
        return emptySDS

    def ref(self):
        """Get the reference number of the dataset.
 
        Args:
          no argument
        Returns:
          dataset reference number
  
        C library equivalent : SDidtoref
                                              """

        sds_ref = _C.SDidtoref(self._id)
        _checkErr('idtoref', sds_ref, 'illegal SDS identifier')
        return sds_ref

    def iscoordvar(self):
        """Determine whether the dataset is a coordinate variable 
        (holds a dimension scale). A coordinate variable is created
        when a dimension is assigned a set of scale values.
 
        Args:
          no argument
        Returns:
          True(1) if the dataset represents a coordinate variable, 
          False(0) if not
 
        C library equivalent : SDiscoordvar
                                           """
 
        return _C.SDiscoordvar(self._id)   # no error status here

    def isrecord(self):
        """Determines whether the dataset is appendable 
        (contains an unlimited dimension). Note that if true, then
        the unlimited dimension is always dimension number 0.
 
        Args:
          no argument
        Returns:
          True(1) if the dataset is appendable, False(0) if not.
 
        C library equivalent : SDisrecord
                                        """

        return _C.SDisrecord(self._id)     # no error status here


    def getcal(self):
        """Retrieve the SDS calibration coefficients. 
 
        Args:
          no argument
        Returns:
          5-element tuple holding :
            -cal: calibration factor (attribute 'scale_factor')
            -cal_error : calibration factor error
                         (attribute 'scale_factor_err')
            -offset: calibration offset (attribute 'add_offset')
            -offset_err : offset error (attribute 'add_offset_err')
            -data_type : type of the data resulting from applying
                         the calibration formula to the dataset values
                         (attribute 'calibrated_nt')
 
        An exception is raised if no calibration data are defined.
        
        Original dataset values 'orival' are converted to calibrated
        values 'calval' through the formula :
           calval = cal * (orival - offset)
 
        The calibration coefficients are part of the so-called
        "standard" SDS attributes. The values inside the tuple returned 
        by 'getcal' are those of the following attributes, in order :
          scale_factor, scale_factor_err, add_offset, add_offset_err,
          calibrated_nt
  
        C library equivalent: SDgetcal()
                                               """

        status, cal, cal_error, offset, offset_err, data_type = \
                         _C.SDgetcal(self._id)
        _checkErr('getcal', status, 'no calibration record')
        return cal, cal_error, offset, offset_err, data_type

    def getdatastrs(self):
        """Retrieve the dataset standard string attributes.
 
        Args:
          no argument
        Returns:
          4-element tuple holding :
            -dataset label string (attribute 'long_name')
            -dataset unit (attribute 'units')
            -dataset output format (attribute 'format')
            -dataset coordinate system (attribute 'coordsys')
  
        The values returned by 'getdatastrs' are part of the
        so-called "standard" SDS attributes.  Those 4 values 
        correspond respectively to the following attributes: 
          long_name, units, format, coordsys .
  
        C library equivalent: SDgetdatastrs
                                                       """

        status, label, unit, format, coord_system = \
               _C.SDgetdatastrs(self._id, 128)
        _checkErr('getdatastrs', status, 'cannot execute')
        return label, unit, format, coord_system

    def getfillvalue(self):
        """Retrieve the dataset fill value.
 
        Args:
          no argument
        Returns:
          dataset fill value (attribute '_FillValue')

        An exception is raised if the fill value is not set.
  
        The fill value is part of the so-called "standard" SDS
        attributes, and corresponds to the following attribute :
          _FillValue
 
        C library equivalent: SDgetfillvalue
                                                   """

        # Obtain SDS data type.
        try:
            sds_name, rank, dim_sizes, data_type, n_attrs = \
                                self.info()
        except HDF4Error:
            raise HDF4Error, 'getfillvalue : invalid SDS identifier'
        n_values = 1   # Fill value stands for 1 value.

        convert = _array_to_ret
        if data_type == SDC.CHAR8:
            buf = _C.array_byte(n_values)
            convert = _array_to_str

        elif data_type in [SDC.UCHAR8, SDC.UINT8]:
            buf = _C.array_byte(n_values)

        elif data_type == SDC.INT8:
            buf = _C.array_int8(n_values)

        elif data_type == SDC.INT16:
            buf = _C.array_int16(n_values)

        elif data_type == SDC.UINT16:
            buf = _C.array_uint16(n_values)

        elif data_type == SDC.INT32:
            buf = _C.array_int32(n_values)

        elif data_type == SDC.FLOAT32:
            buf = _C.array_float32(n_values)

        elif data_type == SDC.FLOAT64:
            buf = _C.array_float64(n_values)

        else:
            raise HDF4Error, "getfillvalue: SDS has an illegal type or " \
                             "unsupported type %d" % data_type

        status = _C.SDgetfillvalue(self._id, buf)
        _checkErr('getfillvalue', status, 'fill value not set')
        return convert(buf, n_values)

    def getrange(self):
        """Retrieve the dataset min and max values.
 
        Args:
          no argument
        Returns: 
          (min, max) tuple (attribute 'valid_range')

          Note that those are the values as stored
          by the 'setrange' method. 'getrange' does *NOT* compute the
          min and max from the current dataset contents.

        An exception is raised if the range is not set.
  
        The range returned by 'getrange' is part of the so-called 
        "standard" SDS attributes. It corresponds to the following
        attribute :
          valid_range
        
        C library equivalent: SDgetrange
                                                       """

        # Obtain SDS data type.
        try:
            sds_name, rank, dim_sizes, data_type, n_attrs = \
                               self.info()
        except HDF4Error:
            raise HDF4Error, 'getrange : invalid SDS identifier'
        n_values = 1

        convert = _array_to_ret
        if data_type == SDC.CHAR8:
            buf1 = _C.array_byte(n_values)
            buf2 = _C.array_byte(n_values)
            convert = _array_to_str

        elif data_type in  [SDC.UCHAR8, SDC.UINT8]:
            buf1 = _C.array_byte(n_values)
            buf2 = _C.array_byte(n_values)

        elif data_type == SDC.INT8:
            buf1 = _C.array_int8(n_values)
            buf2 = _C.array_int8(n_values)

        elif data_type == SDC.INT16:
            buf1 = _C.array_int16(n_values)
            buf2 = _C.array_int16(n_values)

        elif data_type == SDC.UINT16:
            buf1 = _C.array_uint16(n_values)
            buf2 = _C.array_uint16(n_values)

        elif data_type == SDC.INT32:
            buf1 = _C.array_int32(n_values)
            buf2 = _C.array_int32(n_values)

        elif data_type == SDC.FLOAT32:
            buf1 = _C.array_float32(n_values)
            buf2 = _C.array_float32(n_values)

        elif data_type == SDC.FLOAT64:
            buf1 = _C.array_float64(n_values)
            buf2 = _C.array_float64(n_values)

        else:
            raise HDF4Error, "getrange: SDS has an illegal or " \
                             "unsupported type %d" % data

        # Note: The C routine returns the max in buf1 and the min 
        # in buf2. We swap the values returned by the Python
        # interface, since it is more natural to return
        # min first, then max.
        status = _C.SDgetrange(self._id, buf1, buf2)
        _checkErr('getrange', status, 'range not set')
        return convert(buf2, n_values), convert(buf1, n_values)

    def setcal(self, cal, cal_error, offset, offset_err, data_type):
        """Set the dataset calibration coefficients.
 
        Args:
          cal         the calibraton factor (attribute 'scale_factor')
          cal_error   calibration factor error
                      (attribute 'scale_factor_err')
          offset      offset value (attribute 'add_offset')
          offset_err  offset error (attribute 'add_offset_err')
          data_type   data type of the values resulting from applying the
                      calibration formula to the dataset values
                      (one of the SDC.xxx constants)
                      (attribute 'calibrated_nt')
        Returns: 
          None
  
        See method 'getcal' for the definition of the calibration
        formula.
  
        Calibration coefficients are part of the so-called standard
        SDS attributes. Calling 'setcal' is equivalent to setting 
        the following attributes, which correspond to the method 
        parameters, in order: 
          scale_factor, scale_factor_err, add_offset, add_offset_err,
          calibrated_nt
  
        C library equivalent: SDsetcal
                                                      """

        status = _C.SDsetcal(self._id, cal, cal_error,
                             offset, offset_err, data_type)
        _checkErr('setcal', status, 'cannot execute')

    def setdatastrs(self, label, unit, format, coord_sys):
        """Set the dataset standard string type attributes.
 
        Args:
          label         dataset label (attribute 'long_name')
          unit          dataset unit (attribute 'units')
          format        dataset format (attribute 'format')
          coord_sys     dataset coordinate system (attribute 'coordsys')
        Returns:
          None
  
        Those strings are part of the so-called standard
        SDS attributes. Calling 'setdatastrs' is equivalent to setting 
        the following attributes, which correspond to the method 
        parameters, in order: 
          long_name, units, format, coordsys
        
        C library equivalent: SDsetdatastrs
                                                     """

        status = _C.SDsetdatastrs(self._id, label, unit, format, coord_sys)
        _checkErr('setdatastrs', status, 'cannot execute')

    def setfillvalue(self, fill_val):
        """Set the dataset fill value.
 
        Args:
          fill_val   dataset fill value (attribute '_FillValue')
        Returns: 
          None
  
        The fill value is part of the so-called "standard" SDS
        attributes. Calling 'setfillvalue' is equivalent to setting
        the following attribute:
          _FillValue
  
        C library equivalent: SDsetfillvalue
                                                           """

        # Obtain SDS data type.
        try:
            sds_name, rank, dim_sizes, data_type, n_attrs = self.info()
        except HDF4Error:
            raise HDF4Error, 'setfillvalue : cannot execute'
        n_values = 1   # Fill value stands for 1 value.

        if data_type == SDC.CHAR8:
            buf = _C.array_byte(n_values)

        elif data_type in [SDC.UCHAR8, SDC.UINT8]:
            buf = _C.array_byte(n_values)

        elif data_type == SDC.INT8:
            # SWIG refuses negative values here. We found that if we
            # pass them as byte values, it will work.
            buf = _C.array_int8(n_values)
            if fill_val >= 0:
                fill_val &= 0x7f
            else:
                fill_val = abs(fill_val) & 0x7f
                if fill_val:
                    fill_val = 256 - fill_val
                else:
                    fill_val = 128    # -128 in 2's complement

        elif data_type == SDC.INT16:
            buf = _C.array_int16(n_values)

        elif data_type == SDC.UINT16:
            buf = _C.array_uint16(n_values)

        elif data_type == SDC.INT32:
            buf = _C.array_int32(n_values)

        elif data_type == SDC.FLOAT32:
            buf = _C.array_float32(n_values)

        elif data_type == SDC.FLOAT64:
            buf = _C.array_float64(n_values)

        else:
            raise HDF4Error, "setfillvalue: SDS has an illegal or " \
                             "unsupported type %d" % data_type

        buf[0] = fill_val
        status = _C.SDsetfillvalue(self._id, buf)
        _checkErr('setfillvalue', status, 'cannot execute')


    def setrange(self, min, max):
        """Set the dataset min and max values.
 
        Args:
          min        dataset minimum value (attribute 'valid_range')
          max        dataset maximum value (attribute 'valid_range')

        Returns: 
          None
 
        The data range is part of the so-called "standard" SDS
        attributes. Calling method 'setrange' is equivalent to
        setting the following attribute with a 2-element [min,max]
        array :
          valid_range
          
  
        C library equivalent: SDsetrange
                                                   """

        # Obtain SDS data type.
        try:
            sds_name, rank, dim_sizes, data_type, n_attrs = self.info()
        except HDF4Error:
            raise HDF4Error, 'setrange : cannot execute'
        n_values = 1

        if data_type == SDC.CHAR8:
            buf1 = _C.array_byte(n_values)
            buf2 = _C.array_byte(n_values)

        elif data_type in [SDC.UCHAR8, SDC.UINT8]:
            buf1 = _C.array_byte(n_values)
            buf2 = _C.array_byte(n_values)

        elif data_type == SDC.INT8:
            # SWIG refuses negative values here. We found that if we
            # pass them as byte values, it will work.
            buf1 = _C.array_int8(n_values)
            buf2 = _C.array_int8(n_values)
            v = min
            if v >= 0:
                v &= 0x7f
            else:
                v = abs(v) & 0x7f
                if v:
                    v = 256 - v
                else:
                    v = 128    # -128 in 2's complement
            min = v
            v = max
            if v >= 0:
                v &= 0x7f
            else:
                v = abs(v) & 0x7f
                if v:
                    v = 256 - v
                else:
                    v = 128    # -128 in 2's complement
            max = v
            
        elif data_type == SDC.INT16:
            buf1 = _C.array_int16(n_values)
            buf2 = _C.array_int16(n_values)

        elif data_type == SDC.UINT16:
            buf1 = _C.array_uint16(n_values)
            buf2 = _C.array_uint16(n_values)

        elif data_type == SDC.INT32:
            buf1 = _C.array_int32(n_values)
            buf2 = _C.array_int32(n_values)

        elif data_type == SDC.FLOAT32:
            buf1 = _C.array_float32(n_values)
            buf2 = _C.array_float32(n_values)

        elif data_type == SDC.FLOAT64:
            buf1 = _C.array_float64(n_values)
            buf2 = _C.array_float64(n_values)

        else:
            raise HDF4Error, "SDsetrange: SDS has an illegal or " \
                             "unsupported type %d" % data_type

        buf1[0] = max
        buf2[0] = min
        status = _C.SDsetrange(self._id, buf1, buf2)
        _checkErr('setrange', status, 'cannot execute')

    def getcompress(self):
        """Retrieves data set compression type.
 
        Args:
          no argument
        Returns: 
          2-element tuple holding :
            -compression type, one of the SDC.COMP_xxx constants
            -auxiliary value for some of the compression types

        An exception is raised if compression is not set.
  
        C library equivalent: SDgetcompress
                                                           """

        status, comp_type, value = _C._SDgetcompress(self._id)
        _checkErr('getcompress', status, 'no compression')
        return comp_type, value

    def setcompress(self, comp_type, value=0):
        """Compresses the data set using a specified compression method.
 
        Args:
          comp_type    compression type, identified by one of the
                       SDC.COMP_xxx constants
          value        auxiliary value needed by some compression types
                       (data size for SDC.COMP_SKPHUFF, deflate level
                       for SDC.COMP_DEFLATE; omit for other types)
        Returns: None
  
        SDC.COMP_DEFLATE applies the GZIP compression to the dataset,
        and the value varies from 1 to 9, according to the level of
        compression desired.
 
        'setcompress' must be called before writing to the dataset.
        The dataset must be written all at once, unless it is 
        appendable (has an unlimited dimension). Updating the dataset
        in not allowed. Refer to the HDF user's guide for more details 
        on how to use data compression. 
 
        C library equivalent: SDsetcompress
                                                          """

        status = _C._SDsetcompress(self._id, comp_type, value)
        _checkErr('setcompress', status, 'cannot execute')


    def setexternalfile(self, filename, offset=0):
        """Store the dataset data in an external file.
 
        Args:
          filename    external file name
          offset      offset in bytes where to start writing in
                      the external file
        Returns: None
  
        C library equivalent : SDsetexternalfile
                                                  """

        status = _C.SDsetexternalfile(self._id, filename, offset)
        _checkErr('setexternalfile', status, 'execution error')

    def attr(self, name_or_index):
        """Create an SDAttr instance representing an SDS
        (dataset) attribute.

        Args:
          name_or_index   attribute name or index number; if a name is
                          given, the attribute may not exist

        Returns:
          SDAttr instance for the attribute. Call the methods of this
          class to query, read or set the attribute.

        C library equivalent : no equivalent

                                """

        return SDAttr(self, name_or_index)

    def attributes(self, full=0):
        """Return a dictionnary describing every attribute defined
	on the dataset.

	Args:
          full      true to get complete info about each attribute
                    false to report only each attribute value
	Returns:
          Empty dictionnary if no attribute defined.
	  Otherwise, dictionnary where each key is the name of a
	  dataset attribute. If parameter 'full' is false,
	  key value is the attribute value. If 'full' is true,
	  key value is a tuple with the following elements:
	    - attribute value
	    - attribute index number
	    - attribute type
	    - attribute length

        C library equivalent : no equivalent
	                                            """

        # Get the number of dataset attributes.
	natts = self.info()[4]

	# Inquire each attribute
	res = {}
	for n in range(natts):
            a = self.attr(n)
	    name, aType, nVal = a.info()
	    if full:
	        res[name] = (a.get(), a.index(), aType, nVal)
	    else:
	        res[name] = a.get()

        return res

    def dimensions(self, full=0):
        """Return a dictionnary describing every dataset dimension.

	Args:
          full      true to get complete info about each dimension
                    false to report only each dimension length
	Returns:
	  Dictionnary where each key is a dimension name. If no name
          has been given to the dimension, the key is set to
          'fakeDimx' where 'x' is the dimension index number.
	  If parameter 'full' is false, key value is the dimension
          length. If 'full' is true, key value is a 5-element tuple
          with the following elements:
	    - dimension length; for an unlimited dimension, the reported
              length is the current dimension length
	    - dimension index number
	    - 1 if the dimension is unlimited, 0 otherwise
            - dimension scale type, or 0 if no scale is defined for
              the dimension
            - number of attributes defined on the dimension

        C library equivalent : no equivalent
	                                            """

        # Get the number of dimensions and their lengths.
        nDims, dimLen = self.info()[1:3]
        if type(dimLen) == types.IntType:    # need a sequence
            dimLen = [dimLen]
        # Check if the dataset is appendable.
        unlim = self.isrecord()

        # Inquire each dimension
        res = {}
        for n in range(nDims):
            d = self.dim(n)
            # The length reported by info() is 0 for an unlimited dimension.
            # Rather use the lengths reported by SDS.info()
            name, k, scaleType, nAtt = d.info()
            length = dimLen[n]
            if full:
                res[name] = (length, n, unlim and n == 0,
                             scaleType, nAtt)
            else:
                res[name] = length

        return res


class SDim:
    """The SDim class implements a dimension object.
       There can be one dimension object for each dataset dimension.
       To create an SDim instance, call the dim() method of an SDS class
       instance. To set attributes on an SDim instance, call the
       SDim.attr() method to create an attribute instance, then call the
       methods of this instance. """

    def __init__(self, sds, id, index):
        """Init an SDim instance. This method should not be called
        directly by the user program. To create an SDim instance,
        call the SDS.dim() method.
                                                 """
  
        # Args:
        #  sds    SDS instance
        #  id     dimension identifier 
        #  index  index number of the dimension

        # SDim private attributes
        #  _sds    sds instance
        #  _id     dimension identifier
        #  _index  dimension index number
 
        self._sds = sds
        self._id = id
        self._index = index

    def __getattr__(self, name):
        # Get value(s) of SDim attribute 'name'.

        return _getattr(self, name)

    def __setattr__(self, name, value):
        # Set value(s) of SDim attribute 'name'.

        _setattr(self, name, value, ['_sds', '_id', '_index'])


    def info(self):
        """Return info about the dimension instance.
  
        Args :
          no argument
        Returns:
          4-element tuple holding:
            -dimension name; 'fakeDimx' is returned if the dimension
             has not been named yet, where 'x' is the dimension
             index number
            -dimension length; 0 is returned if the dimension is unlimited;
             call the SDim.length() or SDS.info() methods to obtain the
             current dimension length
            -scale data type (one of the SDC.xxx constants); 0 is
             returned if no scale has been set on the dimension
            -number of attributes attached to the dimension
  
        C library equivalent : SDdiminfo
                                                    """
        status, dim_name, dim_size, data_type, n_attrs = \
                _C.SDdiminfo(self._id)
        _checkErr('info', status, 'cannot execute')
        return dim_name, dim_size, data_type, n_attrs

    def length(self):
        """Return the dimension length. This method is usefull
        to quickly retrieve the current length of an unlimited
        dimension.

        Args:
          no argument
        Returns:
          dimension length; if the dimension is unlimited, the
          returned value is the current dimension length

        C library equivalent : no equivalent
                                                   """
        
        return self._sds.info()[2][self._index]

    def setname(self, dim_name):
        """Set the dimension name.
 
        Args:
          dim_name    dimension name
        Returns:
          None
 
        C library equivalent : SDsetdimname
                                                            """

        status = _C.SDsetdimname(self._id, dim_name)
        _checkErr('setname', status, 'cannot execute')


    def getscale(self):
        """Obtain the scale values along a dimension.
 
        Args:
          no argument
        Returns:
          list with the scale values; the list length is equal to the
          dimension length; the element type is equal to the dimension
          data type, as set when the 'setdimscale()' method was called.
 
        C library equivalent : SDgetdimscale
                                                  """

        # Get dimension info. If data_type is 0, no scale have been set
        # on the dimension.
        status, dim_name, dim_size, data_type, n_attrs = _C.SDdiminfo(self._id)
        _checkErr('getscale', status, 'cannot execute')
        if data_type == 0:
            raise HDF4Error, "no scale set on that dimension"

        # dim_size is 0 for an unlimited dimension. The actual length is
        # obtained through SDgetinfo.
        if dim_size == 0:
           dim_size = self._sds.info()[2][self._index]
    
        # Get scale values.
        if data_type in [SDC.UCHAR8, SDC.UINT8]:
            buf = _C.array_byte(dim_size)

        elif data_type == SDC.INT8:
            buf = _C.array_int8(dim_size)
            
        elif data_type == SDC.INT16:
            buf = _C.array_int16(dim_size)

        elif data_type == SDC.UINT16:
            buf = _C.array_uint16(dim_size)

        elif data_type == SDC.INT32:
            buf = _C.array_int32(dim_size)

        elif data_type == SDC.FLOAT32:
            buf = _C.array_float32(dim_size)

        elif data_type == SDC.FLOAT64:
            buf = _C.array_float64(dim_size)

        else:
            raise HDF4Error, "getscale: dimension has an "\
                             "illegal or unsupported type %d" % data_type

        status = _C.SDgetdimscale(self._id, buf)
        _checkErr('getscale', status, 'cannot execute')
        return _array_to_ret(buf, dim_size)

    def setscale(self, data_type, scale):
        """Initialize the scale values along the dimension.
 
        Args:
          data_type    data type code (one of the SDC.xxx constants)
          scale        sequence holding the scale values; the number of
                       values must match the current length of the dataset 
                       along that dimension

        C library equivalent : SDsetdimscale

        Setting a scale on a dimension generates what HDF calls a
        "coordinate variable". This is a rank 1 dataset similar to any
        other dataset, which is created to hold the scale values. The
        dataset name is identical to that of the dimension on which
        setscale() is called, and the data type passed in 'data_type'
        determines the type of the dataset. To distinguish between such
        a dataset and a "normal" dataset, call the iscoordvar() method
        of the dataset instance.
                                                         """

        try:
            n_values = len(scale)
        except:
            n_values = 1

        # Validate args
        dim_size = self._sds.info()[2][self._index]
        if n_values != dim_size:
            raise HDF4Error, 'number of scale values (%d) does not match ' \
                             'dimension size (%d)' % (n_values, dim_size)

        if data_type == SDC.CHAR8:
            buf = _C.array_byte(n_values)
            # Allow a string as the scale argument.
            # Becomes a noop if already a list.
            scale = list(scale) 
            for n in range(n_values):
                scale[n] = ord(scale[n])

        elif data_type in [SDC.UCHAR8, SDC.UINT8]:
            buf = _C.array_byte(n_values)

        elif data_type == SDC.INT8:
            # SWIG refuses negative values here. We found that if we
            # pass them as byte values, it will work.
            buf = _C.array_int8(n_values)
            scale = list(scale)
            for n in range(n_values):
                v = scale[n]
                if v >= 0:
                    v &= 0x7f
                else:
                    v = abs(v) & 0x7f
                    if v:
                        v = 256 - v
                    else:
                        v = 128         # -128 in 2's complement
                scale[n] = v

        elif data_type == SDC.INT16:
            buf = _C.array_int16(n_values)

        elif data_type == SDC.UINT16:
            buf = _C.array_uint16(n_values)

        elif data_type == SDC.INT32:
            buf = _C.array_int32(n_values)

        elif data_type == SDC.FLOAT32:
            buf = _C.array_float32(n_values)

        elif data_type == SDC.FLOAT64:
            buf = _C.array_float64(n_values)

        else:
            raise HDF4Error, "setscale: illegal or usupported data_type"

        if n_values == 1:
            buf[0] = scale
        else:
            for n in range(n_values):
                buf[n] = scale[n]
        status = _C.SDsetdimscale(self._id, n_values, data_type, buf)
        _checkErr('setscale', status, 'cannot execute')

    def getstrs(self):
        """Retrieve the dimension standard string attributes. 
 
        Args:
          no argument
        Returns:
          3-element tuple holding:
            -dimension label  (attribute 'long_name')
            -dimension unit   (attribute 'units')
            -dimension format (attribute 'format')

        An exception is raised if the standard attributes have
        not been set.
 
        C library equivalent: SDgetdimstrs
                                                """

        status, label, unit, format = _C.SDgetdimstrs(self._id, 128)
        _checkErr('getstrs', status, 'cannot execute')
        return label, unit, format

    def setstrs(self, label, unit, format):
        """Set the dimension standard string attributes.
  
        Args:
          label   dimension label  (attribute 'long_name')
          unit    dimension unit   (attribute 'units')
          format  dimension format (attribute 'format')
  
        Returns: 
          None
  
        C library equivalent: SDsetdimstrs
                                                     """

        status = _C.SDsetdimstrs(self._id, label, unit, format)
        _checkErr('setstrs', status, 'cannot execute')

    def attr(self, name_or_index):
        """Create an SDAttr instance representing an SDim
        (dimension) attribute.

        Args:
          name_or_index   attribute name or index number; if a name is
                          given, the attribute may not exist; in that
                          case, the attribute is created when the
                          instance set() method is called

        Returns:
          SDAttr instance for the attribute. Call the methods of this
          class to query, read or set the attribute.

        C library equivalent : no equivalent

                                """

        return SDAttr(self, name_or_index)

    def attributes(self, full=0):
        """Return a dictionnary describing every attribute defined
	on the dimension.

	Args:
          full      true to get complete info about each attribute
                    false to report only each attribute value
	Returns:
          Empty dictionnary if no attribute defined.
	  Otherwise, dictionnary where each key is the name of a
	  dimension attribute. If parameter 'full' is false,
	  key value is the attribute value. If 'full' is true,
	  key value is a tuple with the following elements:
	    - attribute value
	    - attribute index number
	    - attribute type
	    - attribute length

        C library equivalent : no equivalent
	                                            """

        # Get the number of dataset attributes.
	natts = self.info()[3]

	# Inquire each attribute
	res = {}
	for n in range(natts):
            a = self.attr(n)
	    name, aType, nVal = a.info()
	    if full:
	        res[name] = (a.get(), a.index(), aType, nVal)
	    else:
	        res[name] = a.get()

        return res



###########################
# Support functions
###########################

def _getattr(obj, name):
    # Called by the __getattr__ method of the SD, SDS and SDim objects. 
    
    # Python will call __getattr__ to see if the class wants to
    # define certain missing methods (__str__, __len__, etc).
    # Always fail if the name starts with two underscores.
    if name[:2] == '__':
        raise AttributeError
    # See if we deal with an SD attribute.
    a = SDAttr(obj, name)
    try:
        index = a.index()
    except HDF4Error:
        raise AttributeError, "attribute not found"
    # Return attribute value(s).
    return a.get()

def _setattr(obj, name, value, privAttr):
    # Called by the __setattr__ method of the SD, SDS and SDim objects.

    # Be careful with private attributes.
    if name in privAttr:
        obj.__dict__[name] = value
        return

    # Treat everything else as an HDF attribute.
    if type(value) not in [types.ListType, types.TupleType]:
        value = [value]
    typeList = []
    for v in value:
        t = type(v)
        # Prohibit mixing numeric types and strings.
        if t in [types.IntType, types.FloatType] and \
               not types.StringType in typeList:
            if t not in typeList:
                typeList.append(t)
        # Prohibit sequence of strings or a mix of numbers and string.
        elif t == types.StringType and not typeList:
            typeList.append(t)
        else:
            typeList = []
            break
    if types.StringType in typeList:
        xtype = SDC.CHAR8
        value = value[0]
    # double is "stronger" than int
    elif types.FloatType in typeList:
        xtype = SDC.FLOAT64
    elif types.IntType in typeList:
        xtype = SDC.INT32
    else:
        raise HDF4Error, "Illegal attribute value"

    # Assign value
    try:
        a = SDAttr(obj, name)
        a.set(xtype, value)
    except HDF4Error, msg:
        raise HDF4Error, "cannot set attribute: %s" % msg

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

# #################
# Error processing
# #################

class HDF4Error(Exception):

    def __init__(self, args=None):
        self.args = args

def _checkErr(procName, val, msg=""):

    if val < 0:
        # _HEprint();
        # errCode = HEvalue(1)
        #if errCode != 0:
        #    str = "%s (%d): %s" % (procName, errCode, HEstring(errCode))
        #else:
        str = "%s : %s" % (procName, msg)
        raise HDF4Error, str
