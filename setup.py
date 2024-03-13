from __future__ import print_function

import sys
import os
import os.path as path
import shlex
import sysconfig

from setuptools import Extension, setup
import numpy as np


def _find_args(pat, env):
    try:
        val = os.environ[env].split(os.pathsep)
    except KeyError:
        val = []
    try:
        k = sys.argv.index(pat)
        val.extend(sys.argv[k + 1].split(os.pathsep))
        del sys.argv[k]
        del sys.argv[k]
    except ValueError:
        pass
    return val


# A Debian based linux distribution might be using libhdf4 (contains netcdf
# routines) or libhdf4-alt (does not contain netcdf routines). This function
# tries to detect if the alt version should be used.
def _use_hdf4alt(libdirs):
    if not sys.platform.startswith("linux"):
        return False
    libdirs.extend(os.environ.get("LD_LIBRARY_PATH", "").split(os.pathsep))
    libdirs.append("/usr/lib/%s" % sysconfig.get_config_var('MULTIARCH'))
    libdirs.append("/usr/lib")
    libdirs.append("/usr/local/lib")
    libdirs.append("/lib")
    for d in libdirs:
        if os.path.exists(os.path.join(d, "libdfalt.so")) and os.path.exists(
            os.path.join(d, "libmfhdfalt.so")
        ):
            return True
    return False


include_dirs = _find_args("-i", "INCLUDE_DIRS")
library_dirs = _find_args("-l", "LIBRARY_DIRS")
szip_installed = "SZIP" in os.environ
compress = "NO_COMPRESS" not in os.environ
extra_link_args = None
if "LINK_ARGS" in os.environ:
    extra_link_args = shlex.split(os.environ["LINK_ARGS"])


msg = (
    "Cannot proceed without the HDF4 library.  Please "
    "export INCLUDE_DIRS and LIBRARY_DIRS as explained"
    "in the INSTALL file."
)

if sys.platform.startswith("linux"):
    # libhdf4 header files on most linux distributations
    # (e.g. Debian/Ubuntu, CentOS) are stored in /usr/include/hdf
    d = "/usr/include/hdf/"
    if not include_dirs and os.path.exists(d):
        include_dirs.append(d)

for p in include_dirs + library_dirs:
    if not path.exists(p):
        print("\n******\n%s not found\n******\n\n" % p)
        raise RuntimeError(msg)

if sys.platform == "win32":
    libraries = ["mfhdf", "hdf", "xdr"]
elif _use_hdf4alt(library_dirs):
    libraries = ["mfhdfalt", "dfalt"]
else:
    libraries = ["mfhdf", "df"]

if szip_installed:
    extra_compile_args = []
    if sys.platform == "win32":
        libraries += ["szlib"]
    else:
        libraries += ["sz"]
else:
    extra_compile_args = ["-DNOSZIP"]
if sys.platform == "win32":
    libraries += ["libjpeg", "zlib", "ws2_32"]
else:
    libraries += ["jpeg", "z"]

if not compress:
    extra_compile_args += ["-DNOCOMPRESS"]


setup(
    ext_modules=[
        Extension(
            name="pyhdf._hdfext",
            sources=["pyhdf/hdfext_wrap.c"],
            include_dirs=[np.get_include()] + include_dirs,
            extra_compile_args=extra_compile_args,
            library_dirs=library_dirs,
            extra_link_args=extra_link_args,
            libraries=libraries,
        ),
    ],
)
