import pytest  # noqa
import logging

import numpy as np
from mumott import DataContainer

from mumott.methods.basis_sets import SphericalHarmonics
from mumott.methods.projectors import SAXSProjectorNumba
from mumott.methods.residual_calculators import GradientResidualCalculator
from mumott.optimization.regularizers import TotalVariation
from mumott.optimization.loss_functions import SquaredLoss
from mumott.optimization.optimizers import LBFGS

LOGGER = logging.getLogger(__name__)


def test_optimise(caplog):
    caplog.set_level(logging.WARNING)
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    lf = SquaredLoss(meth)
    reg = TotalVariation()
    lf.add_regularizer('tv', reg, 1e-2)
    test_dict = dict(test1=1, disp=False, test2=2, test3=123, maxiter=1)
    opt = LBFGS(lf, **test_dict)
    result = opt.optimize()
    assert 'Unknown option test1' in caplog.text
    assert np.isclose(result['fun'], 5507.02)
    assert np.isclose(result['nit'], 1)


def test_x0(caplog):
    caplog.set_level(logging.WARNING)
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    lf = SquaredLoss(meth)
    reg = TotalVariation()
    lf.add_regularizer('tv', reg, 1e-1)
    test_dict = dict(disp=False, test1=2, test3=123, maxiter=1, x0=np.ones_like(lf.initial_values))
    opt = LBFGS(lf, **test_dict)
    result = opt.optimize()
    assert 'Unknown option test1' in caplog.text
    assert np.isclose(result['fun'], 874.5143)
    assert np.isclose(result['nit'], 1)


def test_hash(caplog):
    reg = TotalVariation()
    assert hex(hash(reg))[2:8] == '1e0097'
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    lf = SquaredLoss(meth)
    assert hex(hash(lf))[2:8] == '103d1e'
    reg = TotalVariation()
    lf.add_regularizer('tv', reg, 1e-2)
    assert hex(hash(lf))[2:8] == '1aed21'
    lf.regularization_weights['tv'] = 0.0005
    assert hex(hash(lf))[2:8] == '11cbcc'


def test_str():
    reg = TotalVariation()
    s = str(reg)
    assert '1e0097' in s


def test_html():
    reg = TotalVariation()
    s = reg._repr_html_()
    assert '1e0097' in s
