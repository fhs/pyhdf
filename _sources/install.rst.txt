============
Installation
============

pyhdf supports installation on Python 2 and Python 3. Please open an
issue here if you encounter any problems during installation:
https://github.com/fhs/pyhdf/issues

The recommended method of installing
pyhdf is to use conda.  See the `Conda user guide
<https://conda.io/projects/conda/en/latest/user-guide/getting-started.html>`_
on how to install conda and activate your conda environment.
Once you're in the conda environment, install `pyhdf from conda-forge
<https://anaconda.org/conda-forge/pyhdf>`_::

    conda install -c conda-forge pyhdf

If you don't want to use conda, the instructions below describes how you
can compile pyhdf from source.


Download the source
-------------------

The source code of the latest release of pyhdf can be obtained from
either of these two location:

*  PyPi / the cheeseshop: https://pypi.python.org/pypi/pyhdf
*  Github: https://github.com/fhs/pyhdf/releases

Requirements
------------

The following packages are required to build and install pyhdf:

- `Python <http://www.python.org>`_:
  Python 2.6 or newer for Python 2, or Python 3.2 or newer for Python 3.
- `NumPy <http://www.numpy.org/>`_
- `HDF4 libraries <https://portal.hdfgroup.org/display/support/Download+HDF4>`_ (to use
  their HDF4 binaries, you will also need szip, available from the same page)
- Compiler suite e.g. `GCC <http://gcc.gnu.org>`_.
  On Windows, you need to use a `compatible Visual C++ compiler
  <https://wiki.python.org/moin/WindowsCompilers>`_.
- `zlib <http://www.zlib.net/>`_
- `libjpeg <http://www.ijg.org/>`_ 

On Debian and Debian-based Linux distributions (e.g. Ubuntu), you can install
all the requirements for Python 3 using this command::

    apt-get install build-essential python3-dev python3-numpy libhdf4-dev -y

Installing from the source archive
----------------------------------

1. Go to the pyhdf source directory.

2. If your HDF4 libraries or include files reside in directories
   that are not searched by default on your system, the installation script
   will complain about missing files.

   Add to the search path by exporting ``INCLUDE_DIRS`` and
   ``LIBRARY_DIRS``, e.g.::

        export INCLUDE_DIRS=/usr/local/hdf-4.2r3/include
        export LIBRARY_DIRS=/usr/local/hdf-4.2r3/lib

   or on Windows something like (replace with actual location)::

        set INCLUDE_DIRS=C:\hdf4\include
        set LIBRARY_DIRS=C:\hdf4\lib;C:\hdf4\dll;C:\hdf4\jpeg6\lib;C:\hdf4\szip21\lib;C:\hdf4\zlib123\lib

   Note that jpeg, zlib, and (optionally) szip libraries must be found
   as well. If they are not in a standard place for the compiler,
   their location must be specified. On Mac OS X, ``/usr/local/lib``
   and ``/usr/local/include`` may need to be specified if the
   libraries were installed there.  You may need to install the devel
   versions of these packages to get the statically-linked libraries
   if your HDF binary is statically linked.
   
   If you are using the binary HDF4 library available from the HDF4 site, you
   must also have szlib installed. Then, you will also need to set ``SZIP``::

        export SZIP=1

	(or on Windows:  set SZIP=1)

   If you do not wish to use szlib, you will need to compile HDF4 from source.

   If anything goes wrong, read the detailed notes below.
   Warning messages about implicit declarations of some functions
   may be produced.  Those are due to SWIG, and may be safely
   ignored.

3. Install system-wide or locally::

        # sudo python setup.py install
        $ python setup.py install --prefix=/usr/local (or prefix of choice)

   Or, you might prefer to make a package (msi, rpm, egg, etc.) and install the 
   package::

        $ python setup.py bdist_<package>

To make sure everything works as expected, run the ``hdfstruct.py``
script (under ``examples/hdfstruct``) on one of your HDF4 files. The
script should display the file structure. This is a handy tool to have
around when you want to explore the contents of any HDF4 file.


Further notes
-------------

External libraries
~~~~~~~~~~~~~~~~~~

HDF4.2 no longer provides its own copies of the jpeg and z libraries.
Those must be installed separately (on Linux, they should be part of
any standard distribution).

The sz library (versions 2.0 or higher) must be installed if the SZIP
compression method is to be used with SDsetcompress(). HDF v4.2 must
also then be compiled with SZIP support.  The binaries available from
NCSA are (at the time of this writing) compiled with SZIP support
(including encoding).  To use these binaries, you *must have SZIP installed*.
The binaries Enthought has produced and which are available in EPD and for 
download from Sourceforge are compiled with SZIP support without encoding
capability.  

Getting an SZIP enabled HDF library may require compiling the library
from source with the "--with-szlib" configuration option.  Note that
you *must* install SZIP in a separate step. For more details, see the
`HDF Group site
<https://portal.hdfgroup.org/display/HDF5/Szip+Compression+in+HDF+Products>`_.

In case your HDF library was compiled with SZIP support and you abide by the
szip licensing terms, set the environment variable ``SZIP`` to ``1``.

If you get error messages related to the ``SDgetcompress()`` /
``SDsetcompress()`` functions, e.g. ``"undefined symbol:
SDgetcompress"``, set the environment variable ``NO_COMPRESS`` to "1".
This will transform ``SDgetcompress()`` and ``SDsetcompress()`` into
no-ops, which will immediately raise an exception, and will not be
resolved against the HDF library symbols. This may make it possible to
work with an HDF library earlier than v4.2.

Swig-generated interface files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Interface files ``hdfext.py`` and ``hdfext_wrap.c`` (located under the
``pyhdf`` subdirectory) have been generated using the SWIG tool.
Those two files should be usable as is on most environments.  It could
happen however that, for reasons related to your environment, your C
compiler does not accept the '.c' file and raises a compilation
error. If so, the interface needs to be regenerated.  To do so,
install `SWIG <http://www.swig.org>`_, then run::

  $ cd pyhdf
  $ swig -python hdfext.i

SWIG should silently regenerate the two interface files, after which
installation should proceed correctly.

TRU64 note
~~~~~~~~~~
The HDF installation creates its libraries as archive (.a) files,
not shareable (.so) ones. On TRU64, the linker by default first looks
for shareable libraries in every directory, then in a second round
for archive files. This means that if there is a libjpeg.so somewhere
on the standard linker search paths, it will be found first, even if
the HDF libjpeg.a file exists in the directory pointed by "library_dirs".
To solve the problem, set the environment variable ``LINK_ARGS``::

  export LINK_ARGS="-oldstyle_liblookup"

This will tell the linker to look for .so then for .a files in each visited
directory.
