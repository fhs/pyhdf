# $Id: error.py,v 1.1 2004-08-02 15:00:34 gosselin Exp $
# $Log: not supported by cvs2svn $

import hdfext as _C

# #################
# Error processing
# #################

class HDF4Error(Exception):

    def __init__(self, args=None):
        self.args = args

def _checkErr(procName, val, msg=""):

    if val < 0:
        #_C._HEprint();
        errCode = _C.HEvalue(1)
        if errCode != 0:
            str = "%s (%d): %s" % (procName, errCode, _C.HEstring(errCode))
        else:
            str = "%s : %s" % (procName, msg)
        raise HDF4Error, str

