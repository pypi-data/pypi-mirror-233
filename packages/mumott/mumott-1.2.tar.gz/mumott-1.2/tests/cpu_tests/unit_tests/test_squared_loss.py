import pytest  # noqa

import numpy as np
from mumott import DataContainer

from mumott.methods.basis_sets import SphericalHarmonics
from mumott.methods.projectors import SAXSProjectorNumba
from mumott.methods.residual_calculators import GradientResidualCalculator
from mumott.optimization.loss_functions import SquaredLoss

default_hash = '103d1e'


def test_get_residual_norm():
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    lf = SquaredLoss(meth)
    d = lf.get_residual_norm(get_gradient=False)
    assert np.isclose(d['residual_norm'], 7304.44)
    assert d['gradient'] is None

    d = lf.get_residual_norm(get_gradient=True)
    assert np.isclose(d['residual_norm'], 7304.44)
    assert np.allclose(d['gradient'][0, 0], [[-47.51], [-47.77], [-48.83], [-50.04]])

    dc.projections.weights *= 0.5
    lf = SquaredLoss(meth, use_weights=True)
    d = lf.get_residual_norm(get_gradient=False)
    assert np.isclose(d['residual_norm'], 3652.22)
    assert d['gradient'] is None

    d = lf.get_residual_norm(get_gradient=True)
    assert np.isclose(d['residual_norm'], 3652.22)
    assert np.allclose(d['gradient'][0, 0], [[-23.755], [-23.885], [-24.415], [-25.02]])

    lf.residual_norm_multiplier = 10
    d = lf.get_residual_norm(get_gradient=False)
    assert np.isclose(d['residual_norm'], 3652.22)

    lf.preconditioner = 0.5 * np.ones_like(meth.coefficients)
    lf.residual_norm_multiplier = 1
    d = lf.get_residual_norm(get_gradient=True)
    assert np.isclose(d['residual_norm'], 3652.22)
    assert np.allclose(d['gradient'][0, 0], np.array([[-23.755], [-23.885], [-24.415], [-25.02]]))

    lf.preconditioner = np.array((1, 2, 3))
    d = lf.get_residual_norm(get_gradient=True)


def test_get_loss():
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    lf = SquaredLoss(meth)
    d = lf.get_loss(get_gradient=False)
    assert np.isclose(d['loss'], 7304.44)
    assert d['gradient'] is None

    d = lf.get_loss(get_gradient=True)
    assert np.isclose(d['loss'], 7304.44)
    assert np.allclose(d['gradient'][0, 0], [[-47.51], [-47.77], [-48.83], [-50.04]])

    dc.projections.weights *= 0.5
    lf = SquaredLoss(meth, use_weights=False)
    d = lf.get_loss(get_gradient=False)
    assert np.isclose(d['loss'], 7304.44)

    lf = SquaredLoss(meth, use_weights=True)
    d = lf.get_loss(get_gradient=False)
    assert np.isclose(d['loss'], 3652.22)

    d = lf.get_loss(get_gradient=False)
    lf.residual_norm_multiplier = 10
    d = lf.get_loss(get_gradient=False)
    assert np.isclose(d['loss'], 36522.24)

    lf.preconditioner = 0.5 * np.ones_like(meth.coefficients)
    lf.residual_norm_multiplier = 1
    d = lf.get_loss(get_gradient=True)
    assert np.isclose(d['loss'], 3652.22)
    assert np.allclose(d['gradient'][0, 0], 0.5 * np.array([[-23.755], [-23.885], [-24.415], [-25.02]]))

    lf.preconditioner = np.array((1, 2, 3))
    with pytest.raises(ValueError, match='first three dimensions'):
        d = lf.get_loss(get_gradient=True)


def test_str():
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    lf = SquaredLoss(meth)
    s = str(lf)
    assert default_hash in s


def test_html():
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    lf = SquaredLoss(meth)
    h = lf._repr_html_()
    assert default_hash in h


def test_hash():
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    lf = SquaredLoss(meth, use_weights=True)
    assert hex(hash(lf))[2:8] == '11fc46'
    lf.use_weights = False
    assert hex(hash(lf))[2:8] == default_hash
    meth.coefficients += 1
    assert hex(hash(lf))[2:8] == '1ed6f4'
