# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.
import _sdext
def _swig_setattr(self,class_type,name,value):
    if (name == "this"):
        if isinstance(value, class_type):
            self.__dict__[name] = value.this
            if hasattr(value,"thisown"): self.__dict__["thisown"] = value.thisown
            del value.thisown
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    self.__dict__[name] = value

def _swig_getattr(self,class_type,name):
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


DFNT_NONE = _sdext.DFNT_NONE
DFNT_QUERY = _sdext.DFNT_QUERY
DFNT_VERSION = _sdext.DFNT_VERSION
DFNT_FLOAT32 = _sdext.DFNT_FLOAT32
DFNT_FLOAT = _sdext.DFNT_FLOAT
DFNT_FLOAT64 = _sdext.DFNT_FLOAT64
DFNT_DOUBLE = _sdext.DFNT_DOUBLE
DFNT_FLOAT128 = _sdext.DFNT_FLOAT128
DFNT_INT8 = _sdext.DFNT_INT8
DFNT_UINT8 = _sdext.DFNT_UINT8
DFNT_INT16 = _sdext.DFNT_INT16
DFNT_UINT16 = _sdext.DFNT_UINT16
DFNT_INT32 = _sdext.DFNT_INT32
DFNT_UINT32 = _sdext.DFNT_UINT32
DFNT_INT64 = _sdext.DFNT_INT64
DFNT_UINT64 = _sdext.DFNT_UINT64
DFNT_INT128 = _sdext.DFNT_INT128
DFNT_UINT128 = _sdext.DFNT_UINT128
DFNT_UCHAR8 = _sdext.DFNT_UCHAR8
DFNT_UCHAR = _sdext.DFNT_UCHAR
DFNT_CHAR8 = _sdext.DFNT_CHAR8
DFNT_CHAR = _sdext.DFNT_CHAR
DFNT_CHAR16 = _sdext.DFNT_CHAR16
DFNT_UCHAR16 = _sdext.DFNT_UCHAR16
SD_UNLIMITED = _sdext.SD_UNLIMITED
SD_FILL = _sdext.SD_FILL
SD_NOFILL = _sdext.SD_NOFILL
DFACC_READ = _sdext.DFACC_READ
DFACC_WRITE = _sdext.DFACC_WRITE
DFACC_CREATE = _sdext.DFACC_CREATE
DFACC_ALL = _sdext.DFACC_ALL
DFACC_RDONLY = _sdext.DFACC_RDONLY
DFACC_RDWR = _sdext.DFACC_RDWR
DFACC_CLOBBER = _sdext.DFACC_CLOBBER
DFACC_BUFFER = _sdext.DFACC_BUFFER
DFACC_APPENDABLE = _sdext.DFACC_APPENDABLE
DFACC_CURRENT = _sdext.DFACC_CURRENT
DFACC_OLD = _sdext.DFACC_OLD
COMP_CODE_NONE = _sdext.COMP_CODE_NONE
COMP_CODE_RLE = _sdext.COMP_CODE_RLE
COMP_CODE_NBIT = _sdext.COMP_CODE_NBIT
COMP_CODE_SKPHUFF = _sdext.COMP_CODE_SKPHUFF
COMP_CODE_DEFLATE = _sdext.COMP_CODE_DEFLATE
class array_byte(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_byte, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_byte, name)
    def __init__(self,*args):
        _swig_setattr(self, array_byte, 'this', apply(_sdext.new_array_byte,args))
        _swig_setattr(self, array_byte, 'thisown', 1)
    def __del__(self, destroy= _sdext.delete_array_byte):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_sdext.array_byte___getitem__,args)
    def __setitem__(*args): return apply(_sdext.array_byte___setitem__,args)
    def cast(*args): return apply(_sdext.array_byte_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _sdext.array_byte_frompointer
    if _newclass:frompointer = staticmethod(_sdext.array_byte_frompointer)
    def __repr__(self):
        return "<C array_byte instance at %s>" % (self.this,)

class array_bytePtr(array_byte):
    def __init__(self,this):
        _swig_setattr(self, array_byte, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_byte, 'thisown', 0)
        _swig_setattr(self, array_byte,self.__class__,array_byte)
_sdext.array_byte_swigregister(array_bytePtr)
array_byte_frompointer = _sdext.array_byte_frompointer


class array_int8(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_int8, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_int8, name)
    def __init__(self,*args):
        _swig_setattr(self, array_int8, 'this', apply(_sdext.new_array_int8,args))
        _swig_setattr(self, array_int8, 'thisown', 1)
    def __del__(self, destroy= _sdext.delete_array_int8):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_sdext.array_int8___getitem__,args)
    def __setitem__(*args): return apply(_sdext.array_int8___setitem__,args)
    def cast(*args): return apply(_sdext.array_int8_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _sdext.array_int8_frompointer
    if _newclass:frompointer = staticmethod(_sdext.array_int8_frompointer)
    def __repr__(self):
        return "<C array_int8 instance at %s>" % (self.this,)

class array_int8Ptr(array_int8):
    def __init__(self,this):
        _swig_setattr(self, array_int8, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_int8, 'thisown', 0)
        _swig_setattr(self, array_int8,self.__class__,array_int8)
_sdext.array_int8_swigregister(array_int8Ptr)
array_int8_frompointer = _sdext.array_int8_frompointer


class array_int16(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_int16, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_int16, name)
    def __init__(self,*args):
        _swig_setattr(self, array_int16, 'this', apply(_sdext.new_array_int16,args))
        _swig_setattr(self, array_int16, 'thisown', 1)
    def __del__(self, destroy= _sdext.delete_array_int16):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_sdext.array_int16___getitem__,args)
    def __setitem__(*args): return apply(_sdext.array_int16___setitem__,args)
    def cast(*args): return apply(_sdext.array_int16_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _sdext.array_int16_frompointer
    if _newclass:frompointer = staticmethod(_sdext.array_int16_frompointer)
    def __repr__(self):
        return "<C array_int16 instance at %s>" % (self.this,)

class array_int16Ptr(array_int16):
    def __init__(self,this):
        _swig_setattr(self, array_int16, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_int16, 'thisown', 0)
        _swig_setattr(self, array_int16,self.__class__,array_int16)
_sdext.array_int16_swigregister(array_int16Ptr)
array_int16_frompointer = _sdext.array_int16_frompointer


class array_uint16(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_uint16, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_uint16, name)
    def __init__(self,*args):
        _swig_setattr(self, array_uint16, 'this', apply(_sdext.new_array_uint16,args))
        _swig_setattr(self, array_uint16, 'thisown', 1)
    def __del__(self, destroy= _sdext.delete_array_uint16):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_sdext.array_uint16___getitem__,args)
    def __setitem__(*args): return apply(_sdext.array_uint16___setitem__,args)
    def cast(*args): return apply(_sdext.array_uint16_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _sdext.array_uint16_frompointer
    if _newclass:frompointer = staticmethod(_sdext.array_uint16_frompointer)
    def __repr__(self):
        return "<C array_uint16 instance at %s>" % (self.this,)

class array_uint16Ptr(array_uint16):
    def __init__(self,this):
        _swig_setattr(self, array_uint16, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_uint16, 'thisown', 0)
        _swig_setattr(self, array_uint16,self.__class__,array_uint16)
_sdext.array_uint16_swigregister(array_uint16Ptr)
array_uint16_frompointer = _sdext.array_uint16_frompointer


class array_int32(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_int32, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_int32, name)
    def __init__(self,*args):
        _swig_setattr(self, array_int32, 'this', apply(_sdext.new_array_int32,args))
        _swig_setattr(self, array_int32, 'thisown', 1)
    def __del__(self, destroy= _sdext.delete_array_int32):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_sdext.array_int32___getitem__,args)
    def __setitem__(*args): return apply(_sdext.array_int32___setitem__,args)
    def cast(*args): return apply(_sdext.array_int32_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _sdext.array_int32_frompointer
    if _newclass:frompointer = staticmethod(_sdext.array_int32_frompointer)
    def __repr__(self):
        return "<C array_int32 instance at %s>" % (self.this,)

class array_int32Ptr(array_int32):
    def __init__(self,this):
        _swig_setattr(self, array_int32, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_int32, 'thisown', 0)
        _swig_setattr(self, array_int32,self.__class__,array_int32)
_sdext.array_int32_swigregister(array_int32Ptr)
array_int32_frompointer = _sdext.array_int32_frompointer


class array_float32(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_float32, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_float32, name)
    def __init__(self,*args):
        _swig_setattr(self, array_float32, 'this', apply(_sdext.new_array_float32,args))
        _swig_setattr(self, array_float32, 'thisown', 1)
    def __del__(self, destroy= _sdext.delete_array_float32):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_sdext.array_float32___getitem__,args)
    def __setitem__(*args): return apply(_sdext.array_float32___setitem__,args)
    def cast(*args): return apply(_sdext.array_float32_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _sdext.array_float32_frompointer
    if _newclass:frompointer = staticmethod(_sdext.array_float32_frompointer)
    def __repr__(self):
        return "<C array_float32 instance at %s>" % (self.this,)

class array_float32Ptr(array_float32):
    def __init__(self,this):
        _swig_setattr(self, array_float32, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_float32, 'thisown', 0)
        _swig_setattr(self, array_float32,self.__class__,array_float32)
_sdext.array_float32_swigregister(array_float32Ptr)
array_float32_frompointer = _sdext.array_float32_frompointer


class array_float64(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_float64, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_float64, name)
    def __init__(self,*args):
        _swig_setattr(self, array_float64, 'this', apply(_sdext.new_array_float64,args))
        _swig_setattr(self, array_float64, 'thisown', 1)
    def __del__(self, destroy= _sdext.delete_array_float64):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_sdext.array_float64___getitem__,args)
    def __setitem__(*args): return apply(_sdext.array_float64___setitem__,args)
    def cast(*args): return apply(_sdext.array_float64_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _sdext.array_float64_frompointer
    if _newclass:frompointer = staticmethod(_sdext.array_float64_frompointer)
    def __repr__(self):
        return "<C array_float64 instance at %s>" % (self.this,)

class array_float64Ptr(array_float64):
    def __init__(self,this):
        _swig_setattr(self, array_float64, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_float64, 'thisown', 0)
        _swig_setattr(self, array_float64,self.__class__,array_float64)
_sdext.array_float64_swigregister(array_float64Ptr)
array_float64_frompointer = _sdext.array_float64_frompointer


_SDreaddata_0 = _sdext._SDreaddata_0

_SDwritedata_0 = _sdext._SDwritedata_0

SDstart = _sdext.SDstart

SDcreate = _sdext.SDcreate

SDselect = _sdext.SDselect

SDendaccess = _sdext.SDendaccess

SDend = _sdext.SDend

SDfileinfo = _sdext.SDfileinfo

SDgetinfo = _sdext.SDgetinfo

SDcheckempty = _sdext.SDcheckempty

SDidtoref = _sdext.SDidtoref

SDiscoordvar = _sdext.SDiscoordvar

SDisrecord = _sdext.SDisrecord

SDnametoindex = _sdext.SDnametoindex

SDreftoindex = _sdext.SDreftoindex

SDdiminfo = _sdext.SDdiminfo

SDgetdimid = _sdext.SDgetdimid

SDsetdimname = _sdext.SDsetdimname

SDgetdimscale = _sdext.SDgetdimscale

SDsetdimscale = _sdext.SDsetdimscale

SDattrinfo = _sdext.SDattrinfo

SDfindattr = _sdext.SDfindattr

SDreadattr = _sdext.SDreadattr

SDsetattr = _sdext.SDsetattr

SDgetcal = _sdext.SDgetcal

SDgetdatastrs = _sdext.SDgetdatastrs

SDgetdimstrs = _sdext.SDgetdimstrs

SDgetfillvalue = _sdext.SDgetfillvalue

SDgetrange = _sdext.SDgetrange

SDsetcal = _sdext.SDsetcal

SDsetdatastrs = _sdext.SDsetdatastrs

SDsetdimstrs = _sdext.SDsetdimstrs

SDsetfillmode = _sdext.SDsetfillmode

SDsetfillvalue = _sdext.SDsetfillvalue

SDsetrange = _sdext.SDsetrange

_SDgetcompress = _sdext._SDgetcompress

_SDsetcompress = _sdext._SDsetcompress

SDsetexternalfile = _sdext.SDsetexternalfile

HEvalue = _sdext.HEvalue

HEstring = _sdext.HEstring

_HEprint = _sdext._HEprint


