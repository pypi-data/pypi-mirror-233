import pytest  # noqa
import numpy as np

from mumott import DataContainer
from mumott.methods.residual_calculators import GradientResidualCalculator
from mumott.methods.basis_sets import SphericalHarmonics
from mumott.methods.projectors import SAXSProjectorNumba
from mumott import ProbedCoordinates


def test_class_structure():
    dc = DataContainer('tests/test_half_circle.h5')
    gm = dc.geometry
    s = str(gm)
    assert 'Geometry' in s

    pr = SAXSProjectorNumba(gm)
    s = str(pr)
    assert 'SAXSProjectorNumba' in s
    assert pr.is_dirty is False

    test_array = gm.k_direction_0.copy()
    gm.k_direction_0 = test_array
    assert np.allclose(gm.k_direction_0, test_array)

    assert pr.is_dirty is False
    test_array = np.array((0.5, 0.2, 0.1))
    gm.k_direction_0 = test_array

    assert pr.is_dirty is True
    assert np.allclose(gm.k_direction_0, test_array)

    pc = ProbedCoordinates()
    bs = SphericalHarmonics(pc)
    s = str(bs)
    assert 'SphericalHarmonics' in s

    method = GradientResidualCalculator(dc, bs, pr)
    s = str(method)
    assert 'GradientResidualCalculator' in s
