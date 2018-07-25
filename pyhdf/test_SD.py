#!/usr/bin/env python

import numpy as np
import os
import pyhdf.SD
import tempfile
from nose.tools import eq_
from numpy.testing import assert_array_equal
from pyhdf.SD import SDC

def test_long_varname():
    sds_name = 'a'*255

    _, path = tempfile.mkstemp(suffix='.hdf', prefix='pyhdf_')
    try:
        # create a file with a long variable name
        sd = pyhdf.SD.SD(path, SDC.WRITE|SDC.CREATE|SDC.TRUNC)
        sds = sd.create(sds_name, SDC.FLOAT32, (3,))
        sds[:] = range(10, 13)
        sds.endaccess()
        sd.end()

        # check we can read the variable name
        sd = pyhdf.SD.SD(path)
        sds = sd.select(sds_name)
        name, _, _, _, _ = sds.info()
        sds.endaccess()
        sd.end()
        eq_(sds_name, name)
    finally:
        os.unlink(path)

def test_negative_int8():
    _, path = tempfile.mkstemp(suffix='.hdf', prefix='pyhdf_')
    try:
        sd = pyhdf.SD.SD(path, SDC.WRITE|SDC.CREATE|SDC.TRUNC)
        data = np.zeros(shape=(20,20), dtype=np.int8)
        sds = sd.create("testsds", SDC.INT8, data.shape)
        sds.setfillvalue(-1)
        eq_(sds.getfillvalue(), -1)

        sds.setrange(-50, -30)
        min, max = sds.getrange()
        eq_(min, -50)
        eq_(max, -30)

        attr = sds.attr("testattr")
        attr.set(SDC.INT8, -1)
        eq_(attr.get(), -1)

        dim = sds.dim(0)
        scale = [-1]*20
        dim.setscale(SDC.INT8, scale)
        assert_array_equal(dim.getscale(), scale)

        sds[:,:] = -40
        sd.end()
    finally:
        os.unlink(path)
