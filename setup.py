# Allows bdist_egg to work if you have setuptools installed.
# This import must be before the numpy.distutils import of setup.
#  Otherwise, no harm.
try:
    import setuptools
except:
    pass

from numpy.distutils.core import setup, Extension

import sys
import os
import os.path as path
def _find_args(pat, env):
    val = os.environ.get(env, [])
    if val:
        val = val.split(os.pathsep)
    try:
        k = sys.argv.index(pat)
        val.extend(sys.argv[k+1].split(os.pathsep))
        del sys.argv[k]
        del sys.argv[k]
    except ValueError:
        pass
    return val    

include_dirs = _find_args('-i', 'INCLUDE_DIRS')
library_dirs = _find_args('-l', 'LIBRARY_DIRS')
szip_installed = not os.environ.has_key('NOSZIP')
compress = not os.environ.has_key('NO_COMPRESS')
extra_link_args = os.environ.get('LINK_ARGS', '')


msg = 'Cannot proceed without the HDF4 library.  Please ' \
      'export INCLUDE_DIRS and LIBRARY_DIRS as explained' \
      'in the INSTALL file.'

if sys.platform == 'win32':
    try:
        k = sys.argv.index('--hdf4')
        baseloc = sys.argv[k+1]
        del sys.argv[k]
        del sys.argv[k]
    except (ValueError, IndexError):
        baseloc = None
    if not baseloc:
        baseloc = os.environ.get('HDF4', None)
    if baseloc:
        # fix include_dirs and library_dirs
        #  based on fixed set of paths
        if not path.exists(baseloc):
            print "\n******\n%s not found\n******\n\n" % baseloc
            raise RuntimeError(msg)
        if not path.isdir(baseloc):
            print "\n******\n%s not a directory \n******\n\n" % baseloc
            raise RuntimeError(msg)
        alldirs = os.listdir(baseloc)
        include_dirs = []
        library_dirs = []
        for adir in alldirs:
            if not path.isdir(path.sep.join([baseloc, adir])):
                continue
            if adir.startswith('42'):
                include_dirs.append(path.sep.join([baseloc, adir, 'include']))
                library_dirs.append(path.sep.join([baseloc, adir, 'dll']))
            library_dirs.append(path.sep.join([baseloc, adir, 'lib']))
        print "Using include_dirs = ", include_dirs
        print "Using library_dirs = ", library_dirs
        
for p in include_dirs + library_dirs:
    if not path.exists(p):
        print "\n******\n%s not found\n******\n\n" % p
        raise RuntimeError(msg)

if sys.platform == 'win32':
    # Find DLL path
    dll_path = ''
    for p in library_dirs:
        if path.exists(p + os.path.sep + "HM423M.DLL"):
            dll_path = p + os.path.sep
            break
    if dll_path == '':
        raise RuntimeError("Cannot find required HDF4 DLLs -- check LIBRARY_DIRS")

if sys.platform == 'win32':
    libraries = ["hm423m", "hd423m", "xdr_for_dll" ]
else:
    libraries = ["mfhdf", "df"]

if szip_installed:
    extra_compile_args = []
    if sys.platform == 'win32':
        libraries += ["szlib"]
    else:
        libraries += ["sz"]
else:
    extra_compile_args = ["-DNOSZIP"]
if sys.platform == 'win32':
    libraries += ["libjpeg", "zlib", "ws2_32"]
else:
    libraries += ["jpeg", "z"]

if not compress:
    extra_compile_args += ["-DNOCOMPRESS"]

_hdfext = Extension('pyhdf._hdfext',
                    sources      = ["pyhdf/hdfext_wrap.c"],
                    include_dirs = include_dirs,
                    extra_compile_args = extra_compile_args,
                    library_dirs = library_dirs,
                    extra_link_args=[extra_link_args],
                    libraries = libraries,
                    )

if sys.platform == 'win32':
    data_files = [("pyhdf", [dll_path + x for x in ["HM423M.DLL", "HD423M.DLL"]])]
else:
    data_files = []

setup(name         = 'pyhdf',
      author       = 'Andre Gosselin',
      author_email = 'Andre.Gosselin@dfo-mpo.gc.ca',
      description  = 'Python interface to the NCSA HDF4 library',
      keywords     = ['hdf', 'netcdf', 'numpy', 'python', 'pyhdf'],
      license      = 'public',
      long_description = 'The pyhdf package wraps the functionality\n '
                         'of the NCSA HDF version 4 library inside a Python OOP\n '
                         'framework. The SD (scientific dataset), VS\n '
                         '(Vdata) and V (Vgroup) APIs are currently implemented.\n '
                         'SD datasets are read/written\n '
                         'through numpy arrays. netCDF files can also\n '
                         'be read and modified with pyhdf.',
      url          = 'http://www.sourceforge.net/projects/pysclint',
      version      = '0.8.3',
      packages     = ['pyhdf'],
      ext_modules  = [_hdfext],
      data_files   = data_files
      )
