# -*- coding: utf-8 -*-
"""
Main module of the mumott package.
"""

import logging
import sys
from .core.numba_setup import numba_setup
from .core.geometry import Geometry
from .core.probed_coordinates import ProbedCoordinates
from .core.spherical_harmonic_mapper import SphericalHarmonicMapper
from .data_handling.data_container import DataContainer

__project__ = 'mumott'
__description__ = 'A module for analyzing tensor tomography experiments via Python'
__copyright__ = '2023'
__license__ = 'Mozilla Public License 2.0 (MPL 2.0)'
__version__ = '1.2'
__maintainer__ = 'The mumott developers team'
__status__ = 'Beta'
__url__ = 'https://mumott.org/'

__all__ = [
    'Geometry',
    'ProbedCoordinates',
    'DataContainer',
    'SphericalHarmonicMapper',
]

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)
numba_setup()
