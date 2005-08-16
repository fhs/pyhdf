# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.
import _pycdfext
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


class array_byte(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_byte, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_byte, name)
    def __init__(self,*args):
        _swig_setattr(self, array_byte, 'this', apply(_pycdfext.new_array_byte,args))
        _swig_setattr(self, array_byte, 'thisown', 1)
    def __del__(self, destroy= _pycdfext.delete_array_byte):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_pycdfext.array_byte___getitem__,args)
    def __setitem__(*args): return apply(_pycdfext.array_byte___setitem__,args)
    def cast(*args): return apply(_pycdfext.array_byte_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _pycdfext.array_byte_frompointer
    if _newclass:frompointer = staticmethod(_pycdfext.array_byte_frompointer)
    def __repr__(self):
        return "<C array_byte instance at %s>" % (self.this,)

class array_bytePtr(array_byte):
    def __init__(self,this):
        _swig_setattr(self, array_byte, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_byte, 'thisown', 0)
        _swig_setattr(self, array_byte,self.__class__,array_byte)
_pycdfext.array_byte_swigregister(array_bytePtr)
array_byte_frompointer = _pycdfext.array_byte_frompointer


class array_int16(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_int16, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_int16, name)
    def __init__(self,*args):
        _swig_setattr(self, array_int16, 'this', apply(_pycdfext.new_array_int16,args))
        _swig_setattr(self, array_int16, 'thisown', 1)
    def __del__(self, destroy= _pycdfext.delete_array_int16):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_pycdfext.array_int16___getitem__,args)
    def __setitem__(*args): return apply(_pycdfext.array_int16___setitem__,args)
    def cast(*args): return apply(_pycdfext.array_int16_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _pycdfext.array_int16_frompointer
    if _newclass:frompointer = staticmethod(_pycdfext.array_int16_frompointer)
    def __repr__(self):
        return "<C array_int16 instance at %s>" % (self.this,)

class array_int16Ptr(array_int16):
    def __init__(self,this):
        _swig_setattr(self, array_int16, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_int16, 'thisown', 0)
        _swig_setattr(self, array_int16,self.__class__,array_int16)
_pycdfext.array_int16_swigregister(array_int16Ptr)
array_int16_frompointer = _pycdfext.array_int16_frompointer


class array_uint16(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_uint16, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_uint16, name)
    def __init__(self,*args):
        _swig_setattr(self, array_uint16, 'this', apply(_pycdfext.new_array_uint16,args))
        _swig_setattr(self, array_uint16, 'thisown', 1)
    def __del__(self, destroy= _pycdfext.delete_array_uint16):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_pycdfext.array_uint16___getitem__,args)
    def __setitem__(*args): return apply(_pycdfext.array_uint16___setitem__,args)
    def cast(*args): return apply(_pycdfext.array_uint16_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _pycdfext.array_uint16_frompointer
    if _newclass:frompointer = staticmethod(_pycdfext.array_uint16_frompointer)
    def __repr__(self):
        return "<C array_uint16 instance at %s>" % (self.this,)

class array_uint16Ptr(array_uint16):
    def __init__(self,this):
        _swig_setattr(self, array_uint16, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_uint16, 'thisown', 0)
        _swig_setattr(self, array_uint16,self.__class__,array_uint16)
_pycdfext.array_uint16_swigregister(array_uint16Ptr)
array_uint16_frompointer = _pycdfext.array_uint16_frompointer


class array_int(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_int, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_int, name)
    def __init__(self,*args):
        _swig_setattr(self, array_int, 'this', apply(_pycdfext.new_array_int,args))
        _swig_setattr(self, array_int, 'thisown', 1)
    def __del__(self, destroy= _pycdfext.delete_array_int):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_pycdfext.array_int___getitem__,args)
    def __setitem__(*args): return apply(_pycdfext.array_int___setitem__,args)
    def cast(*args): return apply(_pycdfext.array_int_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _pycdfext.array_int_frompointer
    if _newclass:frompointer = staticmethod(_pycdfext.array_int_frompointer)
    def __repr__(self):
        return "<C array_int instance at %s>" % (self.this,)

class array_intPtr(array_int):
    def __init__(self,this):
        _swig_setattr(self, array_int, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_int, 'thisown', 0)
        _swig_setattr(self, array_int,self.__class__,array_int)
_pycdfext.array_int_swigregister(array_intPtr)
array_int_frompointer = _pycdfext.array_int_frompointer


class array_float(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_float, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_float, name)
    def __init__(self,*args):
        _swig_setattr(self, array_float, 'this', apply(_pycdfext.new_array_float,args))
        _swig_setattr(self, array_float, 'thisown', 1)
    def __del__(self, destroy= _pycdfext.delete_array_float):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_pycdfext.array_float___getitem__,args)
    def __setitem__(*args): return apply(_pycdfext.array_float___setitem__,args)
    def cast(*args): return apply(_pycdfext.array_float_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _pycdfext.array_float_frompointer
    if _newclass:frompointer = staticmethod(_pycdfext.array_float_frompointer)
    def __repr__(self):
        return "<C array_float instance at %s>" % (self.this,)

class array_floatPtr(array_float):
    def __init__(self,this):
        _swig_setattr(self, array_float, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_float, 'thisown', 0)
        _swig_setattr(self, array_float,self.__class__,array_float)
_pycdfext.array_float_swigregister(array_floatPtr)
array_float_frompointer = _pycdfext.array_float_frompointer


class array_double(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_double, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_double, name)
    def __init__(self,*args):
        _swig_setattr(self, array_double, 'this', apply(_pycdfext.new_array_double,args))
        _swig_setattr(self, array_double, 'thisown', 1)
    def __del__(self, destroy= _pycdfext.delete_array_double):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_pycdfext.array_double___getitem__,args)
    def __setitem__(*args): return apply(_pycdfext.array_double___setitem__,args)
    def cast(*args): return apply(_pycdfext.array_double_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _pycdfext.array_double_frompointer
    if _newclass:frompointer = staticmethod(_pycdfext.array_double_frompointer)
    def __repr__(self):
        return "<C array_double instance at %s>" % (self.this,)

class array_doublePtr(array_double):
    def __init__(self,this):
        _swig_setattr(self, array_double, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_double, 'thisown', 0)
        _swig_setattr(self, array_double,self.__class__,array_double)
_pycdfext.array_double_swigregister(array_doublePtr)
array_double_frompointer = _pycdfext.array_double_frompointer


class array_size_t(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, array_size_t, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, array_size_t, name)
    def __init__(self,*args):
        _swig_setattr(self, array_size_t, 'this', apply(_pycdfext.new_array_size_t,args))
        _swig_setattr(self, array_size_t, 'thisown', 1)
    def __del__(self, destroy= _pycdfext.delete_array_size_t):
        try:
            if self.thisown: destroy(self)
        except: pass
    def __getitem__(*args): return apply(_pycdfext.array_size_t___getitem__,args)
    def __setitem__(*args): return apply(_pycdfext.array_size_t___setitem__,args)
    def cast(*args): return apply(_pycdfext.array_size_t_cast,args)
    __swig_getmethods__["frompointer"] = lambda x: _pycdfext.array_size_t_frompointer
    if _newclass:frompointer = staticmethod(_pycdfext.array_size_t_frompointer)
    def __repr__(self):
        return "<C array_size_t instance at %s>" % (self.this,)

class array_size_tPtr(array_size_t):
    def __init__(self,this):
        _swig_setattr(self, array_size_t, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, array_size_t, 'thisown', 0)
        _swig_setattr(self, array_size_t,self.__class__,array_size_t)
_pycdfext.array_size_t_swigregister(array_size_tPtr)
array_size_t_frompointer = _pycdfext.array_size_t_frompointer


NC_NOERR = _pycdfext.NC_NOERR
NC_NOWRITE = _pycdfext.NC_NOWRITE
NC_WRITE = _pycdfext.NC_WRITE
NC_CLOBBER = _pycdfext.NC_CLOBBER
NC_NOCLOBBER = _pycdfext.NC_NOCLOBBER
NC_64BIT_OFFSET = _pycdfext.NC_64BIT_OFFSET
NC_FILL = _pycdfext.NC_FILL
NC_NOFILL = _pycdfext.NC_NOFILL
NC_LOCK = _pycdfext.NC_LOCK
NC_SHARE = _pycdfext.NC_SHARE
NC_NAT = _pycdfext.NC_NAT
NC_BYTE = _pycdfext.NC_BYTE
NC_CHAR = _pycdfext.NC_CHAR
NC_SHORT = _pycdfext.NC_SHORT
NC_INT = _pycdfext.NC_INT
NC_FLOAT = _pycdfext.NC_FLOAT
NC_DOUBLE = _pycdfext.NC_DOUBLE
NC_GLOBAL = _pycdfext.NC_GLOBAL
NC_UNLIMITED = _pycdfext.NC_UNLIMITED
NOERR = _pycdfext.NOERR
NOWRITE = _pycdfext.NOWRITE
WRITE = _pycdfext.WRITE
CLOBBER = _pycdfext.CLOBBER
NOCLOBBER = _pycdfext.NOCLOBBER
BIT64_OFFSET = _pycdfext.BIT64_OFFSET
FILL = _pycdfext.FILL
NOFILL = _pycdfext.NOFILL
LOCK = _pycdfext.LOCK
SHARE = _pycdfext.SHARE
NAT = _pycdfext.NAT
BYTE = _pycdfext.BYTE
CHAR = _pycdfext.CHAR
SHORT = _pycdfext.SHORT
INT = _pycdfext.INT
FLOAT = _pycdfext.FLOAT
DOUBLE = _pycdfext.DOUBLE
GLOBAL = _pycdfext.GLOBAL
UNLIMITED = _pycdfext.UNLIMITED
_nc_get_var_0 = _pycdfext._nc_get_var_0

_nc_put_var_0 = _pycdfext._nc_put_var_0

nc_inq_libvers = _pycdfext.nc_inq_libvers

nc_strerror = _pycdfext.nc_strerror

nc_create = _pycdfext.nc_create

nc_open = _pycdfext.nc_open

nc_close = _pycdfext.nc_close

nc_redef = _pycdfext.nc_redef

nc_enddef = _pycdfext.nc_enddef

nc_inq = _pycdfext.nc_inq

nc_inq_ndims = _pycdfext.nc_inq_ndims

nc_inq_nvars = _pycdfext.nc_inq_nvars

nc_inq_natts = _pycdfext.nc_inq_natts

nc_inq_unlimdim = _pycdfext.nc_inq_unlimdim

nc_sync = _pycdfext.nc_sync

nc_abort = _pycdfext.nc_abort

nc_set_fill = _pycdfext.nc_set_fill

nc_def_dim = _pycdfext.nc_def_dim

nc_inq_dimid = _pycdfext.nc_inq_dimid

nc_inq_dim = _pycdfext.nc_inq_dim

nc_inq_dimname = _pycdfext.nc_inq_dimname

nc_inq_dimlen = _pycdfext.nc_inq_dimlen

nc_rename_dim = _pycdfext.nc_rename_dim

nc_def_var = _pycdfext.nc_def_var

nc_inq_varid = _pycdfext.nc_inq_varid

nc_inq_var = _pycdfext.nc_inq_var

nc_inq_varname = _pycdfext.nc_inq_varname

nc_inq_vartype = _pycdfext.nc_inq_vartype

nc_inq_varndims = _pycdfext.nc_inq_varndims

nc_inq_vardimid = _pycdfext.nc_inq_vardimid

nc_inq_varnatts = _pycdfext.nc_inq_varnatts

nc_put_var1_text = _pycdfext.nc_put_var1_text

nc_put_var1_uchar = _pycdfext.nc_put_var1_uchar

nc_put_var1_int = _pycdfext.nc_put_var1_int

nc_put_var1_double = _pycdfext.nc_put_var1_double

nc_get_var1_text = _pycdfext.nc_get_var1_text

nc_get_var1_uchar = _pycdfext.nc_get_var1_uchar

nc_get_var1_int = _pycdfext.nc_get_var1_int

nc_get_var1_double = _pycdfext.nc_get_var1_double

nc_rename_var = _pycdfext.nc_rename_var

nc_put_att_text = _pycdfext.nc_put_att_text

nc_put_att_uchar = _pycdfext.nc_put_att_uchar

nc_put_att_int = _pycdfext.nc_put_att_int

nc_put_att_float = _pycdfext.nc_put_att_float

nc_put_att_double = _pycdfext.nc_put_att_double

nc_inq_att = _pycdfext.nc_inq_att

nc_inq_atttype = _pycdfext.nc_inq_atttype

nc_inq_attlen = _pycdfext.nc_inq_attlen

nc_inq_attname = _pycdfext.nc_inq_attname

nc_inq_attid = _pycdfext.nc_inq_attid

nc_get_att_text = _pycdfext.nc_get_att_text

nc_get_att_uchar = _pycdfext.nc_get_att_uchar

nc_get_att_int = _pycdfext.nc_get_att_int

nc_get_att_double = _pycdfext.nc_get_att_double

nc_copy_att = _pycdfext.nc_copy_att

nc_del_att = _pycdfext.nc_del_att

nc_rename_att = _pycdfext.nc_rename_att


