import numpy as np
from numpy.testing import assert_array_equal

from pyhdf import hdfext
from pyhdf.SD import SD, SDC


LITTLE_ENDIAN = 0x4000


def test_little_endian_get(tmp_path):
    path = str(tmp_path / 'little.hdf')
    sd = SD(path, SDC.WRITE | SDC.CREATE)
    sds = sd.create('values', SDC.INT16 | LITTLE_ENDIAN, (3,))
    hdfext._SDwritedata_0(sds._id, SDC.INT16, [0], [3], [-1234, 0, 1234], [1])
    sds.endaccess()
    sd.end()

    sd = SD(path)
    sds = sd.select('values')
    assert sds.info()[3] == SDC.INT16 | LITTLE_ENDIAN
    assert_array_equal(sds.get(), np.array([-1234, 0, 1234], dtype=np.int16))
    sds.endaccess()
    sd.end()


def test_little_endian_set(tmp_path):
    path = str(tmp_path / 'little.hdf')
    sd = SD(path, SDC.WRITE | SDC.CREATE)
    sds = sd.create('values', SDC.INT16 | LITTLE_ENDIAN, (3,))
    sds.set([-1234, 0, 1234])
    actual = hdfext._SDreaddata_0(sds._id, SDC.INT16, [0], [3], [1])
    assert_array_equal(actual, np.array([-1234, 0, 1234], dtype=np.int16))
    sds.endaccess()
    sd.end()
