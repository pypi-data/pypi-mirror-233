import pytest
import logging

import numpy as np
from mumott import DataContainer

from mumott.methods.basis_sets import SphericalHarmonics
from mumott.methods.projectors import SAXSProjectorNumba
from mumott.methods.residual_calculators import GradientResidualCalculator

LOGGER = logging.getLogger(__name__)

new_pc = np.array([[[0.93896659,  0.04472849, -0.34108812],
                   [0.9655966,   0.04599704, -0.25594428],
                   [0.98454023,  0.04689943, -0.16876307],
                   [0.99564669,  0.0474285, -0.08023846],
                   [0.99882756,  0.04758002,  0.00892486],
                   [0.99405752,  0.0473528,   0.09801714],
                   [0.98137455,  0.04674863,  0.18632918],
                   [0.9608796,   0.04577234,  0.273158],
                   [0.93273582,  0.04443168,  0.35781241],
                   [0.89716724,  0.04273734,  0.43961855],
                   [0.85445699,  0.0407028,   0.51792522]],
                  [[0.7996345,   0.03809129,  0.59927767],
                   [0.73106553,  0.03482494,  0.68141794],
                   [0.654119,    0.03115953,  0.75574957],
                   [0.56967665,  0.02713704,  0.82142078],
                   [0.47870616,  0.02280358,  0.87767899],
                   [0.38224998,  0.01820881,  0.92387953],
                   [0.28141345,  0.01340537,  0.95949297],
                   [0.17735209,  0.00844832,  0.9841112],
                   [0.07125838,  0.00339446,  0.99745211],
                   [-0.03565191, -0.00169831,  0.99936283],
                   [-0.14215364, -0.00677161,  0.98982144]],
                  [[-0.23837871, -0.01135538,  0.97110589],
                   [-0.32388788, -0.01542868,  0.94596966],
                   [-0.40681882, -0.01937917,  0.91330329],
                   [-0.48651138, -0.02317539,  0.8733668],
                   [-0.5623312, -0.02678714,  0.82647811],
                   [-0.63367473, -0.03018565,  0.77301045],
                   [-0.69997406, -0.03334387,  0.71338945],
                   [-0.76070142, -0.03623667,  0.64808969],
                   [-0.81537342, -0.03884102,  0.57763099],
                   [-0.86355485, -0.04113619,  0.5025742],
                   [-0.90486218, -0.0431039,   0.42351681]]])


@pytest.mark.parametrize('vec', [(np.array((0.2, 0.3, 0.7)))])
def test_probed_coordinates(vec):
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    old_pc = bs.probed_coordinates.vector
    meth = GradientResidualCalculator(dc, bs, pr)  # noqa
    dc.geometry.basis_vector_p = vec
    print(bs.probed_coordinates.vector)
    assert not np.allclose(old_pc, bs.probed_coordinates.vector)
    assert np.allclose(new_pc, bs.probed_coordinates.vector)
    assert np.allclose(bs.probed_coordinates.vector, meth.probed_coordinates)


def test_is_dirty():
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    old_hash = hash(meth)
    assert not meth.is_dirty
    dc.geometry.p_direction_0 = np.array((0, 0, 1))
    assert old_hash != hash(meth)
    old_hash = hash(meth)
    assert meth.is_dirty
    meth._update()
    assert old_hash != hash(meth)
    assert not meth.is_dirty


new_coeffs = [np.ones((4, 4, 4, 1)),
              np.ones((4, 4, 2, 1))]


@pytest.mark.parametrize('new_coeff, valid, myhash', [(new_coeffs[0], True, '666156'),
                                                      (new_coeffs[1], False, None)])
def test_coeff(new_coeff, valid, myhash):
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    if valid:
        old_hash = hash(meth)
        meth.coefficients = new_coeff
        assert old_hash != hash(meth)
        assert myhash == str(hash(meth))[:6]
        assert np.allclose(meth.coefficients, new_coeff)
    else:
        with pytest.raises(ValueError):
            meth.coefficients = new_coeff


def test_get_residuals():
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    old_hash = hash(meth)
    out = meth.get_residuals(True)
    residuals, gradient = (out['residuals'], out['gradient'])
    assert old_hash == hash(meth)
    val = np.array([-12.88, -14.4, -21.55])
    assert np.allclose(residuals[0, 0, 2], val)
    grad_slice = np.array([[-47.51],
                          [-47.77],
                          [-48.83],
                          [-50.04]])
    assert np.allclose(meth.get_residuals()['residuals'][0, 0, 2], val)
    assert np.allclose(grad_slice, gradient[0, 1])


def test_str():
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    s = str(meth)
    assert 'd44cdb' in s


def test_html():
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    h = meth._repr_html_()
    assert 'd44cdb' in h


def test_coeff_update(caplog):
    caplog.set_level(logging.WARNING)
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    dc.geometry.volume_shape = np.array((5, 4, 4))
    meth._update()
    assert 'truncated' in caplog.text
    assert np.allclose(meth.coefficients.shape[:-1], np.array((5, 4, 4)))
    caplog.clear()
    bs.ell_max = 2
    meth._update()
    assert 'truncated' in caplog.text
    assert 'Size of basis set' in caplog.text
    caplog.clear()
    assert np.allclose(meth.coefficients.shape, np.array((5, 4, 4, 6)))
    bs.ell_max = 0
    meth._update()
    assert 'truncated' in caplog.text
    assert np.allclose(meth.coefficients.shape, np.array((5, 4, 4, 1)))
