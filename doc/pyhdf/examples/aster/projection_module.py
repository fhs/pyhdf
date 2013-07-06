""" Tools for handling the projection of ASTER data.
"""

import numpy as np
from pyproj import Proj

__all__ = ['UTMProjection']


class UTMProjection(object):
    """ Handle the projection of ASTER data.
    """

    def __init__(self, center, geodetic_latitude, longitude, shape):
        # The (latitude, longitude) of the scene center.
        self.center = center

        # The (11, 11) array of the geodetic latitude at the coordinates of
        # a coarse grid over the scene.
        self.geodetic_latitude = geodetic_latitude

        # The (11, 11) array of the longitude at the coordinates of a coarse
        # grid over the scene.
        self.longitude = longitude

        # The shape of the whole scene.
        self.shape = shape

        # The transformation to and from the UTM projection.
        self.proj = Proj(proj='utm', lon_0=self.center[1], south=(self.center[0] < 0))

        # The UTM coordinates for each pixel.
        self.utmx, self.utmy = self._utm_pixels()

    def lookup_indices(self, latitude, longitude):
        """ Look up image indices with (geodetic) latitude and longitude.

        Parameters
        ----------
        latitude : float array
            The geodetic latitude in degrees.
        longitude : float array
            The longitude in degrees.

        Returns
        -------
        i : int array
        j : int array
            The nearest pixel coordinates of the query.
        """
        # TODO: allow arrays of inputs.
        # TODO: expensive!
        longitude = np.asarray(longitude)
        latitude = np.asarray(latitude)
        shape = latitude.shape
        assert shape == longitude.shape
        longitude = np.atleast_1d(longitude).flatten()
        latitude = np.atleast_1d(latitude).flatten()
        x, y = self.proj(longitude, latitude)
        d = np.hypot(x[:,np.newaxis]-self.utmx.flat, \
            y[:,np.newaxis]-self.utmy.flat)
        ij = d.argmin(axis=1)
        i = ij // self.shape[1]
        j = ij % self.shape[1]
        i.shape = shape
        j.shape = shape
        return i, j

    def _utm_pixels(self):
        """Create the UTM coordinates for each pixel
        through bilinear interpolation.
        """
        i, j = np.mgrid[0:self.shape[0], 0:self.shape[1]]
        di = self.shape[0] // (self.longitude.shape[0] - 1)
        dj = self.shape[1] // (self.longitude.shape[1] - 1)
        qi = i // di
        qi1 = qi + 1
        fi = (i % di).astype(float) / di
        fi1 = 1.0 - fi
        qj = j // dj
        qj1 = qj + 1
        fj = (j % dj).astype(float) / dj
        fj1 = 1.0 - fj
        cx, cy = self.proj(self.longitude, self.geodetic_latitude)
        x = cx[qi,qj]*fi1*fj1 + cx[qi1,qj]*fi*fj1 +\
            cx[qi,qj1]*fi1*fj + cx[qi1,qj1]*fi*fj
        y = cy[qi,qj]*fi1*fj1 + cy[qi1,qj]*fi*fj1 +\
            cy[qi,qj1]*fi1*fj + cy[qi1,qj1]*fi*fj
        return x, y
