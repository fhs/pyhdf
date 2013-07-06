""" Tools for reading an ASTER Level 2 HDF files.
"""

from pyhdf.SD import SD, SDC
from projection_module import UTMProjection
from pyhdf.odl_parser import parse_odl
# hack import pyhdf.odl_parser as odl_parser


__all__ = ['AST05', 'AST08']


class AST05(object):
    """ Represent a Surface Emissivity ASTER 05 Level 2 data product.
    """

    def __init__(self, filename, mode=SDC.READ):
        self.filename = filename
        self._open(mode)

    def _open(self, mode):
        """ Open the HDF file for reading.
        """
        self.sd = SD(self.filename, mode)
        ds = self.sd.datasets()
        assert set(ds) == set(['Band10', 'Band11', 'Band12', 'Band13', 'Band14', 'GeodeticLatitude', 'Longitude', 'QA_DataPlane', 'QA_DataPlane2'])

        pmd = parse_odl( self.sd.attributes()['productmetadata.0'] )
        self.proj = UTMProjection(
            pmd.ASTERGDSGENERICMETADATA.SCENECOORDINATES.SCENECENTER.VALUE,
            self.sd.select('GeodeticLatitude').get(),
            self.sd.select('Longitude').get(),
            (700, 830),
        )
        self.scale_factors = pmd.ASTERGDSGENERICMETADATA.BANDSCALEFACTORS.VALUE[-5:]
        self.band10 = self.sd.select('Band10').get()
        self.band11 = self.sd.select('Band11').get()
        self.band12 = self.sd.select('Band12').get()
        self.band13 = self.sd.select('Band13').get()
        self.band14 = self.sd.select('Band14').get()
        self.all_bands = [self.band10, self.band11, self.band12, self.band13,
            self.band14]
        self.qa1 = self.sd.select('QA_DataPlane').get()
        self.qa2 = self.sd.select('QA_DataPlane2').get()

    def lookup(self, latitude, longitude):
        """ Find the science data and QA flags for the nearest pixel to the
        given (geodetic) latitude and longitude.
        """
        i, j = self.proj.lookup_indices(latitude, longitude)
        ret = []
        for band, scale in zip(self.all_bands, self.scale_factors):
            ret.append(band[i,j] / scale)
        ret.extend([self.qa1[i,j], self.qa2[i,j]])
        return tuple(ret)


class AST08(object):
    """ Represent a Kinetic Temperature ASTER 08 Level 2 data product.
    """

    def __init__(self, filename, mode=SDC.READ):
        self.filename = filename
        self._open(mode)

    def _open(self, mode): # testing the line
        """ Open the HDF file for reading.
        """
        self.sd = SD(self.filename, mode)
        ds = self.sd.datasets()
        assert set(ds) == set(['KineticTemperature', 'GeodeticLatitude',
            'Longitude', 'QA_DataPlane', 'QA_DataPlane2'])

        pmd = parse_odl(self.sd.attributes()['productmetadata.0'])
        self.proj = UTMProjection(
            pmd.ASTERGDSGENERICMETADATA.SCENECOORDINATES.SCENECENTER.VALUE,
            self.sd.select('GeodeticLatitude').get(),
            self.sd.select('Longitude').get(),
            (700, 830),
        )
        self.scale_factor = pmd.ASTERGDSGENERICMETADATA.BANDSCALEFACTORS.VALUE[10]
        self.kt = self.sd.select('KineticTemperature').get()
        self.qa1 = self.sd.select('QA_DataPlane').get()
        self.qa2 = self.sd.select('QA_DataPlane2').get()

    def lookup(self, latitude, longitude):
        """ Find the science data and QA flags for the nearest pixel to the
        given (geodetic) latitude and longitude.
        """
        i, j = self.proj.lookup_indices(latitude, longitude)
        science = self.kt[i,j] / self.scale_factor
        return science, self.qa1[i,j], self.qa2[i,j]
