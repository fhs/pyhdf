# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.
import _hdfext
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


DFNT_NONE = _hdfext.DFNT_NONE
DFNT_QUERY = _hdfext.DFNT_QUERY
DFNT_VERSION = _hdfext.DFNT_VERSION
DFNT_FLOAT32 = _hdfext.DFNT_FLOAT32
DFNT_FLOAT = _hdfext.DFNT_FLOAT
DFNT_FLOAT64 = _hdfext.DFNT_FLOAT64
DFNT_DOUBLE = _hdfext.DFNT_DOUBLE
DFNT_FLOAT128 = _hdfext.DFNT_FLOAT128
DFNT_INT8 = _hdfext.DFNT_INT8
DFNT_UINT8 = _hdfext.DFNT_UINT8
DFNT_INT16 = _hdfext.DFNT_INT16
DFNT_UINT16 = _hdfext.DFNT_UINT16
DFNT_INT32 = _hdfext.DFNT_INT32
DFNT_UINT32 = _hdfext.DFNT_UINT32
DFNT_INT64 = _hdfext.DFNT_INT64
DFNT_UINT64 = _hdfext.DFNT_UINT64
DFNT_INT128 = _hdfext.DFNT_INT128
DFNT_UINT128 = _hdfext.DFNT_UINT128
DFNT_UCHAR8 = _hdfext.DFNT_UCHAR8
DFNT_UCHAR = _hdfext.DFNT_UCHAR
DFNT_CHAR8 = _hdfext.DFNT_CHAR8
DFNT_CHAR = _hdfext.DFNT_CHAR
DFNT_CHAR16 = _hdfext.DFNT_CHAR16
DFNT_UCHAR16 = _hdfext.DFNT_UCHAR16
SD_UNLIMITED = _hdfext.SD_UNLIMITED
SD_FILL = _hdfext.SD_FILL
SD_NOFILL = _hdfext.SD_NOFILL
DFACC_READ = _hdfext.DFACC_READ
DFACC_WRITE = _hdfext.DFACC_WRITE
DFACC_CREATE = _hdfext.DFACC_CREATE
DFACC_ALL = _hdfext.DFACC_ALL
DFACC_RDONLY = _hdfext.DFACC_RDONLY
DFACC_RDWR = _hdfext.DFACC_RDWR
DFACC_CLOBBER = _hdfext.DFACC_CLOBBER
DFACC_BUFFER = _hdfext.DFACC_BUFFER
DFACC_APPENDABLE = _hdfext.DFACC_APPENDABLE
DFACC_CURRENT = _hdfext.DFACC_CURRENT
DFACC_OLD = _hdfext.DFACC_OLD
COMP_CODE_NONE = _hdfext.COMP_CODE_NONE
COMP_CODE_RLE = _hdfext.COMP_CODE_RLE
COMP_CODE_NBIT = _hdfext.COMP_CODE_NBIT
COMP_CODE_SKPHUFF = _hdfext.COMP_CODE_SKPHUFF
COMP_CODE_DEFLATE = _hdfext.COMP_CODE_DEFLATE
COMP_CODE_SZIP = _hdfext.COMP_CODE_SZIP
DFTAG_NDG = _hdfext.DFTAG_NDG
DFTAG_VH = _hdfext.DFTAG_VH
DFTAG_VG = _hdfext.DFTAG_VG
class array_byte(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_byte, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_byte, name)
    def __init__(self,*args):
        _swig_setattr(self, array_byte, 'this', apply(_hdfext.new_array_byte,args))
        _swig_setattr(self, array_byte, 'thisown', 1)
    def __del__(self, destroy= _hdfext.delete_array_byte):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_hdfext.array_byte___getitem__,args)
    def __setitem__(*args): return apply(_hdfext.array_byte___setitem__,args)
    def cast(*args): return apply(_hdfext.array_byte_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _hdfext.array_byte_frompointer
    if _newclass:frompointer = staticmethod(_hdfext.array_byte_frompointer)
    def __repr__(self):
        return "<C array_byte instance at %s>" % (self.this,)

class array_bytePtr(array_byte):
    def __init__(self,this):
        _swig_setattr(self, array_byte, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_byte, 'thisown', 0)
        _swig_setattr(self, array_byte,self.__class__,array_byte)
_hdfext.array_byte_swigregister(array_bytePtr)
array_byte_frompointer = _hdfext.array_byte_frompointer


class array_int8(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_int8, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_int8, name)
    def __init__(self,*args):
        _swig_setattr(self, array_int8, 'this', apply(_hdfext.new_array_int8,args))
        _swig_setattr(self, array_int8, 'thisown', 1)
    def __del__(self, destroy= _hdfext.delete_array_int8):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_hdfext.array_int8___getitem__,args)
    def __setitem__(*args): return apply(_hdfext.array_int8___setitem__,args)
    def cast(*args): return apply(_hdfext.array_int8_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _hdfext.array_int8_frompointer
    if _newclass:frompointer = staticmethod(_hdfext.array_int8_frompointer)
    def __repr__(self):
        return "<C array_int8 instance at %s>" % (self.this,)

class array_int8Ptr(array_int8):
    def __init__(self,this):
        _swig_setattr(self, array_int8, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_int8, 'thisown', 0)
        _swig_setattr(self, array_int8,self.__class__,array_int8)
_hdfext.array_int8_swigregister(array_int8Ptr)
array_int8_frompointer = _hdfext.array_int8_frompointer


class array_int16(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_int16, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_int16, name)
    def __init__(self,*args):
        _swig_setattr(self, array_int16, 'this', apply(_hdfext.new_array_int16,args))
        _swig_setattr(self, array_int16, 'thisown', 1)
    def __del__(self, destroy= _hdfext.delete_array_int16):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_hdfext.array_int16___getitem__,args)
    def __setitem__(*args): return apply(_hdfext.array_int16___setitem__,args)
    def cast(*args): return apply(_hdfext.array_int16_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _hdfext.array_int16_frompointer
    if _newclass:frompointer = staticmethod(_hdfext.array_int16_frompointer)
    def __repr__(self):
        return "<C array_int16 instance at %s>" % (self.this,)

class array_int16Ptr(array_int16):
    def __init__(self,this):
        _swig_setattr(self, array_int16, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_int16, 'thisown', 0)
        _swig_setattr(self, array_int16,self.__class__,array_int16)
_hdfext.array_int16_swigregister(array_int16Ptr)
array_int16_frompointer = _hdfext.array_int16_frompointer


class array_uint16(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_uint16, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_uint16, name)
    def __init__(self,*args):
        _swig_setattr(self, array_uint16, 'this', apply(_hdfext.new_array_uint16,args))
        _swig_setattr(self, array_uint16, 'thisown', 1)
    def __del__(self, destroy= _hdfext.delete_array_uint16):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_hdfext.array_uint16___getitem__,args)
    def __setitem__(*args): return apply(_hdfext.array_uint16___setitem__,args)
    def cast(*args): return apply(_hdfext.array_uint16_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _hdfext.array_uint16_frompointer
    if _newclass:frompointer = staticmethod(_hdfext.array_uint16_frompointer)
    def __repr__(self):
        return "<C array_uint16 instance at %s>" % (self.this,)

class array_uint16Ptr(array_uint16):
    def __init__(self,this):
        _swig_setattr(self, array_uint16, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_uint16, 'thisown', 0)
        _swig_setattr(self, array_uint16,self.__class__,array_uint16)
_hdfext.array_uint16_swigregister(array_uint16Ptr)
array_uint16_frompointer = _hdfext.array_uint16_frompointer


class array_int32(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_int32, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_int32, name)
    def __init__(self,*args):
        _swig_setattr(self, array_int32, 'this', apply(_hdfext.new_array_int32,args))
        _swig_setattr(self, array_int32, 'thisown', 1)
    def __del__(self, destroy= _hdfext.delete_array_int32):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_hdfext.array_int32___getitem__,args)
    def __setitem__(*args): return apply(_hdfext.array_int32___setitem__,args)
    def cast(*args): return apply(_hdfext.array_int32_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _hdfext.array_int32_frompointer
    if _newclass:frompointer = staticmethod(_hdfext.array_int32_frompointer)
    def __repr__(self):
        return "<C array_int32 instance at %s>" % (self.this,)

class array_int32Ptr(array_int32):
    def __init__(self,this):
        _swig_setattr(self, array_int32, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_int32, 'thisown', 0)
        _swig_setattr(self, array_int32,self.__class__,array_int32)
_hdfext.array_int32_swigregister(array_int32Ptr)
array_int32_frompointer = _hdfext.array_int32_frompointer


class array_uint32(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_uint32, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_uint32, name)
    def __init__(self,*args):
        _swig_setattr(self, array_uint32, 'this', apply(_hdfext.new_array_uint32,args))
        _swig_setattr(self, array_uint32, 'thisown', 1)
    def __del__(self, destroy= _hdfext.delete_array_uint32):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_hdfext.array_uint32___getitem__,args)
    def __setitem__(*args): return apply(_hdfext.array_uint32___setitem__,args)
    def cast(*args): return apply(_hdfext.array_uint32_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _hdfext.array_uint32_frompointer
    if _newclass:frompointer = staticmethod(_hdfext.array_uint32_frompointer)
    def __repr__(self):
        return "<C array_uint32 instance at %s>" % (self.this,)

class array_uint32Ptr(array_uint32):
    def __init__(self,this):
        _swig_setattr(self, array_uint32, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_uint32, 'thisown', 0)
        _swig_setattr(self, array_uint32,self.__class__,array_uint32)
_hdfext.array_uint32_swigregister(array_uint32Ptr)
array_uint32_frompointer = _hdfext.array_uint32_frompointer


class array_float32(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_float32, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_float32, name)
    def __init__(self,*args):
        _swig_setattr(self, array_float32, 'this', apply(_hdfext.new_array_float32,args))
        _swig_setattr(self, array_float32, 'thisown', 1)
    def __del__(self, destroy= _hdfext.delete_array_float32):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_hdfext.array_float32___getitem__,args)
    def __setitem__(*args): return apply(_hdfext.array_float32___setitem__,args)
    def cast(*args): return apply(_hdfext.array_float32_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _hdfext.array_float32_frompointer
    if _newclass:frompointer = staticmethod(_hdfext.array_float32_frompointer)
    def __repr__(self):
        return "<C array_float32 instance at %s>" % (self.this,)

class array_float32Ptr(array_float32):
    def __init__(self,this):
        _swig_setattr(self, array_float32, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_float32, 'thisown', 0)
        _swig_setattr(self, array_float32,self.__class__,array_float32)
_hdfext.array_float32_swigregister(array_float32Ptr)
array_float32_frompointer = _hdfext.array_float32_frompointer


class array_float64(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_float64, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_float64, name)
    def __init__(self,*args):
        _swig_setattr(self, array_float64, 'this', apply(_hdfext.new_array_float64,args))
        _swig_setattr(self, array_float64, 'thisown', 1)
    def __del__(self, destroy= _hdfext.delete_array_float64):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_hdfext.array_float64___getitem__,args)
    def __setitem__(*args): return apply(_hdfext.array_float64___setitem__,args)
    def cast(*args): return apply(_hdfext.array_float64_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _hdfext.array_float64_frompointer
    if _newclass:frompointer = staticmethod(_hdfext.array_float64_frompointer)
    def __repr__(self):
        return "<C array_float64 instance at %s>" % (self.this,)

class array_float64Ptr(array_float64):
    def __init__(self,this):
        _swig_setattr(self, array_float64, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_float64, 'thisown', 0)
        _swig_setattr(self, array_float64,self.__class__,array_float64)
_hdfext.array_float64_swigregister(array_float64Ptr)
array_float64_frompointer = _hdfext.array_float64_frompointer


new_array_voidp = _hdfext.new_array_voidp

delete_array_voidp = _hdfext.delete_array_voidp

array_voidp_getitem = _hdfext.array_voidp_getitem

array_voidp_setitem = _hdfext.array_voidp_setitem

Hopen = _hdfext.Hopen

Hclose = _hdfext.Hclose

Hgetlibversion = _hdfext.Hgetlibversion

Hgetfileversion = _hdfext.Hgetfileversion

Hishdf = _hdfext.Hishdf

HEvalue = _hdfext.HEvalue

HEstring = _hdfext.HEstring

_HEprint = _hdfext._HEprint

_SDreaddata_0 = _hdfext._SDreaddata_0

_SDwritedata_0 = _hdfext._SDwritedata_0

SDstart = _hdfext.SDstart

SDcreate = _hdfext.SDcreate

SDselect = _hdfext.SDselect

SDendaccess = _hdfext.SDendaccess

SDend = _hdfext.SDend

SDfileinfo = _hdfext.SDfileinfo

SDgetinfo = _hdfext.SDgetinfo

SDcheckempty = _hdfext.SDcheckempty

SDidtoref = _hdfext.SDidtoref

SDiscoordvar = _hdfext.SDiscoordvar

SDisrecord = _hdfext.SDisrecord

SDnametoindex = _hdfext.SDnametoindex

SDreftoindex = _hdfext.SDreftoindex

SDdiminfo = _hdfext.SDdiminfo

SDgetdimid = _hdfext.SDgetdimid

SDsetdimname = _hdfext.SDsetdimname

SDgetdimscale = _hdfext.SDgetdimscale

SDsetdimscale = _hdfext.SDsetdimscale

SDattrinfo = _hdfext.SDattrinfo

SDfindattr = _hdfext.SDfindattr

SDreadattr = _hdfext.SDreadattr

SDsetattr = _hdfext.SDsetattr

SDgetcal = _hdfext.SDgetcal

SDgetdatastrs = _hdfext.SDgetdatastrs

SDgetdimstrs = _hdfext.SDgetdimstrs

SDgetfillvalue = _hdfext.SDgetfillvalue

SDgetrange = _hdfext.SDgetrange

SDsetcal = _hdfext.SDsetcal

SDsetdatastrs = _hdfext.SDsetdatastrs

SDsetdimstrs = _hdfext.SDsetdimstrs

SDsetfillmode = _hdfext.SDsetfillmode

SDsetfillvalue = _hdfext.SDsetfillvalue

SDsetrange = _hdfext.SDsetrange

_SDgetcompress = _hdfext._SDgetcompress

_SDsetcompress = _hdfext._SDsetcompress

SDsetexternalfile = _hdfext.SDsetexternalfile

Vinitialize = _hdfext.Vinitialize

VSattach = _hdfext.VSattach

VSdetach = _hdfext.VSdetach

Vfinish = _hdfext.Vfinish

VHstoredata = _hdfext.VHstoredata

VHstoredatam = _hdfext.VHstoredatam

VSfdefine = _hdfext.VSfdefine

VSsetfields = _hdfext.VSsetfields

VSseek = _hdfext.VSseek

VSread = _hdfext.VSread

VSwrite = _hdfext.VSwrite

VSfpack = _hdfext.VSfpack

VSelts = _hdfext.VSelts

VSgetclass = _hdfext.VSgetclass

VSgetfields = _hdfext.VSgetfields

VSgetinterlace = _hdfext.VSgetinterlace

VSgetname = _hdfext.VSgetname

VSsizeof = _hdfext.VSsizeof

VSinquire = _hdfext.VSinquire

VSQuerytag = _hdfext.VSQuerytag

VSQueryref = _hdfext.VSQueryref

VSfindex = _hdfext.VSfindex

VSisattr = _hdfext.VSisattr

VFnfields = _hdfext.VFnfields

VFfieldtype = _hdfext.VFfieldtype

VFfieldname = _hdfext.VFfieldname

VFfieldesize = _hdfext.VFfieldesize

VFfieldisize = _hdfext.VFfieldisize

VFfieldorder = _hdfext.VFfieldorder

VSfind = _hdfext.VSfind

VSgetid = _hdfext.VSgetid

VSfexist = _hdfext.VSfexist

VSsetclass = _hdfext.VSsetclass

VSsetname = _hdfext.VSsetname

VSsetinterlace = _hdfext.VSsetinterlace

VSsetattr = _hdfext.VSsetattr

VSgetattr = _hdfext.VSgetattr

VSfnattrs = _hdfext.VSfnattrs

VSnattrs = _hdfext.VSnattrs

VSattrinfo = _hdfext.VSattrinfo

VSfindattr = _hdfext.VSfindattr

Vattach = _hdfext.Vattach

Vdetach = _hdfext.Vdetach

Vgetname = _hdfext.Vgetname

Vsetname = _hdfext.Vsetname

Vgetclass = _hdfext.Vgetclass

Vsetclass = _hdfext.Vsetclass

Vfind = _hdfext.Vfind

Vfindclass = _hdfext.Vfindclass

Vinsert = _hdfext.Vinsert

Vaddtagref = _hdfext.Vaddtagref

Vdeletetagref = _hdfext.Vdeletetagref

Vdelete = _hdfext.Vdelete

VQueryref = _hdfext.VQueryref

VQuerytag = _hdfext.VQuerytag

Vntagrefs = _hdfext.Vntagrefs

Vgettagref = _hdfext.Vgettagref

Vgetversion = _hdfext.Vgetversion

Vgettagrefs = _hdfext.Vgettagrefs

Vgetid = _hdfext.Vgetid

Vinqtagref = _hdfext.Vinqtagref

Visvg = _hdfext.Visvg

Visvs = _hdfext.Visvs

Vnrefs = _hdfext.Vnrefs

Vfindattr = _hdfext.Vfindattr

Vgetattr = _hdfext.Vgetattr

Vsetattr = _hdfext.Vsetattr

Vattrinfo = _hdfext.Vattrinfo

Vnattrs = _hdfext.Vnattrs


