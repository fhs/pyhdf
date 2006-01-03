# $Id: pycdf.py,v 1.8 2006-01-03 23:14:04 gosselin_a Exp $
# $Name: not supported by cvs2svn $
# $Log: not supported by cvs2svn $
# Revision 1.7  2006/01/02 20:35:59  gosselin_a
# Previous check-out forgot to log the most important information
# about the changes made to pycdf.py. Here they are.
#   -numaray support
#   -Ellipsis notation now allowed inside a slicing expression
#   -The full contents of a Numeric array or a cdf variable can now be assigned
#    to a sliced variable, simply by using its name, without recourse
#    to a "[:]" slicing expression.
#   -A __str__() method was added to CDFVar class, allowing it to be
#    printed saying simply "print v" instead of having to write
#    "print v[:]".
#   -New functions: pycdfVersion() and pycdfArrayPkg().
#   -Stricter validity checks when assigning to an array.
#   -Few bug fixes.
#
# See the CHANGES file for details.
#
# Revision 1.6  2006/01/02 20:25:24  gosselin_a
# Retouched the documentation to produce nicer printouts.
#
# Revision 1.5  2006/01/02 18:51:15  gosselin_a
# The 'pycdf' directory has been restructured so as to allow
# installing pycdf with either the Numeric or numarray array packages.
# The directory top level now holds the package-independent
# python code. 'numeric' and 'numarray' directories hold the
# package-dependent parts.
#
# Revision 1.4  2005/08/16 02:39:05  gosselin_a
# Addition of new features in preparation of release 0.6-0 .
#   -Support of CDF2 file format (64 bit file offsets).
#    Requires netCDF 3.6+.
#
# Revision 1.3  2005/08/15 02:00:30  gosselin_a
# pycdf-0.5-4 bug fix release. See CHANGES file.
#
# Revision 1.2  2005/07/16 16:22:35  gosselin_a
# pycdf classes are now 'new-style' classes (they derive from 'object').
# Added CVS keywords.
#

"""Python interface to the Unidata netCDF library
(see: www.unidata.ucar.edu/packages/netcdf).

Version: 0.6-1
Date:    Jan 3 2006   

  
Table of contents
  Introduction
  Array package : Numeric and numarray
  Package components
  Prerequisites
  Documentation
  Summary of differences between pycdf and C API
  Error handling
  High level attribute access
  High level variable access : extended indexing, slicing and ellipsis
  Primer on reading and querying a netcdf variable
  Reading/setting multivalued netCDF attributes and variables
  Rules governing array assignment
  Working with scalar variables
  Working with the unlimited dimension
  Open issues and current limitations : scipy_core
  Functions summary
  Classes summary
  Examples
   
  
Introduction
------------
pycdf is a python wrapper around the netCDF C API. It augments the API
with an OOP framework where a netcdf file is accessed through 4 different
types of objects:
  CDF      netCDF dataset (file)
  CDFDim   netCDF dimension
  CDFVar   netCDF variable
  CDFAttr  netCDF attribute (dataset or variable attribute)

pycdf key features are as follows.

  -pycdf is a complete implementation of the functionnality offered
   by the netCDF C API. For almost every function offered by the C API 
   exists an equivalent method in one of the pycdf classes. pycdf does not
   hide anything, and everything possible in C implementation is also
   achievable in python. It is quite straightforward to go from C to python
   and vice-versa, and to learn pycdf usage by refering to the C API
   documentation.
   
  -pycdf method names bear a strong resemblance to their C counterparts,
   but are generally much simpler.
   
  -A few high-level python methods have been developped to ease
   programmer's task. Of greatest interest are those allowing netCDF
   access through familiar python idioms:   
     -netCDF attributes can be read/written like ordinary python class
      attributes
     -netCDF variables can be read/written like ordinary python lists using
      multidimensional indices and so-called "extended slice syntax", with
      strides allowed
   See "High level attribute access" and "High level variable access"
   sections for details.

   Other python specific helper methods are:
     -pycdf can transparently put the dataset into define and data mode,
      thus relieving the programmer from having to call redef() and
      enddef(). See CDF.datamode() method for details.
     -pycdf offers methods to retrieve a dictionnary of the attributes,
      dimensions and variables defined on a dataset, and of the attributes
      set on a variable. Querying a dataset is thus geatly simplified.
      See methods CDF.attributes(), CDF.dimensions(), CDF.variables(),
      and CDFVar.attributes() for details.
      
Array package : Numeric and numarray
------------------------------------
netCDF variables are read/written using high-level "array" objects.
Arrays used to be provided solely by the python Numeric package. Beginning
with version 0.6, the python numarray package can now be used. The choice
of the array package on which to base pycdf is made at install time (see
the INSTALL file in the pycdf distribution). Only one style of install is
possible : a Numeric-based and a numarray-based pycdf cannot coexist on the
same machine, unless one wants to play tricks with python search paths.

Although the underlying API is very much identical, the two packages define
the "array" somewhat differently :

  >>> import Numeric, numarray
  >>> type(Numeric.array('i')), type(numarray.array('i'))
  ==> (<type 'array'>, <class 'numarray.numarraycore.NumArray'>)

Since the contents of cdf variables are always returned as "arrays" to the
calling program, the user must be carefull when processing those arrays
using packages directly or indirectly based on Numeric/numarray : a
Numeric-style array may not always be acceptable to a numarray-based
package, and vice-versa.

However, since pycdf simply dispatches "arrays" to the calling program and
does not process them in any special way, it appears that the programmer
can import either 'Numeric' or 'numarray', irrespective of the variant used
to install pycdf. Thus :

  >>> from Numeric import * 

should usually work even if pycdf has been installed using numarray. In the
rest of this documentation, when one reads "from Numeric import ...", it
should be assumed that "from numarray import ..." could also be used,
unless explicitly stated otherwise.

It is however deemed safer to import the same array package as the one
used when installing pycdf. To obtain the name of the package on which the
current pycdf installation is based, call function pycdfArrayPkg().


Package components
------------------
pycdf is a proper Python package, eg a collection of modules stored under
a directory name identical to the package name and holding an __init__.py
file. The pycdf package is composed of 3 modules:
   _pycdfext   C extension module responsible for wrapping the
               netcdf library
   pycdfext    python module implementing some utility functions
               complementing the extension module
   pycdf       python module which wraps the extension module inside
               an OOP framework

_pycdfext and pycdfest were generated with the SWIG preprocessor.
SWIG is however *not* needed to run the package. Those two modules
are meant to do their work in the background, and should never be called
directly. Only 'pycdf' should be imported by the user program.
  
Prerequisites
-------------
  The following software must be installed in order for pycdf to
  work.
  
  netCDF library
    pycdf does *not* include the netCDF library, which must
    be installed separately. netCDF is available at
    "www.unidata.ucar.edu/packages/netcdf".

  Numeric or numarray python package
    netCDF variables are read/written using the array data type provided
    by the Numeric or numarray python package. Numeric or nmarray are
    available at "numpy.sourceforge.net".

Documentation
-------------
pycdf has been written so as to stick as closely as possible to 
the naming conventions and calling sequences documented inside the
"NetCDF Users Guide for C" manual. Even if pycdf gives an OOP twist
to the C API, the C manual can be easily used as a documentary source
for pycdf, once the class to which a method belongs has been
identified, and of course once requirements imposed by the Python
langage have been taken into account. Consequently, this documentation
will not attempt to provide an exhaustive coverage of the netCDF
library. For this, the user is referred to the above mentioned manual.
  
This document (in both its text and html versions) has been completely
produced using "pydoc", the Python documentation generator (which
made its debut in the 2.1 release). pydoc can also be used
as an on-line help tool. For example, to know everything about
the CDFVar class, say:
  
  >>> from pydoc import help
  >>> from pycdf import *
  >>> help(CDFVar)

To be more specific and get help only for the get() method of the
CDFVar class:

  >>> help(CDFVar.get)   # or...
  >>> help(vinst.get)    # if vinst is a CDFVar instance
  

Summary of differences between pycdf and C API
----------------------------------------------
Most of the differences between the pycdf and C API can
be summarized as follows.

  Python method vs C function names:

   -Prefix 'nc_' has been dropped everywhere.
   -Suffixes that became redundant given the class to which the
    method belongs have been dropped. For example,  C function 
    'nc_inq_var()' belongs to python class CDFVar (the class
    encapsulating methods having to do with a netCDF 'variable').
    The '_var' suffix is now redundant, and the method name
    simplifes to 'inq()'.
   -The same reasoning has led to the dropping of redundant
    infixes. For ex., C function 'nc_inq_dimname()' belongs
    to the 'CDFDim' class (the class describing a netCDF
    'dimension'), and has been renamed 'inq_name' since the
    'dim' infix is now redundant.
 
  Internal vs external data types

   -The C API offers the programmer the possibility of automatically 
    converting between netCDF external types (eg: NC.BYTE, NC.SHORT, 
    NC.INT, etc) and a vast array of C "internal" types (unsigned char, 
    char, short, etc). Each basic function responsible for reading/writing
    a value then comes in a variety of different flavors, one per internal
    type (eg: nc_put_var_text(), nc_put_var_uchar(), nc_put_var_schar,
    etc). 
   -pycdf does not offer any such type conversion, mostly because this
    would be either meaningless in the context of the Python language,
    or because type conversion is better left as an explicit task to
    the programmer outside of the netCDF context.
    Values returned by the "get" methods always match the netCDF type
    (NC.BYTE, NC.SHORT and NC.INT are returned as integers, 
    NC.FLOAT and NC.DOUBLE as reals, and NC.CHAR as strings).
    Conversely, values written by the "put" methods are taken verbatim
    from the argument lists and outputted according to the underlying
    netCDF type, using the function variant allowing the maximum value
    range (eg: "long" variant for integers, "double" variant for reals).
    
  Return values
  
   -In the C API, every function returns an integer status code, and values
    computed by the function are returned through one or more pointers
    passed as arguments.
   -In pycdf, error statuses are returned through the Python exception
    mechanism, and values are returned as the method result. When the
    C API specifies that multiple values are returned, pycdf returns a 
    tuple of values, which are ordered similarly as the pointers in the
    C function argument list.
   

Error handling
--------------
All errors are reported by pycdf using the Python exception mechanism.
pycdf normally raises a CDFError exception (a subclass of Exception). 
The message accompanying the error is a 3-element tuple composed
in order of: the name of the function/method which raised the exception,
an integer error code, and a string explaining the meaning of this
error code. A negative error code signals an error raised by the
netCDF C library, and the string is then identical to the one obtained
through the strerror() function call. An error code of 0 indicates
an error signaled by the python layer, not the netCDF C library.
However, some errors related to the inner workings of the pycdf package 
are reported using the standard python exceptions (ValueError, TypeError,
etc) rather than a CDFError exception.

Ex.:
  >>> from pycdf import *
  >>> try:
  ...   d=CDF('toto.nc')
  ... except CDFError,err:
  ...   print "pycdf reported an error in function/method:",err[0]
  ...   print "      netCDF error ",err[1],":",err[2]
  >>>

High level attribute access
---------------------------

netCDF allow setting attributes either at the dataset or the variable
level. Attributes are names storing information (in the form of scalars,
strings, sequences) which help interpret the dataset or variable they
are attached to. netCDF attributes rely on a set of conventions (see the
netCDF manual) and are not enforced in ay way by the library. The only
exception (known to the author) is the '_FillValue' attribute which, when
attached to a variable, sets the value that is to be stored in
uninitialized entries of this variable. All other attributes must be
interpreted at the application level.

With pycdf, attributes can be assigned in two ways.

  -By calling the get()/put() method of an attribute instance. In the
   following example, dataset 'example.nc' is created, and string
   attribute 'title' is attached to the dataset and given value
   'this is an example'.
     >>> from pycdf import *
     >>> d = CDF('example.nc',NC.WRITE|NC.CREATE)  # create dataset
     >>> att = d.attr('title')               # create attr. instance
     >>> att.put(NC.CHAR, 'this is an example') # set attr. type and value
     >>> att.get()                           # get attr. value
     'this is an example'
     >>>

  -By handling the attribute like an ordinary Python class attribute.
   Above example can then be rewritten as follows:
     >>> from pycdf import *
     >>> d = CDF('example.nc',NC.WRITE|NC.CREATE)  # create dataset
     >>> d.title = 'this is an example'      # set attribute type and value
     >>> d.title                             # get attribute value
     'this is an example'
     >>>

  This applies as well to multi-valued attributes.
    >>> att = d.attr('values')               # With an attribute instance
    >>> att.put(NC.INT, (1,2,3,4,5))           
    >>> att.get()
    [1, 2, 3, 4, 5]

    >>> d.values = (1,2,3,4,5)               # As a Python class attribute
    >>> d.values
    [1, 2, 3, 4, 5]

When the attribute is known by its name through a string, standard
functions `setattr()' and `getattr()' can be used to replace the dot
notation. Above example becomes:
    >>> setattr(d, 'values', (1,2,3,4,5))
    >>> getattr(d, 'values')
    [1, 2, 3, 4, 5]

Handling a netCDF attribute like a Python class attribute is admittedly
more natural, and also simpler. Some control is however lost in doing so.
  -Attribute type cannot be specified. pycdf automatically selects one of
   three types according to the value(s) assigned to the attribute:
   NC.CHAR if value is a string, NC.INT if all values are integral,
   NC.DOUBLE if one value is a float. 
  -Consequently, unsigned NC.BYTE values cannot be assigned.
  -Attribute properties (length, type, index number) can only be queried
   through methods of an attribute instance.

High level variable access : extended indexing, slicing and ellipsis
--------------------------------------------------------------------
With pycdf, netCDF variables can be read/written in two ways.

The first way is through the get()/put() methods of a variable instance.
Those methods accept parameters to specify the starting indices, the count
of values to read/write, and the strides along each dimension. For example,
if 'v' is a 4x4 array:
    >>> v.get()                         # complete array
    >>> v.get(start=(0,0),count=(1,4))  # first row
    >>> v.get(start=(0,1),count=(2,2),  # second and third columns of
    ...       stride=(2,1))             # first and third row

The second way is by indexing and slicing the variable like a Python
sequence. pycdf here follows most of the rules used to index and slice
Numeric arrays. Thus a netCDF variable can be seen as a Numeric array,
except that data is read from/written to a file instead of memory.

Extended indexing let you access variable elements with the familiar
[i,j,...] notation, with one index per dimension. For example, if 'm' is a
3x3x3 netCDF variable, one could write:
    >>> m[0,3,5] = m[0,5,3]
    
When indexing is used to select a dimension in a `get' operation, this
dimension is removed from the output array, thus reducing its rank by 1. A
rank 0 array is converted to a scalar. Thus, for a 3x3x3 `m' variable
(rank 3) of type int :
    >>> a = m[0]         # a is a 3x3 array (rank 2)
    >>> a = m[0,0]       # a is a 3 element array (rank 1)
    >>> a = m[0,0,0]     # a is an integer (rank 0 array becomes a scalar)

Had this rule not be followed, m[0,0,0] would have resulted in a single
element array, which could complicate computations.

Extended slice syntax allows slicing netCDF variables along each of its
dimensions, with the specification of optional strides to step through
dimensions at regular intervals. For each dimension, the slice syntax
is: "i:j[:stride]", the stride being optional. As with ordinary slices,
the starting and ending values of a slice can be omitted to refer to the
first and last element, respectively, and the end value can be negative to
indicate that the index is measured relative to the tail instead of the
beginning. Omitted dimensions are assumed to be sliced from beginning to
end. Thus:
    >>> m[0]             # treated as `m[0,:,:]'.

Example above with get()/put() methods can thus be rewritten as follows:
    >>> v[:]             # complete array
    >>> v[:1]            # first row
    >>> v[::2,1:3]       #  second and third columns of first and third row

Indexes and slices can be freely mixed, eg:
    >>> m[:2,3,1:3:2]
     
An ellipis (...) can be used to denote consecutive dimensions in a slicing
expression, avoiding the use of a series of ':' "wild-cards". Only one
ellipsis can appear, either at the start, the end, or the middle of the
slicing expression (more than one ellipsis would make the expression
ambiguous). Thus, if 'v' a 5-dimensional variable :
     v[...,-1]      equivalent to v[:,:,:,:,-1]
     v[0,...,-1]    equivalent to v[0,:,:,:,-1]
     v[2,...]       equivalent to v[2]

An ellipsis can help write cleaner code. Referring to the above
example, it is not clear, when faced with "v[2]", if we deal with a
1-dimensional array or not. The ellipsis used in the equivalent "v[2,...]"
expression makes clear that trailing dimensions are to be accounted for.

Note that, countrary to indexing, a slice never reduces the rank of the
output array, even if its length is 1. For example, given a 3x3x3 `m'
variable:
    >>> a = m[0]         # indexing: a is a 3x3 array (rank 2)
    >>> a = m[0:1]       # slicing: a is a 1x3x3 array (rank 3)
    
As can easily be seen, extended slice syntax is much more elegant and
compact, and offers a few possibilities not easy to achieve with the
get()/put() methods. Negative indices offer a nice example:
    >>> v[-2:]                         # last two rows
    >>> v[-3:-1]                       # second and third row
    >>> v[:,-1]                        # last column

The only features exclusively available with the get()/put) methods are the
specification of a mapping vector (which could be used for ex. to
transpose an array), and the handling of NC.BYTE type values as unsigned.

Primer on reading and querying a netcdf file
--------------------------------------------
Here are useful hints for a quick start on how to read and query a netcdf
file.

Assume the file is named 'table.nc' (as created for example by the
'txttocdf.py' program inside the 'examples/txttocdf' directory accompanying
the pycdf distribution).

To open the file:

  % python
  
  >>> from pycdf import *
  >>> from Numeric import *    # or "from numarray import *"
  >>> nc = CDF('table.nc')     # file opened in readonly mode

To get a dictionnary of attributes defined at the file level :

  >>> ncattr = nc.attributes()  # key is attr name, value is attr value

To get a dictionnary of the variables stored inside the file :
  
  >>> vardict = nc.variables()

The keys are the variable names; the values store the variable properties,
eg: dimension names, shape, and type

To get a list of the variable names:

  >>> varnames = nc.variables().keys()

To retrieve and print the full array of values stored inside variable
'varnames[0]' :

  >>> v0 = nc.var(varnames[0])[:]  # without the [:], you would get a CDF
                                   # var instance;  the slice gets you
                                   # the array of values
  >>> print v0                       

To print the values of the last column of array v0 :

  >>> print v0[:,-1]

To print just the first two rows of values of variable 'varnames[1]' :

  >>> v1_01 = nc.var(varnames[1])[:2]

To get the dictionnary of attributes attached to variable 'varnames[0]' :

  >>> v0_dict = nc.var(varnames[0]).attributes()

Keys are the attribute names, and the dictionnary values store the
attribute values.

See 'examples/cdfstruct/cdfstruct.py' in the pycdf distribution for an
example of a program that exercices many of the pycdf query and read
methods.


Reading/setting multivalued netCDF attributes and variables
-----------------------------------------------------------
Multivalued netCDF attributes are set using a python sequence (tuple or
list). Reading such an attribute returns a python list. The easiest way to
read/set a netCDF attribute is by handling it like a Python class attribute
(see "High level attribute access"). For example:
    >>> d=CDF('test.nc',NC.WRITE|NC.CREATE)  # create dataset
    >>> d.integers = (1,2,3,4)         # define multivalued integer attr
    >>> d.integers                     # get the attribute value
    [1, 2, 3, 4]

The easiest way to set multivalued netCDF variables is to assign to an
indexed subset of the variable, using "[:]" (or [...]) to assign to the
whole variable (see "High level variable access"). The assigned value
can be a python sequence, which can be multi-leveled when assigning to a
multdimensional variable. For example:
    >>> d=CDF('test.nc',NC.WRITE|NC.CREATE)     # create dataset
    >>> d3=d.def_dim('d1',3)                    # create dim. of length 3
    >>> v1=d.def_var('v1',NC.INT,d3)            # 3-elem vector
    >>> v1[:]=[1,2,3]                           # assign 3-elem python list
    >>> v2=d.def_var('d2',NC.INT,(d3,d3))       # create 3x3 variable
           # The list assigned to v2 is composed
           # of 3 lists, each representing a row of v2.
    >>> v2[:]=[[1,2,3],[11,12,13],[21,22,23]]

The assigned value can also be a Numeric/numarray array.
Rewriting example above:
    >>> v1=array([1,2,3])
    >>> v2=array([[1,2,3],[11,12,13],[21,22,23])

Note how we use indexing expressions 'v1[:]' and 'v2[:]' when assigning
using python sequences, and just the variable names when assigning 
arrays.

Reading a netCDF variable always returns an array, except if
indexing is used and produces a rank-0 array, in which case a scalar is
returned.

Rules governing array assignment
--------------------------------
pycdf releases before 0.6 were somewhat careless when dealing with
array assignments. For example, no validity check was performed when
attempting to assign the contents of an array to an array of a different
shape. This could result in garbage being assigned, fatal errors, 
and hard to catch rampant bugs.

Beginning with release 0.6, when an array (or a slice of thereof) is
assigned to, pycdf makes sure that the type of right-hand side is
acceptable, and that the values meet certain validity constraints. An
array can be assigned :
       - a scalar (integer or float)
       - a sequence (list or tuple) of integers or floats, or sequences
         of integers or floats (arbitrarily nested)
       - an array (possibly sliced)

The following paragraphs define the rules obeyed by pycdf.
Any unmet condition will be signaled by a TypeError or ValueError
exception.
       
Assigning a scalar to an array
  When an integer or float scalar value is used on the right-hand side
  (as in "x[4:6,:10:2] = 5), the value is now replicated (broadcasted)
  over the whole left-hand size. Thus:
      >>> x[:2] = 0"    # zeroes the first  two rows of array "x"
      >>> x[:] = 1      # set 'x' to all 1's; equivalent to, but much
                        # simpler than :
                        #   x[:] = Numeric.ones((x.shape()))
                        #   x[:] = NUMARRAY.ones((x.shape()))

  Note in the above example that we do not have to care about the shape of
  the left-hand side array.

Assigning a sequence (tuple or list) to an array
  When a sequence appears on the right-hand size, it must hold only
  integer or float scalars, or nested sequences thereof. The total number
  of scalars in the sequence (ignoring nesting level) must match
  exactly the number of elements expected on the left-hand side. The
  sequence nesting levels are of no consequence, and the values are
  assigned to the array in row-major order. Thus, if "x" is a 3x3 array
  and "seq" is a sequence , then the statement "x[:] = seq" requires 9
  values to be assigned to 'x' and is legal only if "seq" enumerates
  exactly 9 values, eg:
      >>> x[:] = (1,2,3,4,5,6,7,8,9)       # ok, 9 values at same level
      >>> x[:] = ((1,2,3),(4,5,6),(7,8,9)) # ok, 9 values in a 2-level tuple
      >>> x[:] = ((1,2,3)[(4,5,6),(7,8,9)] # ok, 9 values, mix of
                                           # tuple and list
      >>> x[:] = [1,2,3,4]             # wrong, 4 values listed, 5 missing

Assigning the contents of an array to an array
  When an array (possibly sliced) is used as the right-hand size, its shape
  must exactly match that of the array (possibly sliced) used on the left-
   hand side. Thus, if "x" is a 4x4 array and "y" is a 6x4 array :
        >>> x[...] = y      # Fails, shape of x is (4,4) and does not match
                            # that of y which is (6,4)
        >>> x[...] = y[:4]  # Works since array 'y' is sliced to
                            # a (4,4) shape



Working with scalar variables
-----------------------------

A scalar (rank-0) variable is created inside a dataset by calling
dataset method def_var() with an empty (or omitted) dimension sequence, eg:
   >>> cdf = CDF(...)
   >>> cdf.automode()
   >>> temp = df.def_var('temp', NC.FLOAT)    # 'temp' is a scalar variable

Now, methods put() and get() of this variable can be called 
to set and get the variable value, and attributes can be set on the
variable in the usual way, eg:
   >>> temp.put(12)
   >>> temp.units = "celsius"
   >>> print temp.get(), temp.units       # prints "12.0 celsius"
   
For uniformity purposes, the slicing expression "[:]" is also applicable
to scalar variables, even if they are not sequences at all.
Purists may disagree, but otherwise scalar variables could only be accessed
through get() and put() methods, preventing writing generic code to handle
variables using slicing constructs. We can thus write:
   >>> temp[:] = 12                      # equivalent to temp.put(12)
   >>> print temp[:]                     # equivalent to "print temp.get()"


Working with the unlimited dimension
------------------------------------

Inside a dataset, one dimension can be designated as being 'unlimited',
allowing variables based on that dimension to dynamically grow
along that dimension. In physical applications, the unlimited dimension
is frequently used to manage 'time', as for example in a meteorological
model which could output forecasts composed of temperature(time,lat,lon),
pressure(time,lat,lon), etc, data grids.

An unlimited dimension is defined by calling the dataset def_dim() method
using NC.UNLIMITED as the dimension length, eg:
   >>> d1 = cdf.def_dim('d1', NC.UNLIMITED)

A variable can be allowed to grow along that dimension if that dimension
comes first in the variable dimension list, eg:
   >>> d2 = cdf.def_dim('d2', 5)
   >>> v = cdf.def_var('v', NC.DOUBLE, (d1, d2))  # 'd1' must come first

Given an unlimited dimension 'd' and a variable 'v' whose first dimension
is 'd', it is common in netcdf parlance to designate 'v' as a "record
variable", and the data subsets v[0], v[1], etc as "records" inside 'v'.
For ex., if 'd' represents time, and 'v' is a temperature(time,lat,lon)
variable, one can picture v[0] as a "record" holding the grid of
temperatures at time 0, v[1] as the "record" of temperatures at time 1,
etc. Variable 'v' is extended by adding "records" v[0], v[1], etc along
dimension 'd', much as a traditional file is extended by writing data
records to it.

Given a CDFVar instance v, method v.isrecord() can be called to check
whether v is a record variable, eg if first dimension of v refers to the
unlimited dimension.

Only ONE unlimited dimension is allowed inside a dataset, and ALL variables
based on that dimension grow "in synch". So, if variables 'v1' and 'v2'
include an unlimited dimension, adding records to 'v1' will also create new
records in 'v2' as a side effect. Those records will be initialized with
the 'v2' fill value. They will of course need to be properly initialized
afterwards.

When assigning to a variable along an unlimited dimension, the variable
must be properly sliced so as to match the shape of the right-hand side.
The "wild-card" notation ([:], [...]) cannot be used if the shape of the
right-hand side exceeds the current shape of the variable : a shape
mismatch will then be declared and the assignment will be refused. Slicing
the variable beyond its current length will allocate new records and solve
the problem. For example, if 'd' is an unlimited dimension, 'v' has
dimensions (d,5) and 'v' is empty at start: 
   >>> v[:]  = zeros((4,5))    # fails: shape mismatch : (0,5) vs (4,5)
   >>> v[:4] = ones((4,5))     # works: allocate records 0 to 3
                               # and set them to 1's
   >>> v[:]  = zeros((4,5))    # now works: records 0 to 3 exist and are
                               # reset to 0's
   >>> v[:2,:2] = ones((2,2))  # works: resets records 0 and 1 to 1's

An unlimited dimension can be made to grow by assigning to higher and
higher indices along that dimension. Thus:
   >>> for i in range(4,7):
   ...    v[i] = i * ones(5)  # grow dimension unlimited dimension
                              # from 4 to 6

Making an unlimited dimension grow in a non-sequential way will allocate
intermediate records inside the variable, which will be initialized with
the variable fill value (default one, or the one set with attribute
_FillValue). So, if 'v' currently holds 7 records (v[0] to v[6]):
   >>> v._FillValue = 999.0
   >>> v[8] = ones(5)        # will fill v[7] with '999.0' fill values

The same holds true for the other record variables defined in the dataset.
They will all grow in synch when the unlimited dimension length is
extended, and newly created records inside those variables will be set to
their variable fill value.


Open issues and current limitiations : scipy_core
-------------------------------------------------

The following limitations now affect the pycdf package. They may be
lifted out in future releases. Users are encouraged to send their votes
on those issues.

  scipy_core   The Scientific Python project team is currently working on a
               merge of Numeric and numarray called 'scipy_core'.
               Numeric and numarray coud be deprecated once scipy_core
               achieves a stable status (Numeric is said to have reached
               its last release ever). pycdf does not currently support
               scipy_core, but wil certainly do in a not too far feature.


Functions summary
-----------------
pycdf defines the following functions.

   inq_libvers()    query netcdf library version
   strerror()       return the string associated with a netCDF error code

   pycdfVersion()   query pycdf version string
   pycdfArrayPkg()  query the array package used to install pycdf

Classes summary
---------------
pycdf defines the following classes.

  CDF  The CDF class desribes a netCDF dataset. It encapsulates a
       netCDF file descriptor (refered to by 'ncid' in the C manual),
       and all the netCDF top-level functions (those not dealing with
       dimensions, variables or attributes). It contains constructors
       to create instances of all those object types.

       To create a CDF instance call the CDF() constructor.

       methods:
         constructors
	   CDF()       open an existing netCDF file or create a new
	               one, returning a CDF instance
           attr()      get an existing or define a new dataset attribute,
                       returning a CDFAttr (attribute) instance
           dim()       get an existing dimension,
                       returning a CDFDim (dimension) instance
           inq_dimid() equivalent to dim()
           def_dim()   define a new dimension,
                       returning a CDFDim (dimension) instance
           var()       get an existing variable,
                       returning a CDFVar (variable) instance
           inq_varid() equivalent to var()
           def_var()   define a new variable
                       returning a CDFVar (variable) instance

         dataset manipulation
           abort()      backout of recent definitions to the dataset
           close()      close the dataset; this is optional, since a dataset
                        is automatically closed when its instance variable
                        goes out of scope (or is reassigned)
           automode()   activate / deactivate the transparent setting
                        of the dataset define and data mode.
           datamode()   enter data mode, ignoring error if already in
                        this mode
           enddef()     switch the dataset to data mode
           definemode() enter define mode, ignoring error if already
                        in this mode
           redef()      switch the dataset to definition mode
           sync()       synchronize the dataset to disk

         dataset inquiry
	   attributes()    get a dictionnary describing the dataset
	                   global attributes
           dimensions()    get a dictionnary describing the dataset
                           dimensions
           inq()           query number of dimensions, variables, global
                           attributes and id of the unlimited dimension
           inq_natts()     query number of global attributes
           inq_ndims()     query number of dimensions
           inq_nvars()     query number of variables
           inq_unlimdim()  query id of the unlimited dimension
           variables()     get a dictionnary describing the dataset
                           variables
           
         misc
           set_fill()      set fill mode

  CDFAttr  The CDFAttr class describes a netCDF attribute, either
           a variable attribute or a global (dataset) attribute.
           It encapsulates the underlying CDF and CDFVar instances,
           and the attribute name.

           To create a CDFAttr instance, obtain a CDF of CDFVar
           instance, and call its attr() method.

           methods:
             read/write value
               get()      get the attribute value
               put()      set the attribute value

             inquiry
               inq()      get the attribute type and number of values
               inq_id()   get attribute index number
               inq_len    get attribute number of values
               inq_name() get attribute name
               inq_type() get attribute type

             misc
               copy()     copy attribute to another variable or dataset
               delete()   delete attribute
               rename()   rename attribute

  CDFDim   The CDFDim class describes a netCDF dimension. It encapsulates
           the underlying CDF instance and the dimension index number.

           To create a CDFDim instance, obtain a CDF instance
           and call one of its dim(), def_dim() or inq_dimid()
           methods.

           methods:
             inquiry
               inq()      get the dimension name and length
               inq_len()  get the dimension length
               inq_name() get the dimension name

             misc
               rename()   rename dimension

  CDFVar   The CDFVar class describes a netCDF variable. It encapsulates
           the underlying CDF dataset instance, and the variable index
           number.

           To create a CDFVar instance, obtain a CDF dataset
           instance, and call one of its def_var(), var() or
           inq_varid() methods.

           methods:
             constructors
               attr()      get an existing or create a new variable
                           attribute, returning a CDFAttr instance

             get/set variable value
               get()       get the netCDF variable contents, totally or
                           partially; returns a Numeric array
               get_1()     get a single value form the netCDF variable
               put()       write a set of values to the variable;
                           the set can be a Numeric array
               put_1()     put a single value in the variable

             inquiry
       	       attributes()  get a dictionnary holding the names and
	                     values of all the variable attributes
               dimensions()  get the names of the variable dimensions
               inq()         get variable name, type, dimension index
                             numbers and number of attributes
               inq_dimid()   get the dimensions index numbers
               inq_name()    get the variable name
               inq_natts()   get the variable number of attributes
               inq_ndims()   get the variable number of dimensions
               inq_type()    get the variable type
               isrecord()    indicates wheter the variable is a record
                             variable (eg dimension 0 refers to the
                             unlimited dimension)
               shape()       get the lengths of the variable dimensions

             misc
               rename()    rename the variable


  NC       The NC class defines constants for setting file opening modes,
           data Those constants are defined as class attributes.
           Constants are named after their C API counterparts.

           
            data types:
              NC.BYTE
              NC.CHAR
              NC.SHORT
              NC.INT
              NC.FLOAT
              NC.DOUBLE

            file opening modes:
              NC.CREATE   (note: specific to pycdf, absent from the C API)
              NC.TRUNC    (note: specific to pycdf, absent from the C API)
              NC.LOCK
              NC.SHARE
              NC.NOWRITE
              NC.WRITE
              NC.BIT64_OFFSET (corresponds to C NC_64BIT_OFFSET constant)
              
            dataset fill mode:
              NC.FILL
              NC.NOFILL
              
            attribute:
              NC.GLOBAL
              
            dimension:
              NC.UNLIMITED
              
Examples
--------

Example-1

The following simple example exercises some important pycdf methods. It
shows how to create a netCDF dataset, define attributes and dimensions,
create variables, and assign their contents.

Suppose we have a series of text files each defining a 2-dimensional real
matrix. First line holds the matrix dimensions, and following lines hold
matrix values, one row per line. The following procedure will transfer to
a netCDF variable the contents of any one of those text files. The
procedure also computes the matrix min and max values, storing them as
variable attributes. It also assigns to the variable the group of
attributes passed as a dictionnary by the calling program. Note how simple
such an assignment becomes with pycdf: the dictionnary can contain any
number of attributes, of different types, single or multi-valued. Doing
the same in a conventional language would be much more challenging.

Error checking is minimal, to keep example as simple as possible
(admittedly a rather poor excuse ...).


  from Numeric import *
  from pycdf import *

  def txtToCDF(txtFile, ncFile, varName, attr):
    # Transfer contents of 'txtFile' to NC.FLOAT variable 'varName' inside
    # netCDF file 'ncFile'. `attr' is a dictionnary holding attributes
    # to assign to the variable.

    try:   # Catch CDFError exceptions
        # Open netCDF file in update mode, creating it if inexistent.
        nc = CDF(ncFile, NC.WRITE|NC.CREATE)
        # Automatically set define and data modes.
        nc.automode()
        # Open text file and get matrix dimensions on first line
        # (admittedly a flaky design, it would be better to compute those
        # values programmatically).
        txt = open(txtFile)
        ni, nj = map(int, txt.readline().split()) # split fields, then
                                                  # convert to ints
        # Defined netCDF dimensions. Should check for already existing
        # dimensions of that name.
        dimi = nc.def_dim(varName + '_i', ni) # create name like 'depth_i'
        dimj = nc.def_dim(varName + '_j', nj) # and 'depth_j'
        # Define netCDF variable of type NC.FLOAT with those dimensions.
        # Should check that this variable does not already exist.
        var = nc.def_var(varName, NC.FLOAT, (dimi, dimj))
        # Assign attributes passed as argument inside dict `attr'.
        for attrName in attr.keys():
            setattr(var, attrName, attr[attrName])
        # Load variable with lines of data. Compute min and max
        # over the whole matrix.
        i = 0
        while i < ni:
            # split fields, converting them to a list of floats
            elems = map(float, txt.readline().split())
            # assign to netCDF array
            var[i] = elems
            # compute min and max
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
        var.minVal = minVal
        var.maxVal = maxVal
        # Close files (not really necessary, since closing is
        # automatic when file objects go out of scope.
        nc.close()
        txt.close()
    except CDFError, msg:
        print "CDF error:",msg

We could now call the procedure as follows:

  ncFile  = 'table.nc'   # netCDF file name
  # Transfer contents of 'temp.txt' to variable 'temperature'
  txtToCDF('temp.txt', ncFile, 'temperature',
           # Dictionary of attributes to set on netCDF variable
           {'title'      : 'temperature matrix',
            'units'      : 'celsius',
            'precision'  : 0.01,
            'valid_range': (-2.8,27.0)})  # Note multivalued attribute

  # Transfer contents of 'depth.txt' to variable 'depth'
  txtToCDF('depth.txt', ncFile, 'depth',
           # Dictionary of attributes to set on netCDF variable
           {'title'      : 'depth matrix',
            'units'      : 'meters',
            'precision'  : 0.1,
            'valid_range': (0, 500.0)})   # Note multivalued attribute



Example 2

This example shows a usefull python program that will display the
structure of any netCDF file whose name is given on the command line.
After the netCDF file is opened, high level inquiry methods are called
to obtain dictionnaries descrybing dataset attributes, dimensions and
variables. The rest of the program mostly consists in nicely formatting
the contents of those dictionaries.


  import sys
  from pycdf import *
  from Numeric import *

  # Convert numeric type code to string representation
  typeTab = {NC.BYTE:   'BYTE',
             NC.CHAR:   'CHAR',
             NC.SHORT:  'SHORT',
             NC.INT:    'INT',
             NC.FLOAT:  'FLOAT',
             NC.DOUBLE: 'DOUBLE'}

  printf = sys.stdout.write
  ncFile = sys.argv[1]              # get file name from cmd line
  try:
      nc = CDF(ncFile)              # open netCDF file, read-only
      attr = nc.attributes(full=1)  # dataset attributes dictionnary
      dims = nc.dimensions(full=1)  # dataset dimensions dictionnary
      vars = nc.variables()         # dataset variables disctionnary

      # Dataset name, number of attributes, dimensions and variables.
      printf("DATASET INFO\n")
      printf("------------\n\n")
      printf("%-25s%s\n" % ("netCDF file:", ncFile))
      printf("%-25s%d\n" % ("  dataset attributes:", len(attr)))
      printf("%-25s%d\n" % ("  dimensions:", len(dims)))
      printf("%-25s%d\n" % ("  variables:", len(vars)))
      printf("\n");

      # Attribute table.
      if len(attr) > 0:
          printf("Dataset attributes\n\n")
          printf("  name                 idx type   len value\n")
          printf("  -------------------- --- ----   --- -----\n")
          attNames = attr.keys()
          attNames.sort()
          for a in attNames:
              t = attr[a]
              printf("  %-20s %3d %-6s %3d %s\n" %
                     (a, t[1], typeTab[t[2]], t[3], t[0]))
          printf("\n")

      # Dimensions table
      if len(dims) > 0:
          printf("Dataset dimensions\n\n")
          printf("  name                 idx length unlimited\n")
          printf("  -------------------- --- ------ ---------\n")
          dimNames = dims.keys()
          dimNames.sort()
          for d in dimNames:
              t = dims[d]
              printf ("  %-20s %3d %6d %3s\n" %
                      (d, t[1], t[0], t[2] and 'X' or ''))
          printf("\n")

      # Variables table
      if len(vars) > 0:
          printf("Dataset variables\n\n")
          printf("  name                 idx type   nattr dimension(s)\n")
          printf("  -------------------- --- ----   ----- ------------\n")
          varNames = vars.keys()
          varNames.sort()
          for v in varNames:
              vAttr = nc.var(v).attributes()
              t = vars[v]
              printf("  %-20s %3d %-6s %5d " %
                     (v, t[3], typeTab[t[2]], len(vAttr)))
              n = 0
              for d in t[0]:
                  printf("%s%s(%d)" % (n > 0 and ', ' or '', d, t[1][n]))
                  n += 1
              printf("\n")
          printf("\n")

          # Variables attributes
          if len(varNames) > 0:
              printf("VARIABLE INFO\n")
              printf("-------------\n\n")
              for v in varNames:
                  vAttr = nc.var(v).attributes(full=1)
                  if len(vAttr) > 0:
                      printf("%s attributes\n\n" % v)
                      printf("  name                 idx type   len value\n")
                      printf("  -------------------- --- ----   --- -----\n")
                      attNames = vAttr.keys()
                      attNames.sort()
                      for a in attNames:
                          t = vAttr[a]
                          printf("  %-20s %3d %-6s %3d %s\n" %
                                 (a, t[1], typeTab[t[2]], t[3], t[0]))
                      printf("\n")
      
  except CDFError, msg:       # Catch CDFError exceptions
      print "CDFError", msg
         
"""

_VERSION = "0.6-1"

import os, os.path
import sys
import types

# 'pycdf_array' packages declarations dependent on which array package (numarray, Numeric, ...)
# was chosen as the array package.
from pycdfext_array import array, _ARRAYPKG
    
import pycdfext as _C


# List of names we want to be imported by an "from pycdf import *"
# statement

__all__ = ['CDF', 'CDFAttr', 'CDFDim', 'CDFVar',
           'NC',
           'CDFError',
           'pycdfVersion', 'pycdfArrayPkg',
           'inq_libvers', 'strerror']

#############
# Functions.
#############

def pycdfVersion():
    """Query the version of the pycdf package.

    Args:
      no argument
    Returns:
      version string (eg: "0.6-0")

    C library equivalent: n/a
                                  """

    return _VERSION

def pycdfArrayPkg():
    """Query the array package used when installing pycdf.

    Arguments:
      no argument
    Returns:
      string indentifying the array package ("Numeric", "numarray")

    C library equivalent : n/a
                                   """

    return _ARRAYPKG
    

def inq_libvers():     
    """Return the netCDF library version.

    Args:
      no argument
    Returns:
      version string

    C library equivalent : nc_inq_libvers
                                           """

    return _C.nc_inq_libvers()

def strerror(ncerr) :      # static method
    """Return the error string associated with a netCDF error code.
  
    Args:
      ncerr    netCDF error code
    Returns:
      error string
 
    C library equivalent : nc_strerror
                                            """
    return _C.nc_strerror(ncerr)

class NC(object):
    """This class holds constants defining data types and opening modes"""
    
    NOERR        = _C.NOERR
    LOCK         = _C.LOCK
    SHARE        = _C.SHARE
    WRITE        = _C.WRITE
    NOWRITE      = _C.NOWRITE
    BIT64_OFFSET = _C.BIT64_OFFSET
    CREATE       = 0x1000            # specific tp pycdf
    TRUNC        = 0x2000            # specific to pycdf

    FILL         = _C.FILL
    NOFILL       = _C.NOFILL

    BYTE         = _C.BYTE
    CHAR         = _C.CHAR
    SHORT        = _C.SHORT
    INT          = _C.INT
    FLOAT        = _C.FLOAT
    DOUBLE       = _C.DOUBLE
    GLOBAL       = _C.GLOBAL
    UNLIMITED    = _C.UNLIMITED  

class CDF(object):
    """The CDF class describes a netCDF dataset.
    To instantiate a netCDF dataset, call the CDF()
    constructor.                                     """

    def __init__(self, path, mode=NC.NOWRITE):
        """Create a new netCDF dataset or open an existing one.

        NOTE about "classic" and "new" CDF file format
        ----------------------------------------------
        New files will be created in the original netCDF CDF1
        (aka "classic") format, unless the NC.BIT64_OFFSET flag
        is set in the mode argument, in which case the new CDF2
        format will be used. Except for this new creation mode flag,
        the format type used by a file is essentially transparent to
        an application, and has no impact on the rest of the API.
        
        CDF2 allows much bigger file sizes (over 2GB) by using 64 bits
        integer offsets. netCDF library version 3.6 or above must
        be installed in order to use this last feature, otherwise
        the new mode flag will be inoperant. Also note that a CDF2 file
        cannot be read on a platform with an earlier version of the
        netCDF library ( < 3.6) . Users are thus advised to not create
        CDF2 files unless necessary, to improve portability.
 
        Args:
          path    name of the netCDF file to open
          mode    file opening mode; this mode is set of binary flags
	          which can be or'ed together
		      
		      NC.CREATE  combined with NC.WRITE to create file if it
                                 does not exist
                      NC.TRUNC   if NC.WRITE is set, overwrite file if it
                                 already exists
                      NC.NOWRITE open file in  read-only mode; automatically
                                 set if NC.WRITE is not set; file must
                                 exist, otherwise an error is raised
                      NC.WRITE   open file in read-write mode; if file
                                 exists it is updated, unless NC.TRUNC is
                                 set, in which case it is erased and
                                 recreated; if file does not exist, an error
                                 is raised unless NC.CREATE is set, in which
                                 case the file is created
                      NC.SHARE   mimimize buffering to improve file sharing 
		                 with other processes
                      NC.BIT64_OFFSET
                                 Create a CDF2 file format, using 64
                                 bit offsets allowing file sizes over 2GB

                  Note that pycdf offers a richer set of opening modes,
                  close to the ones found inside the C library.
                  netCDF routines support only 2 basic modes
                  (clobber and no clobber).
	
	    Once the file is opened, it is left in define mode if 
            it has been created, and in data mode otherwise.

        Returns:
          a CDF instance
 
        C library equivalent : nc_create / nc_open
	                                             """
	# Private attributes:
	#  _id:       dataset id
        #  _automode: automode flag

        # Make sure _id is initialized in case __del__ is called
        # when the SD object goes out of scope after failing to
        # open file. Failure to do so may put python into an infinite loop
        # (thanks to Richard.Andrews@esands.com and 
        # E.Bernsen@phys.uu.nl for reporting this bug).
        self._id = None
                                                   
        # See if file exists.
        exists = os.path.exists(path)

        if NC.WRITE & mode:
            if exists:
                if NC.TRUNC & mode:
                    try:
                        os.remove(path)
                    except Exception, msg:
                        raise CDFError("CDF", 0, "cannot delete %s : %s" % (path, str(msg)))
                    fct = _C.nc_create
                else:
                    fct = _C.nc_open
            else:
                if NC.CREATE & mode:
                    fct = _C.nc_create
                    mode &= ~NC.CREATE
                else:
                    raise CDFError("CDF", 0, "no such file")
        else:
            if exists:
                fct = _C.nc_open
            else:
                raise CDFError("CDF", 0, "no such file")
                
        status, id = fct(path, mode)
        _checkCDFErr('CDF', status)
        
        self._id = id
        self._automode = 0

    def __del__(self):
        """Close the associated dataset when a CDF instance is deleted,
        if this has not already been done."""

        try:
            if self._id:
                self.close()
        except:
            pass

    def _forceDataMode(self):
        # Private method: force dataset into data mode if `automode' flag
        # is set.

        if self._automode:
            self.datamode()
        
    def _forceDefineMode(self):
        # Private method: force dataset into define mode if `automode' flag
        # is set.

        if self._automode:
            self.definemode()
        
    def __getattr__(self, name):
        # Get value(s) of global attribute 'name'.
        # Dataset mode: does not matter.

	# Python will call __getattr__ to see if the class wants to
	# define certain missing methods (__str__, __len__, etc).
	# Always fail if the name starts with two underscores.
        if name[:2] == '__':
	    raise AttributeError
	# See if we deal with a netCDF attribute.
	a = CDFAttr(self, None, name)
	# Check existence.
	try:
	    type, values = a.inq()
	except CDFError:
            raise AttributeError, "Global attribute not found"
        except Exception, msg:
            raise AttributeError, msg
        
        # Return attribute value(s).
	return a.get()

    def __setattr__(self, name, value):
        # Set value(s) of global attribute 'name'.
	# Dataset mode: define mode.

	# Be careful with private attributes.
	if name in ['_id', '_automode']:
	    self.__dict__[name] = value
	    return

	# Treat everything else as a netCDF global attribute.
        varnum = NC.GLOBAL
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
	    xtype = NC.CHAR
	    value = value[0]
	# double is "stronger" than int
	elif types.FloatType in typeList:
	    xtype = NC.DOUBLE
	elif types.IntType in typeList:
	    xtype = NC.INT
	else:
	    raise ValueError, "Illegal attribute value"

	# Force the dataset in define mode.
        self._forceDefineMode()

        # Assign value
	n = len(value)
	if xtype == NC.CHAR:
            status = _C.nc_put_att_text(self._id, varnum, name, n, value)
        elif xtype in [NC.INT]:
            buf = _C.array_int(n)
            for k in range(n):
                buf[k] = value[k]
            status = _C.nc_put_att_int(self._id, varnum, name, xtype, n,
                                      buf)
        elif xtype in [NC.DOUBLE]:
            buf = _C.array_double(n)
            for k in range(n):
                buf[k] = value[k]
            status = _C.nc_put_att_double(self._id, varnum, name, xtype, n,
                                         buf)
        _checkCDFErr('put', status)

    
    def close(self):
        """Close the dataset. This call is optional, since the dataset is automatically
        closed when its instance variable goes out of scope or is reassigned. 
 
        Args:
          no argument
        Returns:
          None
 
        C library equivalent :  nc_close
                                          """

        _checkCDFErr('close', _C.nc_close(self._id))
        
        # Cancel the id so that self.__del__() does no try to close the dataset
        # again. Attempting to close an already closed file could severely corrupt
        # internal netcdf tables.
        self._id = 0   

    def automode(self, auto=1):
        """Activate / deactivate the transparent setting of the dataset
        define and data mode.

        Args:
          auto     If true (!= 0), the module will transparently set the
                   define or data mode, depending on the call to be made,
                   thus relieving the programmer of the responsability
                   to set the dataset mode with calls to redef()/enddef()
                   methods. If false (== 0), dataset mode must be set
                   explicitly.

        Returns:
          None

        The CDF() constructor always sets the auto flag to false when
        opening the netCDF file.

        C library equivalent : no equivalent
                                                    """

        self._automode = auto
        
    def redef(self):
        """Put netCDF dataset into define mode.
 
        Args:
          no argument
        Returns:
          None
 
        C library equivalent : nc_redef
                                                 """
 
        _checkCDFErr('redef', _C.nc_redef(self._id))

    def definemode(self):
        """Put the dataset in define mode, ignoring possible error if
        already in define mode.

        Args:
          no argument
        Returns:
          None

        C library equivalent : no equivalent
                                                """
        
	try:
	    _checkCDFErr('definemode', _C.nc_redef(self._id))
	except CDFError,err:
	    # error code -39 is raised if dataset already in data mode.
	    if err[1] != -39:
	        raise CDFError, err

    def enddef(self):
        """Leave define mode and enter data mode.
 
        Args:
          no argument
        Returns:
          none
 
        C library equivalent : nc_enddef
                                            """

        _checkCDFErr('enddef', _C.nc_enddef(self._id))

    def datamode(self):
        """Put the dataset in data mode, ignoring possible error if already
        in data mode.
        
        Args: 
          no argument 
        Returns:
          None

        C library equivalent : no equivalent
                                                  """
        
	try:
	    _checkCDFErr('datamode', _C.nc_enddef(self._id))
	except CDFError,err:
	    # error code -38 is raised if dataset already in data mode.
	    if err[1] != -38:
	        raise CDFError, err
        
    def inq(self):
        """Return info about the dataset.
        Dataset mode: does not matter.
 
        Args:
          no argument
        Returns:
          4-element tuple holding:
            -number of dimensions
            -number of variables
            -number of global attributes
            -id of the unlimited dimension, or -1 if none
 
        C library equivalent : nc_inq
                                           """
        status, ndims, nvars, ngatt, unlimdimid = _C.nc_inq(self._id)
        _checkCDFErr('inq', status)
        return ndims, nvars, ngatt, unlimdimid

    def inq_ndims(self):
        """Return the number of dimensions in the dataset.
        Dataset mode: does not matter.
 
        Args:
          no argument
        Returns:
          number of dimensions
 
        C library equivalent : nc_inq_ndims
                                              """

        status, ndims = _C.nc_inq_ndims(self._id)
        _checkCDFErr('inq_ndims', status)
        return ndims

    def inq_nvars(self):
        """Return the number of variables in the dataset.
        Dataset mode: does not matter.
 
        Args:
          no argument
        Returns:
          number of variables
 
        C library equivalent : nc_inq_nvars
                                              """

        status, nvars = _C.nc_inq_nvars(self._id)
        _checkCDFErr('inq_nvars', status)
        return nvars

    def inq_natts(self):
        """Return the number of global attributes in the dataset.
        Dataset mode: does not matter.

        Args:
          no argument
        Returns:
          number of global attributes

        C library equivalent : nc_inq_natts
                                              """

        status, natts = _C.nc_inq_natts(self._id)
        _checkCDFErr('inq_natts', status)
        return natts

    def inq_unlimdim(self):
        """Return the id of the unlimited dimension in the dataset.
        Dataset mode: does not matter.

        Args:
          no argument
        Returns:
          id of the unlimited dimension, or -1 if none

        C library equivalent : nc_inq_unlimdim
                                              """

        status, unlimdim = _C.nc_inq_unlimdim(self._id)
        _checkCDFErr('inq_unlimdim', status)
        return unlimdim

    def attr(self, name_id):
        """Obtain an CDFAttr instance for a global attribute,
        given its name or its index number. The attribute may or may
        not exist.
        Dataset mode: does not matter.
 
        Args:
          name_id   If a string argument is used, it is interpreted as the
                    attribute name, which may be non-existent. 
                    Otherwise, it must be a non negative integer 
                    giving the index number of an existing attribute.
        Returns:
          CDFAttr instance
 
        C library equivalent : None
                                              """

        if type(name_id) == type(''):
            return CDFAttr(self, None, name_id)

        status, name = _C.nc_inq_attname(self._id, NC.GLOBAL, name_id)
        _checkCDFErr('attr', status)
        return CDFAttr(self, None, name)

    def sync(self):
        """Synchronize the dataset to disk.
        Dataset mode: data mode. 
 
        Args:
          no argument
        Returns:
          None
 
        C library equivalent : nc_sync
                                             """
        self._forceDataMode()
        _checkCDFErr('sync', _C.nc_sync(self._id))

    def abort(self):
        """Back out of recent definitions to the dataset. Dataset is closed
        at exit.
        Dataset mode: does not matter.
 
        Args:
          no argument
        Returns:
          None
 
        C library equivalent : nc_abort
                                             """

        _checkCDFErr('abort', _C.nc_abort(self._id))
        # Make sure self.__del__() will not try to close the dataset again.
        self._id = 0

    def set_fill(self, fillmode):
        """Set fill mode for writes to the dataset.
        Dataset mode: does not matter.
 
        Args:
          fillmode   NC.FILL   prefill non-record variables with 
                               fill values (default)
                     NC.NOFILL data not explicitly initialized is left in
                               an undetermined state
        Returns:
          previous fillmode
 
        C library equivalent : nc_set_fill

        The value used as the fill value is the one set using the variable
        '_FillValue' attribute, or a default implementation dependent value. 
                                              """

        status, prevmode = _C.nc_set_fill(self._id, fillmode)
        _checkCDFErr('set_fill', status)
        return prevmode

    def def_dim(self, name, length):   
        """Add a new dimension to the dataset.
        Dataset mode: define mode.
 
        Args:
          name      dimension name
          length    dimension length; use NC.UNLIMITED to create
                    an unlimited dimension (only one such dimension
                    is allowed in a dataset)
        Returns:
          CDFDim class instance
 
        C library equivalent : nc_def_dim
                                           """
        self._forceDefineMode()
        status, id = _C.nc_def_dim(self._id, name, length)
        _checkCDFErr('def_dim', status)
        return CDFDim(self, id)

    def inq_dimid(self, name): 
        """Get a dimension instance given its name.
        Dataset mode: does not matter.
 
        Args:
          name    dimension name 
        Returns:
          CDFDim instance representing the given dimension
 
        C library equivalent : nc_inq_dimid
                                             """
 
        status, id = _C.nc_inq_dimid(self._id, name)
        _checkCDFErr('inq_dimid', status)
        return CDFDim(self, id)

    def dim(self, name_num):
        """ Get a dimension instance given its name or number.
        Dataset mode: does not matter.
 
        Args:
          name_num    Dimension name or number. If a string is used, it
                      is assumed to be the dimension name, and the
                      method behaves as inq_dimid(). Otherwise, the
                      argument must be a non negative number interpreted
                      as the dimension index number. Dimensions are
                      numbered starting at 0.
        Output:
          CDFDim instance representing the given dimension
 
        C library equivalent : none
                                          """
 
        # Validate name.
        if type(name_num) == type(''):
            status, num = _C.nc_inq_dimid(self._id, name_num)
        # Validate the dimension index number.
        else:
            status, name, length = _C.nc_inq_dim(self._id, name_num)
            num = name_num
        _checkCDFErr('dim', status)

        return CDFDim(self, num)

    def def_var(self, name, xtype, dimids=[]):
        """Add a new variable to the dataset.
        Dataset mode: define mode.
 
        Args:
          name        variable name
          xtype       variable type (one of NC.BYTE, NC.CHAR, NC.SHORT,
                      NC.INT, NC.FLOAT, NC.DOUBLE)
          dimids      sequence defining the variable dimensions; can be
                      a mixture of CDFDim instances, dimension index
                      numbers, or dimension names; omit this argument or
                      specify an empty sequence to define a scalar
                      variable; for a one-dimensional variable, the
                      dimension can be specified directly and does not
                      need to be entered as a sequence; for a record variable
                      (eg using an unlimited dimension), the unlimited
                      dimension must come first
        Returns:
          CDFVar instance identifying the variable

        C library equivalent : nc_def_var
                                                       """
        if type(dimids) in [types.ListType, types.TupleType]:
            ndims = len(dimids)
        else:    # Transform scalar into sequence
            ndims = 1
            dimids = [dimids]

        buf = _C.array_int((ndims > 0) and ndims or 1)    # allocate at least 1
        for n in range(ndims):
            d = dimids[n]
            if isinstance(d, CDFDim):
                buf[n] = d._id
            elif type(d) in [types.IntType, types.StringType]:
                buf[n] = self.dim(d)._id
            else:
                raise CDFError('def_var', 0, 'illegal dimension')
        self._forceDefineMode()
        status, id = _C.nc_def_var(self._id, name, xtype, ndims, buf)
        _checkCDFErr('def_var', status)
        return CDFVar(self, id)

    def inq_varid(self, name):
        """Get a variable instance given its name.
        Dataset mode: does not matter.
 
        Args:
          name       variable name
        Returns:
          CDFVar instance identifying the variable
 
        C library equivalent : nc_inq_varid
                                                """

        status, id = _C.nc_inq_varid(self._id, name)
        _checkCDFErr('inq_varid', status)
        return CDFVar(self, id)

    def var(self, name_num):
        """Get a variable instance given its name or index number.
        Dataset mode: does not matter.
 
        Args:
          name_num   Variable name or index number inside the dataset.
                     If a string is used, it is assumed to be the
                     variable name, and the method behaves as the
                     inq_varid() method. Otherwise, argument must be
                     a non negative integer which is interpreted as the
                     variable index number inside the dataset. 
                     Variables are numbered starting at 0
        Returns:
          CDFVar instance identifying the variable
 
        C library equivalent : none
                                          """
 
        # Validate var name.
        if type(name_num) == type(''):
            status, num = _C.nc_inq_varid(self._id, name_num)
        # Validate index number.
        else:
            status, name = _C.nc_inq_varname(self._id, name_num)
            num = name_num
        _checkCDFErr('var', status)

        return CDFVar(self, num)


    def attributes(self, full=0):
        """Return a dictionnary describing every global
	attribute in the dataset.
        Dataset mode: does not matter.

	Args:
          full      true to get complete info about each attribute
                    false to report only each attribute value
	Returns:
          Empty dictionnary if no global attribute defined
	  Otherwise, dictionnary where each key is the name of a
	  global attribute. If parameter `full' is false,
	  key value is the attribute value. If `full' is true,
	  key value is a tuple with the following elements:
	    - attribute value
	    - attribute index number
	    - attribute type
	    - attribute length

        C library equivalent : no equivalent
	                                            """

        # Get the number of global attributes.
	natts = self.inq_natts()

	# Inquire each attribute
	res = {}
	for n in range(natts):
            a = self.attr(n)
	    name = a.inq_name()
	    if full:
	        res[name] = (a.get(), a.inq_id(), a.inq_type(), 
	                             a.inq_len())
	    else:
	        res[name] = a.get()

        return res

    def dimensions(self, full=0):
        """Return a dictionnary holding the names and lengths of every
        dimension defined in the dataset.
        Dataset mode: does not matter.

	Args:
          full      true to get complete info about each dimension
                    false to report only each dimension length
	Returns:
          Empty dictionnary if no dimension defined
	  Otherwise, dictionnary where each key is a dimension name.
	  If parameter `full' is false, key value is the dimension
          length. If `full' is true, key value is a tuple with the
          following elements:
	    - dimension length
	    - dimension index number
	    - 1 if the dimension is unlimited, 0 otherwise

          Note that for the unlimited dimension, the reported length
          is the current length of the dimension.

        C library equivalent : no equivalent
	                                            """

        # Get the number of dimensions.
        nDims = self.inq_ndims()
        # Get the number of the unlimited dimension
        unlim = self.inq_unlimdim()

        # Inquire each dimension
        res = {}
        for n in range(nDims):
            d = self.dim(n)
            name, length = d.inq()
            if full:
                res[name] = (length, n, n == unlim)
            else:
                res[name] = length

        return res

    def variables(self):
        """Return a dictionnary describing all the dataset variables.
        Dataset mode: does not matter.

        Args:
          no argument
        Returns:
          Empty dictionnary if no variable is defined.
          Otherwise, dictionnary whose keys are the dataset variable names,
          and values are tuples describing the corresponding variables.
          Each tuple holds the following elements in order:
            -tuple holding the names of the dimensions defining the
             variable coordinate axes
            -tuple holding the variable shape (dimension lengths);
             if a dimension is unlimited, the reported length corresponds
             to the dimension current length
            -variable type
            -variable index number

        C library equivalent : no equivalent
                                                """
        # Get number of variables
        nVars = self.inq_nvars()

        # Inquire each var
        res = {}
        for n in range(nVars):
            v = self.var(n)
            name = v.inq_name()
            dims = v.inq_dimid()
            dimNames = []
            dimLengths = []
            for dimNum in dims:
                d = self.dim(dimNum)
                dimNames.append(d.inq_name())
                dimLengths.append(d.inq_len())
            res[name] = (tuple(dimNames), tuple(dimLengths),
                         v.inq_type(), n)

        return res
        

class CDFDim(object):
    """The CDFDim class describes a netCDF dimension.
    To instantiate a dimension, obtain a CDF instance,
    and then call one of the following methods of this
    instance: def_dim(), dim() or inq_dimid()."""

    def __init__(self, ncid, id):
        """Instantiate a CDFDim class. This method is for the module
        own internal use. To instantiate a netCDF dimension,
        user program should call the `def_dim()', `inq_dimid()'
        or dim() methods of a CDF instance.
                                                  """

        # Args:
        #   ncid : CDF instance
        #   id   : dimension ID inside the dataset represented by `ncid'

	# Private attributes:
	#   _ncid  : CDF instance
	#   _id    : dimension id

        self._ncid = ncid
        self._id = id

    def inq(self):
        """Obtain the name and length of the dimension instance.
        Dataset mode: does not matter.
   
        Args:
          no argument
        Returns:
          2-element tuple holding:
            -dimension name
            -dimension length; for the unlimited dimension, this
             is the number of records written so far
  
        C library equivalent : nc_inq_dim
                                            """

        status, name, length = _C.nc_inq_dim(self._ncid._id, self._id)
        _checkCDFErr('inq', status)
        return name, length


    def inq_name(self):
        """Obtain the name of the dimension instance.
        Dataset mode: does not matter.
 
        Args:
          no argument
        Returns:
          dimension name (string)
 
        C library equivalent : nc_inq_dimname
                                                   """
 
        status, name = _C.nc_inq_dimname(self._ncid._id, self._id)
        _checkCDFErr('inq_name', status)
        return name

    def inq_len(self):
        """Obtain the length of the dimension instance.
        Dataset mode: does not matter.
 
        Args:
          no argument
        Returns:
          dimension length; for the unlimited dimension, this is
          the number of records written so far
 
        C library equivalent : nc_inq_dimlen
                                                   """
 
        status, length = _C.nc_inq_dimlen(self._ncid._id, self._id)
        _checkCDFErr('inq_len', status)
        return length

    def rename(self, name):
        """Rename the dimension.
        Dataset mode: define mode (except if the new name is shorter than
        the current one).
 
        Args:
          name    new dimension name; it is illegal to use the name of an
                  existing dimension
        Returns
          None
 
        C library equivalent : nc_rename_dim
                                               """
 
        self._ncid._forceDefineMode()
        _checkCDFErr('rename', 
                     _C.nc_rename_dim(self._ncid._id, self._id, name))

class CDFVar(object):
    """The CDFVar class defines a netCDF variable.
    To instantiate a netCDF variable, first obtain a
    CDF instance, then call one of the following methods of 
    this instance: def_var(), inq_var(id) or var() . """

    def __init__(self,ncid, id):
        """This method is for the internal use of the module functions.
        To instantiate this class, a user program should call
        methods `def_var', inq_varid' or `var' of a CDF instance.
                                                   """

        # Args:
        #   ncid     CDF instance
        #   id       variable index number
	
	# Private attributes:
	#    _ncid   : CDF instance
	#    _id     : variable index number

        self._ncid = ncid
        self._id   = id

    def __str__(self):
        """Retrun a string representationof the cdf var."""

        return str(self[...])
      
    def __getattr__(self, name):
        """Get value of variable attribute 'name'.
        Dataset mode: does not matter. """

	# Python will call __getattr__ to see if the class wants to
	# define certain missing methods (__str__, __len__, etc). 
	# Always fail if the name starts with two underscores.
        if name[:2] == '__':
	    raise AttributeError

	# Otherwise, see if this is a netCDF attribute.
	a = CDFAttr(self._ncid, self, name)
	# Check existence.
	try:
	    type, values = a.inq()
	except CDFError:
	    raise AttributeError, "Variable attribute not found"
	# Return attribute value(s).
	return a.get()

    def __setattr__(self, name, value):
        """Set value(s) of variable attribute 'name'.
	Dataset mode: define mode.
	                                 """

	# Be careful with private attributes.
	if name in ['_ncid', '_id']:
	    self.__dict__[name] = value
	    return

	# Treat everything else as a netCDF variable attribute.
        varnum = self._id
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
	    xtype = NC.CHAR
	    value = value[0]
	# double is "stronger" than int
	elif types.FloatType in typeList:
	    xtype = NC.DOUBLE
	elif types.IntType in typeList:
	    xtype = NC.INT
	else:
	    raise ValueError, "Illegal attribute value"
	# Force the dataset in define mode.
        self._ncid._forceDefineMode()

        # Assign value
	n = len(value)
	if xtype == NC.CHAR:
            status = _C.nc_put_att_text(self._ncid._id, varnum, name, n,
                                       value)
        elif xtype in [NC.INT]:
            buf = _C.array_int(n)
            for k in range(n):
                buf[k] = value[k]
            status = _C.nc_put_att_int(self._ncid._id, varnum, name, xtype,
                                      n, buf)
        elif xtype in [NC.DOUBLE]:
            buf = _C.array_double(n)
            for k in range(n):
                buf[k] = value[k]
            status = _C.nc_put_att_double(self._ncid._id, varnum, name,
                                         xtype, n, buf)
        _checkCDFErr('put', status)

    def __len__(self):    # Needed for slices like "-2:" but why ?

        return 0

    def __getitem__(self, elem):

        # This special method is used to index the netCDF variable
        # using the "extended slice syntax". The extended slice syntax
        # is a perfect match for the "start", "count" and "stride"
        # arguments to the nc_get_var() function, and is much more easy
        # to use.
        # Dataset mode: data mode.

        # Compute arguments to 'nc_get_var_0()'.
        start, count, stride = self.__buildStartCountStride(elem)
	# Force the dataset in data mode.
        self._ncid._forceDataMode()
        # Get elements.
        return self.get(start, count, stride)

    def __setitem__(self, elem, data):


        # This special method is used to assign to the netCDF variable
        # using "extended slice syntax". The extended slice syntax
        # is a perfect match for the "start", "count" and "stride"
        # arguments to the nc_put_var() function, and is much more easy
        # to use.
        # Dataset mode: data mode.

        # Compute arguments to 'nc_put_var_0()'.
        # A negative count indicates that the dimension was indexed, not sliced,
        # and will be dropped.
        start, count, stride = self.__buildStartCountStride(elem)
        
        # Shape of the lhs. Negative values inside 'count' indicate dimensions
        # for which scalar indices have been specified. Those dimensions will
        # be dropped from the resulting array, and thus are ignored here.
        lhsShape = tuple([n for n in count if n > 0])
        
	# Force the dataset in data mode.
        self._ncid._forceDataMode()

        # Verify that the assignment makes sense. The type of the rhs must be one of
        # the following:
        #   array
        #   integer or float
        #   sequence of integers or floats, or sequences thereof

        # If the rhs is an array of the type defined by the array package
        # used to compile pycdf, make sure its shape is
        # compatible with the shape defined by the right-hand-side.
        if type(data) == type(array(0)):
            if lhsShape != data.shape:
                raise ValueError, ("incompatible array shapes, lhs=%s vs rhs=%s" %
                                   (lhsShape, data.shape))

        # Maybe rhs is an array, but not of the type for which pycdf was compiled
        # eg a 'numarray' array when pycdf was compiled for 'Numeric' arrays.
        # Take a chance, and see if the the rhs has a 'shape' attribute and supports
        # 'typecode()' and 'itemsize()' methods. If so, assume it is really an array,
        # so as to accomodate users who prefer to us an array package different from
        # the one for which pycdf was initially compiled.
        elif _assumeArray(data):
            if lhsShape != data.shape:
                raise ValueError, ("incompatible array shapes, lhs=%s vs rhs=%s" %
                                   (lhsShape, data.shape))
          
            
        # If rhs is a cdf var, then it is implicitly an array.
        elif type(data) == type(CDFVar(0, 0)):
            if lhsShape != data.shape():
                raise ValueError, ("incompatible array shapes, lhs=%s vs rhs=%s" %
                                   (lhsShape, data.shape()))
            # Create a Numeric array from the netcdf variable.
            data = data[...]

        # If the rhs is a scalar value, convert it to a list that matches the shape of
        # the slice, so as to correctly broadcast the value over the slice elements.
        elif type(data) in [types.IntType, types.FloatType, types.LongType]:
            for i in range(len(count)):
                data = [data]
                if count[i] > 0:
                    data = data * count[i]

        # If the rhs is a sequence, verify it holds only integers, floats or sequences
        # thereof, and count the number of such scalars it holds.
        elif type(data) in [types.ListType, types.TupleType]:
            nRhs = _checkSeq(data)
            # Count the number of values which need to be assigned in the lhs.
            nLhs = 1
            for k in count:
                if k > 0:
                    nLhs *= k
            # The number of scalars in the rhs must match the number of elements assigned
            # in the lhs.
            if nRhs != nLhs:
                print "debug count=",count,"start=",start,"stride=",stride
                raise ValueError, "%d values assigned, %d needed" % (nRhs, nLhs)

        # Bad assignment.
        else:
            raise TypeError, "the cdf var cannot be assigned a value of type %s" \
                  % type(data)
        
        # Assign.
        self.put(data, start, count, stride)

    def __buildStartCountStride(self, elem):

        # Create the 'start', 'count', 'slice' and 'stride' tuples that
        # will be passed to 'nc_get_var_0'/'nc_put_var_0'.
        #   start     starting indices along each dimension
        #   count     count of values along each dimension; a value of -1
        #             indicates that and index, not a slice, was applied to
        #             the dimension; in that case, the dimension should be
        #             dropped from the output array.
        #   stride    strides along each dimension

        # See if we deal with a record variable, by checking if
        # first dimension refers to the unlimited dimension. Set unlim to -1
        # if not, and 0 otherwise.
        if self.isrecord():
            unlim = 0
        else:
            unnlim = -1
        
        # Handle a scalar variable as a 1-dimensional array of length 1.
        shape = self.shape()
        nDims = self.inq_ndims()
        if nDims == 0:
            nDims = 1
            shape = (1,)

        # Make sure the indexing expression does not exceed the variable
        # number of dimensions.
        if type(elem) == types.TupleType:
            if len(elem) > nDims:
                raise ValueError, "slicing expression exceeds the " \
                                  "number of dimensions of the variable"
        else:   # Convert single index to sequence
            elem = [elem]
            
        # 'elem' is a tuple whose element types can be one of:
        #    IntType      for standard indexing
        #    SliceType    for extended slicing (using 'start', 'stop' and 'step' attributes)
        #    EllipsisType for an ellipsis (...); at most one ellipsis can occur in the
        #                 slicing expression, otherwise the expressionis ambiguous
        # Recreate the 'elem' tuple, replacing a possible ellipsis with empty slices.
        hasEllipsis = 0
        newElem = []
        for e in elem:
            if type(e) == types.EllipsisType:
                if hasEllipsis:
                    raise IndexError, "at most one ellipsis allowed in a slicing expression"
                # The ellipsis stands for the missing dimensions.
                newElem.extend((slice(None, None, None),) * (nDims - len(elem) + 1))
            else:
                newElem.append(e)
        elem = newElem

        # Build arguments to "nc_get_var/nc_put_var".
        start = []
        count = []
        stride = []
        n = -1
        for e in elem:
            n += 1
            
            # Simple index
            if type(e) == types.IntType:
                isSlice = 0       # we do not deal with a slice
                # Respect standard python sequence indexing behavior.
                # Count from the dimension end if index is negative.
                # Consider as illegal an out of bound index, except for the
                # unlimited dimension.
                if e < 0 :
                    e += shape[n]
                if e < 0 or (n != unlim and e >= shape[n]):
                    raise IndexError, "index out of range"
                beg = e
                end = e + 1
                inc = 1
                
            # Slice index. Respect Python syntax for slice upper bounds,
            # which are not included in the resulting slice. Also, if the
            # upper bound exceed the dimension size, truncate it.
            elif type(e) == types.SliceType:
                isSlice = 1     # we deal with a slice
                # None or 0 means not specified
                if e.start:
                    beg = e.start
                    if beg < 0:
                        beg += shape[n]
                else:
                    beg = 0
                # None or maxint means not specified
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
            if n != unlim and end > shape[n]:
                end = shape[n]
            if isSlice:       # we deal with a slice
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

    def inq(self):
        """Return information about the variable.
        Dataset mode: does not matter.
 
        Args:
          no argument
        Returns:
          4-element tuple holding:
            -variable name
            -variable type
            -sequence holding the index numbers of the dimensions
             associated with the variable
            -number of attributes associated with the variable
 
        C library equivalent : nc_inq_var
                                                 """

        # Allocate a large enough buffer for the dimension ids
        buf = _C.array_int(32)
     
        status, name, xtype, ndims, natt = \
            _C.nc_inq_var(self._ncid._id, self._id, buf)
        _checkCDFErr('inq', status)
        dimids = []
        for n in range(ndims):
            dimids.append(buf[n])
        return name, xtype, dimids, natt

    def inq_name(self):
        """Get the variable name.
        Dataset mode: does not matter.
 
        Args:
          no argument
        Returns:
          the name of the variable
 
        C library equivalent : nc_inq_varname
                                               """
 
        status, name = _C.nc_inq_varname(self._ncid._id, self._id)
        _checkCDFErr('inq_name', status)
        return name

    def inq_type(self):
        """Get the variable type.
        Dataset mode: does not matter.
 
        Args:
          no argument
        Returns:
          variable type (one of: NC.BYTE, NC.CHAR, NC.SHORT, NC.INT,
                                 NC.FLOAT, NC.DOUBLE)
 
        C library equivalent : nc_inq_vartype
                                                  """

        status, xtype = _C.nc_inq_vartype(self._ncid._id, self._id)
        _checkCDFErr('inq_type', status)
        return xtype

    def inq_ndims(self):
        """Get the number of dimensions associated with the variable.
        Dataset mode: does not matter.
 
        Args:
          no argument
        Returns:
          number of dimensions
 
        C library equivalent : nc_inq_varndims
                                                  """

        status, ndims = _C.nc_inq_varndims(self._ncid._id, self._id)
        _checkCDFErr('inq_ndims', status)
        return ndims

    def inq_dimid(self):
        """Get the index numbers of the dimensions associated
        with the variable.
        Dataset mode: does not matter.   
 
        Args:
          no argument
        Returns:
          sequence of dimension index numbers
 
        C library equivalent : nc_inq_vardimid
                                                  """

        # Get number of dimensions.
        status, ndims = _C.nc_inq_varndims(self._ncid._id, self._id)
        _checkCDFErr('inq_dimid', status)

        buf = _C.array_int(32)
        status = _C.nc_inq_vardimid(self._ncid._id, self._id, buf)
        _checkCDFErr('inq_dimid', status)
        dimids = []
        for n in range(ndims):
          dimids.append(buf[n])
        return dimids
       
    def inq_natts(self):
        """Get the number of attributes associated with the variable
        Dataset mode: does not matter.
 
        Args:
          no argument
        Returns:
          number of attributes associated with the variable
 
        C library equivalent : nc_inq_varnatts
                                                  """

        status, natts = _C.nc_inq_varnatts(self._ncid._id, self._id)
        _checkCDFErr('inq_natts', status)
        return natts

    def isrecord(self):
        """Determines whether the variable is a record variable, eg
        its first dimension refers to the unlimited dimension.

        Args:
          no argument
        Returns:
          1 if the variable is a record variable, 0 if not

        C library equivalent : None

        This method was taken from HDF4 library.
                                                                  """
        
        return self.inq_dimid()[0] == self._ncid.inq_unlimdim()


    def get_1(self, indices, ubyte=0):
        """Retrieve a single value from the netCDF variable.
        Dataset mode: data mode.
 
        Args:
          indices   sequence holding the indices from where to retrieve
                    the value from; a scalar can be used for a rank-1
                    variable
          ubyte     if variable is of type NC.BYTE, this argument serves as
                    a boolean indicating if the byte value should be
                    treated as an unsigned (ubyte != 0) or a signed
                    (ubyte == 0) value
        Returns:
          value at the given indices
 
        C library equivalent : nc_get_var1_<type>
                                                  """

        try:
            ndims = len(indices)
        except:    # Transform scalar into sequence
            ndims = 1
            indices = [indices]
        buf = _C.array_size_t((ndims > 0) and ndims or 1)    # allocate at least 1
        for n in range(ndims):
            buf[n] = indices[n]

        # Check the variable type.
        status, xtype = _C.nc_inq_vartype(self._ncid._id, self._id)
        _checkCDFErr('get_1', status)

        # Force data mode.
        self._ncid._forceDataMode()
        if xtype in [NC.BYTE] and ubyte:
            bytes = _C.array_byte(1)
            status = _C.nc_get_var1_uchar(self._ncid._id, self._id, 
                                       buf, bytes)
            _checkCDFErr('get_1', status)
            return bytes[0]
        if xtype in [NC.CHAR]:
            fct = _C.nc_get_var1_text
        elif xtype in [NC.BYTE, NC.SHORT, NC.INT]:
            fct = _C.nc_get_var1_int
        elif xtype in [NC.FLOAT, NC.DOUBLE]:
            fct = _C.nc_get_var1_double
        else:
            raise CDFError("get_1", 0, "value type not supported")
        status, value = fct(self._ncid._id, self._id, buf)
        _checkCDFErr('get_1', status)
        return value

    def put_1(self, indices, value, ubyte=0):
        """Store a single value in the netCDF variable. 
        Dataset mode: data mode.
 
        Args:
          indices   sequence holding the indices where to store the value;
                    a scalar can be used for a rank-1 variable
          value     value to store
          ubyte     if variable is of type NC.BYTE, this argument serves as
                    a boolean indicating if the byte value should be
                    treated as an unsigned (ubyte != 0) or a signed
                    (ubyte == 0) value

        Returns:
          None
 
        C library equivalent : nc_put_var1_<type> family
                                                          """
        try:
            ndims = len(indices)
        except:    # Transform scalar into sequence
            ndims = 1
            indices = [indices]
        buf = _C.array_size_t((ndims > 0) and ndims or 1)    # allocate at least 1
        for n in range(ndims):
            buf[n] = indices[n]

        # Force data mode.
        self._ncid._forceDataMode()
        # Check the value type.
        xtype = self.inq_type()

        if xtype in [NC.BYTE] and ubyte:
            bytes = _C.array_byte(1)
            bytes[0] = value
            status = _C.nc_put_var1_uchar(self._ncid._id, self._id, buf,
                                         bytes)
            _checkCDFErr('put_1', status)
            return

        if xtype in [NC.CHAR]:
            fct = _C.nc_put_var1_text
        elif xtype in [NC.BYTE, NC.SHORT, NC.INT]:
            fct = _C.nc_put_var1_int
        elif xtype in [NC.FLOAT, NC.DOUBLE]:
            fct = _C.nc_put_var1_double
        else:
            raise CDFError("put_1", 0, "value type not supported")
        _checkCDFErr('put_1', fct(self._ncid._id, self._id, buf, value))


    def get(self, start=None, count=None, stride=None, 
                map=None, ubyte=0):
        """Read data from the netCDF variable.
        Dataset mode: data mode.
 
        Args:
          start   : indices where to start reading in the data array;
                    default to 0 on all dimensions
          count   : number of values to read along each dimension;
                    a value of -1 is treated like 1, except that the
                    corresponding dimension will be dropped from the output
                    array; default to the current length of all dimensions
          stride  : sampling interval along each dimension;
                    default to 1 on all dimensions
          map     : mapping vector (none by default)
          ubyte   : if variable is of type NC.BYTE, this argument serves as
                    a boolean indicating if the byte value should be
                    treated as an unsigned (ubyte != 0) or a signed
                    (ubyte == 0) value
   
          For n-dimensional variables, last 4 parameters are entered 
          using sequences. For rank-0 or -1 variables, integers
          can also be used.
  
          Note that, to read the whole variable contents, one should
          simply call the method with no argument.
   
        Returns: 
          Numeric array initialized with the data.
  
        C library equivalent : nc_get_var_<type>
                               nc_get_vara_<type>
                               nc_get_vars_<type>
                               nc_get_varm_<type>
                                                       """
 
        # Obtain var info.
        sd = self._ncid
        try:
            name, data_type, dimids, nattr = self.inq()
            rank = len(dimids)
            # Temporarily handle a scalar var as a 1-dimensional array of length 1.
            # This faked array will be undone at exit.
            if rank == 0:
                scalar = 1
                rank = 1
                dim_sizes = [1]
            else:
                scalar = 0
                dim_sizes = []
                for n in range(rank):
                    dim_sizes.append(sd.dim(dimids[n]).inq_len())
        except CDFError, msg:
            raise CDFError('get', 0, 'cannot execute')

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
        if map is None:
            map = [0] * rank    # This signals that map was missing
        elif type(map) == type(1):
            map = [map]
        if (len(start) != rank or len(count) != rank or
            len(stride) != rank or len(map) != rank):
            raise CDFError('get', 0, 'start, stride, count or map '
                                     'do not match variable rank')
        for n in range(rank):
            if start[n] < 0 or start[n] + \
                  (abs(count[n]) - 1) * stride[n] >= dim_sizes[n]:
                raise CDFError('get', 0, 'arguments violate '
                                         'the size (%d) of dimension %d'
                                         % (dim_sizes[n], n))
        if not data_type in [NC.CHAR, NC.BYTE, NC.SHORT, NC.INT,
                             NC.FLOAT, NC.DOUBLE]:
            raise CDFError('get', 0, 'cannot currrently deal with '
                                     'this data type')
        # Force data mode.
        sd._forceDataMode()
        
        try:
            res = _C._nc_get_var_0(sd._id, self._id, data_type, start,
                                   count, stride, map, ubyte)
            # Undo the fake array used to handle a scalar var.
            if scalar:
                res = res[0]
            return res
              
        except ValueError, status:
            status = int(str(status))
            _checkCDFErr('get', status)


    def put(self, data, start=None, count=None, stride=None, 
                mapv=None, ubyte=0):
        """Write data to the netCDF variable.
        Dataset mode: data mode.
 
        Args:
          data    : array of data to write; can be given as a Numeric
                    array, or as Python sequence (whose elements can be
                    imbricated sequences); for a scalar variable, directly
                    specify the value
          start   : indices where to start writing in the variable;
                    default to 0 on all dimensions
          count   : number of values to write along each dimension;
                    default to the current length of the variable
                    dimensions
          stride  : sampling interval along each dimension;
                    default to 1 on all dimensions
          mapv    : mapping vector (none by default)
          ubyte   : if variable is of type NC.BYTE, this argument serves as
                    a boolean indicating if the byte value should be
                    treated as an unsigned (ubyte != 0) or a signed
                    (ubyte == 0) value

          For n-dimensional variables, last 4 parameters are entered 
          using sequences. For rank-0 or -1 variables, integers
          can also be used.
   
          Note that, to write the whole variable at once, one has simply
          to call the method with the values in parameter
          `data', omitting all other parameters.
 
        Returns: 
          None.
  
        C library equivalent : nc_put_var_<type>
                               nc_put_vara_<type>
                               nc_put_vars_<type>
                               nc_put_varm_<type>
                                              """

        # Obtain var info.
        sd = self._ncid
        try:
            name, data_type, dimids, nattr = self.inq()
            rank = len(dimids)
            # Handle a scalar variable as a 1-dimensional array of length 1.
            if rank == 0:
                scalar = 1
                rank = 1
                dim_sizes = [1]
            else:
                dim_sizes = []
                for n in range(rank):
                    dim_sizes.append(sd.dim(dimids[n]).inq_len())
        except CDFError, msg:
            raise CDFError('put', 0, 'cannot execute')

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
        if mapv is None:
            mapv = [0] * rank    # This signals that mapv was missing
        elif type(mapv) == type(1):
            mapv = [mapv]
        if (len(start) != rank or len(count) != rank or
            len(stride) != rank or len(mapv) != rank):
            raise CDFError('put', 0, 'start, stride, count or mapv'
                                     'do not match variable rank')
        unlimited = sd.inq_unlimdim() in dimids
        for n in range(rank):
            ok = 1
            if start[n] < 0:
                ok = 0
            elif n > 0 or not unlimited:
                if start[n] + (abs(count[n]) - 1) * stride[n] >= dim_sizes[n]:
                    ok = 0
            if not ok:
                raise CDFError('put', 0,  'arguments violate '
                                          'the size (%d) of dimension %d' 
                                          % (dim_sizes[n], n))
        if not data_type in [NC.CHAR, NC.BYTE, NC.SHORT, NC.INT,
                             NC.FLOAT, NC.DOUBLE]:
            raise CDFError('put', 0, 'cannot currrently deal '
                                     'with this data type')

        # Writing char data is troublesome. Convert characters to their
        # ascii codes. Be carefull because char data can be specified
        # directly with ascii codes.
        if data_type == NC.CHAR:
            try:
                el = data[0]
            except:
                el = data
            if type(el) == type(''):
                data = map(ord, data)

        # Force data mode.
        sd._forceDataMode()

        try:
            _C._nc_put_var_0(sd._id, self._id, data_type, data, 
                            start, count, stride, mapv, ubyte)
        except ValueError, status:
            try:
                status = int(str(status))
                _checkCDFErr('put', status)
            except:
                raise ValueError, status

    def rename(self, name):
        """Rename the ntCDF variable.
        Dataset mode: define mode, unless the new name length is shorter
        or equal to that of the former one.
 
        Args:
          name    new variable name
        Returns:       
          None
 
        C library equivalent : nc_rename_var
                                                  """
        # Force define mode.
        self._ncid._forceDefineMode()
        _checkCDFErr('rename', 
                     _C.nc_rename_var(self._ncid._id, self._id, name))

    def attr(self, name_id):
        """Obtain an CDFAttr instance for a variable attribute,
        given its name or its index number. The attribute may or may
        not exist.
        Dataset mode: does not matter.
 
        Args:
          name_id   If a string argment is used, it is interpreted as the
                    attribute name, which may be non-existent. 
                    Otherwise, it must be a non negative integer 
                    giving the index number of an existing attribute.
        Returns:
          CDFAttr instance
 
        C library equivalent : None
                                              """

        if type(name_id) == type(''):
            return CDFAttr(self._ncid, self, name_id)

        status, name = _C.nc_inq_attname(self._ncid._id, self._id, name_id)
        _checkCDFErr('attr', status)
        return CDFAttr(self._ncid, self, name)


    def attributes(self, full=0):
        """Return a dictionnary describing every attribute
        attached to the variable.
        Dataset mode: does not matter.

	Args:
	    full      true to get complete info about each attribute
	              false to report only each attribute value
	Returns:
	    Empty dictionnary if no variable attribute defined.
	    Otherwise, dictionnary where each key is the name of a
	    variable attribute. If parameter `full' is false,
	    key value is the attribute value. If `full' is true,
	    key value is a tuple with the following elements:
	      - attribute value
	      - attribute index number
	      - attribute type
	      - attribute length

        C library equivalent : no equivalent
	                                            """

        # Get number of variable attributes.
	natts = self.inq_natts()

	# Inquire each attribute
	res = {}
	for n in range(natts):
            a = self.attr(n)
	    name = a.inq_name()
	    if full:
	        res[name] = (a.get(), a.inq_id(), a.inq_type(), 
	                             a.inq_len())
	    else:
	        res[name] = a.get()

        return res

    def dimensions(self):
        """Return the names of the variable dimensions.
        Dataset mode: does not matter.

        Args:
          no argument
        Returns:
          tuple storing the names of the variable dimensions

        C library equivalent : no equivalent
                                                  """

        # Get list of dimensions.
        dims = self.inq_dimid()
        
        # Query dimension names.
        names = []
        for n in dims:
            d = self._ncid.dim(n)
            names.append(d.inq_name())

        return tuple(names)

    def shape(self):
        """Return the variable shape, that is, the length of its
        dimensions.
        Dataset mode: does not matter.

        Args:
          no argument
        Returns:
          tuple storing the variable shape, i.e. the length of the
          variable dimensions

        C library equivalent : no equivalent
                                                  """

        # Get list of dimensions.
        dims = self.inq_dimid()
        
        # Query dimension lengths.
        shape = []
        for n in dims:
            d = self._ncid.dim(n)
            shape.append(d.inq_len())

        return tuple(shape)


class CDFAttr(object):
    """The CDFattr class describes a netCDF attribute,
    either a global (dataset) attribute or a variable attribute.
    To create an instance of this class, first obtain
    a CDFVar instance (for a variable attribute), or
    a CDF instance (for a global attribute).
    Then call the attr() method of this instance.
      
                                                       """
 
    def __init__(self, ncid, varid, name):
        """This constructor is for the internal use of the module.
                                                 """

        # Args:
        #   ncid     CDF instance
        #   varid    CDFVar instance (None for a global attribute)
        #   name     attribute name

	# Private attributes
	#    _ncid  : CDF instance
	#    _varid : CDFVar instance (None for a global attribute)
	#    _name  : attribute name
        self._ncid =    ncid
        self._varid =   varid
        self._name =    name

    def put(self, xtype, value, ubyte=0):
        """Set the attribute value.
        Dataset mode: define mode, except when setting an existing
        attribute to a value occupying less space than the original one.
 
        Args:
          xtype   attribute type (one of: NC.BYTE, NC.CHAR, NC.SHORT,
                  NC.INT, NC.FLOAT, NC.DOUBLE)
          value   attribute value; use a sequence to assign an 
                  array of values to the attribute
          ubyte   if variable is of type NC.BYTE, this argument serves as
                  a boolean indicating if the byte value should be treated
                  as an unsigned (ubyte != 0) or a signed (ubyte == 0)
                  value

        Returns:
          None
 
        C library equivalent : nc_put_att_<type>
                                                  """

        # varid is None for global attributes.
        if self._varid is not None:
            varnum = self._varid._id
        else:
            varnum = NC.GLOBAL
        try:
            n = len(value)
        except:
            n = 1
            value = [value]

        # Force define mode.
        self._ncid._forceDefineMode()
        
        if xtype == NC.CHAR:
	    ncid = self._ncid
            status = _C.nc_put_att_text(self._ncid._id, varnum, self._name,
                                     len(value), value)
        elif xtype in [NC.BYTE] and ubyte:
            buf = _C.array_byte(n)
            for k in range(n):
                buf[k] = value[k]
            status = _C.nc_put_att_uchar(self._ncid._id, varnum, self._name,
                                      xtype, n, buf)
        elif xtype in [NC.BYTE, NC.SHORT, NC.INT]:
            buf = _C.array_int(n)
            for k in range(n):
                buf[k] = value[k]
            status = _C.nc_put_att_int(self._ncid._id, varnum, self._name,
                                    xtype, n, buf)
	# Check if distinguishing between NC.FLOAT and NC.DOUBLE makes a
        # difference. Does not seem so.
        elif xtype in [NC.FLOAT]:
            buf = _C.array_float(n)
            for k in range(n):
                buf[k] = value[k]
            status = _C.nc_put_att_float(self._ncid._id, varnum, self._name,
                                        xtype, n, buf)
        elif xtype in [NC.DOUBLE]:
            buf = _C.array_double(n)
            for k in range(n):
                buf[k] = value[k]
            status = _C.nc_put_att_double(self._ncid._id, varnum,
                                         self._name, xtype, n, buf)
	else:
	    raise CDFError("put", 0, "illegal type")
        _checkCDFErr('put', status)

    def inq(self):
        """Return the type and number of values stored in the attribute.
        Dataset mode: does not matter.
 
        Args:
          no argument
        Returns:
          2-element tuple holding:
            -attribute type
            -number of values
 
        C library equivalent : nc_inq_att
                                                    """

        # varid is None for global attributes.
        if self._varid is not None:
            varnum = self._varid._id
        else:
            varnum = NC.GLOBAL
 
        status, xtype, nval = _C.nc_inq_att(self._ncid._id, varnum,
                                            self._name)
        _checkCDFErr('inq', status)
        return xtype, nval

    def inq_type(self):
        """Get the type of the attribute.
        Dataset mode: does not matter.
 
        Args:
          no argument
        Returns:
          attribute type
 
        C library equivalent : nc_inq_atttype
                                                  """
 
        # varid is None for global attributes.
        if self._varid is not None:
            varnum = self._varid._id
        else:
            varnum = NC.GLOBAL

        status, xtype = _C.nc_inq_atttype(self._ncid._id, varnum,
                                         self._name)
        _checkCDFErr('inq_type', status)
        return xtype
        
    def inq_len(self):
        """Get the number of values stored in the attribute.
        Dataset mode: doe not matter.
 
        Args:
          no argument
        Returns:
          number of values
 
        C library equivalent : nc_inq_attlen
                                                  """
 
        # varid is None for global attributes.
        if self._varid is not None:
            varnum = self._varid._id
        else:
            varnum = NC.GLOBAL

        status, nval = _C.nc_inq_attlen(self._ncid._id, varnum, self._name)
        _checkCDFErr('inq_len', status)
        return nval

    def inq_name(self):
        """Get the attribute name.
        Dataset mode: does not matter.
 
        Args:
          no argument
        Returns:
          attribute name
 
        C library equivalent: nc_inq_attname
                                               """
 
        return self._name

    def inq_id(self):
        """Get the attribute index number.
        Dataset mode: doe not matter.
 
        Args:
          no argument
        Returns:
          attribute index number (starting at 0)
 
        C library equivalent : nc_inq_attid
                                                """
 
        # varid is None for global attributes.
        if self._varid is not None:
            varnum = self._varid._id
        else:
            varnum = NC.GLOBAL

        status, num = _C.nc_inq_attid(self._ncid._id, varnum, self._name)
        _checkCDFErr('inq_id', status)
        return num

    def get(self, ubyte = 0):
        """Return the attribute value(s).
        Dataset mode: does not matter.
 
        Args:
          ubyte     if attribute is of type NC.BYTE, this argument serves as
                    a boolean indicating if the byte value should be
                    treated as an unsigned (ubyte != 0) or a signed
                    (ubyte == 0) value

        Returns:
          attribute values. A string is returned for a char valued
          attribute. Otherwise, a scalar is returned for a single-valued
          attribute, and a tuple otherwise.
 
        C library equivalent : nc_get_att_<type>
                                                       """

        # varid is None for global attributes.
        if self._varid is not None:
            varnum = self._varid._id
        else:
            varnum = NC.GLOBAL
        # Get attribute info
        status, type, nval = _C.nc_inq_att(self._ncid._id, varnum,
                                          self._name)
        _checkCDFErr('get', status)
        # Get value.
        if type == NC.BYTE and ubyte:
            ret = _C.array_byte(nval)
            status = _C.nc_get_att_uchar(self._ncid._id, varnum,
                                        self._name, ret)
        elif type == NC.CHAR:
            status, ret = _C.nc_get_att_text(self._ncid._id, varnum,
                                            self._name)
            if status == 0:
                ret = ret[:nval]
        elif type in [NC.BYTE, NC.SHORT, NC.INT]:
            ret = _C.array_int(nval)
            status = _C.nc_get_att_int(self._ncid._id, varnum,
                                      self._name, ret)
        elif type in [NC.FLOAT, NC.DOUBLE]:
            ret = _C.array_double(nval)
            status = _C.nc_get_att_double(self._ncid._id, varnum,
                                         self._name, ret)
        
        _checkCDFErr('get', status)
        if type == NC.CHAR:
            return ret
        else:
            return _array_to_ret(ret, nval)

    def copy(self, to):
        """Copy the attribute to a variable attribute or a global
        attribute, inside the same dataset or inside a different dataset.
        Dataset mode: define mode.
 
        Args:
          to    Either a CDF instance to copy the attribute as a 
                global attribute of the dataset, or a CDFVar instance,
                to copy the attribute as a variable attribute.
        Returns:
          None
 
        C library equivalent : nc_copy_att
                                                   """
 
        if self._varid is not None:
          vin = self._varid._id
        else:
          vin = NC.GLOBAL
        
        if isinstance(to, CDF):
          ncid_out = to
          vout = NC.GLOBAL
        elif isinstance(to, CDFVar):
          ncid_out = to._ncid
          vout = to._id
        else:
            raise CDFError('copy', 0, 'illegal "to" object')

        # Force define mode.
        self._ncid._forceDefineMode()
        
        _checkCDFErr('copy', _C.nc_copy_att(self._ncid._id, vin, self._name,
                                             ncid_out._id, vout))
      
    def rename(self, newname):
        """Rename the attribute.
        Dataset mode: define mode, unless the new name is shorter than than
        the current one.
 
        Args:
          newname   new attribute name
        Returns
          None
 
        C library equivalent : nc_rename_att
                                                """

        if self._varid is not None:
            varnum = self._varid._id
        else:
            varnum = NC.GLOBAL

        # Force define mode.
        self._ncid._forceDefineMode()
        
        _checkCDFErr('rename', _C.nc_rename_att(self._ncid._id, varnum, 
                                                 self._name, newname))
        self._name = newname

    def delete(self):
        """Delete attribute.
        Dataset mode: define mode.

        Args:
          no argument
        Returns:
          None

        C library equivalent : nc_del_att
                                               """
        if self._varid is not None:
            varnum = self._varid._id
        else:
            varnum = NC.GLOBAL

        # Force define mode.
        self._ncid._forceDefineMode()
        
        _checkCDFErr('del', _C.nc_del_att(self._ncid._id, varnum,
                                         self._name))
        # Invalidate contents of the attribute instance
        self._ncid = None
        self._varid = None
        self._name = None

###########################
# Support functions
###########################

def _array_to_ret(buf, nValues):
    """ Convert array 'buf' to a scalar or a list. """

    if nValues == 1:
        ret = buf[0]
    else:
        ret = []
        for i in xrange(nValues):
            ret.append(buf[i])
    return ret

def _array_to_str(buf, nValues):
    """ Convert array of bytes 'buf' to a string . """

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

def _checkSeq(seq):
  """Validate a sequence used in an assignment, returning its length,
  including that of its sub-sequences.

      Args:
        seq   Sequence (list of tuple) to validate. The sequence must be composed solely
              of integers, floats, or sequences thereof. Otherwise a TypeError exception
              is raised.

      Returns:
        Total number of elements inside 'seq' and its sub-sequences.
                                                                        """

  n = 0
  for el in seq:
      t = type(el)
      if t in [types.IntType, types.FloatType, types.LongType]:
          n += 1
      elif t in [types.ListType, types.TupleType]:
          n += _checkSeq(el)    # Recursive call
      else:
          raise ValueError, "Sequence must hold only integers or floats"

  return n

def _assumeArray(data):
    """See if we can assume that 'data' is an array.
       If 'data' has a 'shape' attribute defined as a sequence,
       and 'typecode()' and 'itemsize()' methods, we assume 'data' is an array and
       return True. Otherwise False is returned.
                                                             """

    try:
        if type(data.shape) not in [types.ListType, types.TupleType]:
            return 0
        dum = data.typecode()
        dum = data.itemsize()
        return 1

    except Exception,msg:
        return 0
        

# #################
# Error processing
# #################

class CDFError(Exception):

    def __init__(self, procName, errCode, errMsg):
        self.args = (procName, errCode, errMsg)
	self.procName = procName
	self.errCode = errCode
	self.errMsg = errMsg

def _checkCDFErr(procName, errCode, msg=""):

    if errCode != NC.NOERR:
	raise CDFError(procName, errCode, msg or strerror(errCode))

#################
# Test code     #
#################

if __name__ == '__main__':

    from Numeric import *
    try:
        # Create a test dataset. Raise the automode flag, so that
        # we do not need to worry about setting the define/data mode.
        d = CDF('test.nc', NC.WRITE|NC.CREATE|NC.TRUNC)
        d.automode()
        # Create 2 global attributes, one holding a string,
        # and the other one 2 floats.
        d.title = 'This is a test dataset'
        d.cal_coeff = (-0.5, 2.8)
        # We want to create a "record" variable to store a matrix
        # with 5 columns and a variable number of rows.
        # We thus create 2 netCDF dimensions:
        #   -one named `bin_number' of length 5 (NCOLS) for the number
        #    of columns;
        #   -one named `rec_num' of unlimited length (NROWS) for the number
        #    of rows.
        NROWS = NC.UNLIMITED
        NCOLS = 5
        rec_num    = d.def_dim('rec_num',    NROWS)
        bin_number = d.def_dim('bin_number', NCOLS)
        # Create a netCDF record variable named `obs_table', of type
        # integer. Note that the unlimited dimension must come first
        # (must be the slowest varying index).
        obs_table = d.def_var('obs_table', NC.INT, (rec_num, bin_number))
        # Specify valid data range by setting a variable attribute.
        obs_table.valid_range = (-40, 200)
        # Switch to data mode.
        # Initialize variable with a few records
        recs = ((1,3,-4,5,10),
                (0,10,8,7,4),
                (-1,4,5,9,13))
        obs_table[0:len(recs)] = recs
        print "step 1, obs_table"
        print obs_table[:]
        print "should be"
        print array(recs)
        # Change value at row 1 and col 3
        #obs_table.put_1((1,3),45)
        v = 45
        obs_table[1,3] = v      
        print "step 2, obs_table with element [1,3] modified"
        print obs_table[:]
        print "element [1,3] should be"
        print v
        # Get the current number of records in the table,
        # and append 2 new records to the table.
        nrecs = rec_num.inq_len()
        newrecs = ((12,-45,13, 0, 8),
                   (0,56,-10,16,13))
        #obs_table.put(newrecs,               # data
        #         (nrecs,0),             # start
        #         (len(newrecs),NCOLS))  # count
        obs_table[nrecs:nrecs+len(newrecs)] = newrecs
        print "step 3, obs_table with 2 rows appended"
        print obs_table[:]
        print "last 2 rows should be"
        print array(newrecs)

        # Get values of column 2. col_2 is a Numeric array.
        nrecs = rec_num.inq_len()
        col_2 = obs_table[:,2]
        print "step 4, col 2 of obs_table"
        print col_2
        print "column 2 values should be"
        print [-4, 8, 5, 13, -10]
        
        # Bump column values by 5 and write column back to the netCDF
        # variable. We take advantage of Numeric capacity to operate
        # directly on arrays.
        #obs_table.put(col_2+5, start=(0,2), count=(nrecs,1))
        obs_table[:,2] = col_2+5
        print "step 5, column 2 values incremented by 5"
        print obs_table[:]
        print "column 2 values should be"
        print [-4, 8, 5, 13, -10]
        
        # Create a second variable named `obs_table_copy', this time of
        # type double, and initialize it with the first 3 records of
        # variable `obs_table'.
        # Create 2nd variable and copy to it attribute `valid_range' of
        # first variable.
        obs_table_copy = d.def_var('obs_table_copy', NC.DOUBLE,
                                   (rec_num, bin_number))
        obs_table.attr('valid_range').copy(obs_table_copy)
        # Since obs_table_copy was defined using the same dimensions as 
        # obs_table (rec_num, bin_number) and the length of rec_num is
        # currently > 3, obs_table_copy will have uninitialized rows at
        # its end (since we transfer only first 3 records from obs_table).
        # Those rows will be filled with the default fill value. This
        # default does not suit us, so we redefine it to a more convenient
        # one.
        obs_table_copy._FillValue = -9999.0
        # Transfer first 3 records from obs_table to obs_table_copy, first
        # dividing values by 10.
        obs_table_copy[:3] = obs_table[:3]/10.0
        print "step 6, obs_table_copy"
        print array2string(obs_table_copy[:], precision=3,
                           suppress_small=1)
        print "First 3 rows should be equal to those of 'obs_table'"
        print "divided by 10. Last 2 rows should be set to ",\
              obs_table_copy._FillValue
        
        d.close()                     # Close dataset
    except CDFError, msg:
        print "CDF error occured: ",msg
