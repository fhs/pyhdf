#!/usr/bin/env python

from numpy import *
from pycdf import *

if __name__ == '__main__':

    ############
    # test code
    ############

    def compCreate(name, ARec, BRec, CRec):
        """Create a component of a spanned CDF set.

        Arguments:
        name       name of the component file
        ARec       sequence of records to load in the A var
        BRec       sequence of records to load in the B var
        CRec       sequence of records to load in the C var

        compCreate() will initialize the file with the following:
        an unlimited dimension named 'time'
        a coordinate variable time(time), of type NC.INT
        dimensions Ad of length 1, Bd of length 2, and Cd of length 3
        record variable A(time, Ad) of type NC.INT
        record variable B(time, Bd) of type NC.BYTE
        record variable C(time, Cd) of type NC.DOUBLE
        
        variable A will be loaded with records from ARec,
        B with records from BRec, and C with records from CRec.
                                                              """

        cdf = CDF(name, NC.WRITE|NC.CREATE|NC.TRUNC)
        cdf.automode()
    
        Ad = cdf.def_dim('Ad', 1)
        Bd = cdf.def_dim('Bd', 2)
        Cd = cdf.def_dim('Cd', 3)
        tm = cdf.def_dim('time', NC.UNLIMITED)
        dum = cdf.def_dim('dum', 5)
        
        A = cdf.def_var('A', NC.INT,    (tm, Ad)) ; A.title = "this is A"
        B = cdf.def_var('B', NC.BYTE,   (tm, Bd)) ; B.title = "this is B"
        C = cdf.def_var('C', NC.DOUBLE, (tm, Cd)) ; C.title = "this is C"
        time = cdf.def_var('time', NC.INT, tm)
        time._FillValue = -1
        DUM = cdf.def_var('dum', NC.INT, dum)

        A[:len(ARec)] = ARec
        B[:] = BRec
        C[:] = CRec

    # Create 3 components of the spanned set
    compCreate(
           'c1.nc',
           (1000,2000,3000,4000,5000),
           (1,2,
            3,4,
            5,6,
            7,8,
            9,10),
           (-1, -2, -3,
            -4, -5, -6,
            -7, -8, -9,
            -10, -11, -12,
            -13, -14, -15)
           )

    compCreate(
           'c2.nc',
           (1000,2000,3000),
           (1,2,
            3,4,
            5,6),
           (-1, -2, -3,
            -4, -5, -6,
            -7, -8, -9)
           )

    compCreate(
           'c3.nc',
           (1000,2000),
           (1,2,
            3,4),
           (-1, -2, -3,
            -4, -5, -6)
           )

    cdfmf = CDFMF(('c1.nc', 'c2.nc', 'c3.nc'))
    unlimid = cdfmf.inq_unlimdim()
    print "unlimid=",unlimid
    print "total unlim length=", cdfmf.inq_unlimlen()
    A = cdfmf.var('A') ; print "A.title=", A.title
    B = cdfmf.var('B') ; print "B.title=", B.title
    C = cdfmf.var('C') ; print "C.title=", C.title
    print "shape A=", A.shape()
    print "shape B=", B.shape()
    print "shape C=", C.shape()

    print "A[:3,:]=", A[:3,:]
    print "A[:6]=", A[:6]
    print "A[5:8]=",A[5:8]
    print "A[5:9]=",A[5:9]
    print "A[::3,:]=", A[::3,:]
    print "A[::2, :]=", A[::2]

    print "B[3:11:3]=", B[3:11:3]
    print "C[10:]=", C[10:]

    print "A[...]=", A[...]
    print "B[...]=", B[...]
    print "C[...]=", C[...]
