import pytest  # noqa
import logging

import numpy as np
from mumott import DataContainer

from mumott.methods.basis_sets import SphericalHarmonics
from mumott.methods.projectors import SAXSProjectorNumba
from mumott.methods.residual_calculators import GradientResidualCalculator
from mumott.optimization.regularizers import Laplacian
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
    reg = Laplacian()
    lf.add_regularizer('laplacian', reg, 1e-2)
    test_dict = dict(test1=1, disp=False, test2=2, test3=123, maxiter=1)
    opt = LBFGS(lf, **test_dict)
    result = opt.optimize()
    assert 'Unknown option test1' in caplog.text
    assert np.isclose(result['fun'], 5507.07)
    assert np.isclose(result['nit'], 1)


def test_x0(caplog):
    caplog.set_level(logging.WARNING)
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    lf = SquaredLoss(meth)
    reg = Laplacian()
    lf.add_regularizer('laplacian', reg, 1e-1)
    test_dict = dict(disp=False, test1=2, test3=123, maxiter=1, x0=np.ones_like(lf.initial_values))
    opt = LBFGS(lf, **test_dict)
    result = opt.optimize()
    assert 'Unknown option test1' in caplog.text
    assert np.isclose(result['fun'], 3252.08)
    assert np.isclose(result['nit'], 1)


def test_hash(caplog):
    reg = Laplacian()
    assert hex(hash(reg))[2:8] == '1df556'
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    lf = SquaredLoss(meth)
    assert hex(hash(lf))[2:8] == '103d1e'
    reg = Laplacian()
    lf.add_regularizer('laplacian', reg, 1e-2)
    assert hex(hash(lf))[2:8] == '16a351'
    lf.regularization_weights['laplacian'] = 0.0005
    assert hex(hash(lf))[2:8] == '1ab0ea'


def add_remove_regularizers():
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    lf = SquaredLoss(meth)
    rf = Laplacian()
    lf.add_regularizer('laplacian', rf, 1e-2)
    assert 'laplacian' in lf.regularizers
    lf.remove_regularizer()
    assert 'laplacian' not in lf.regularizers


def test_str():
    reg = Laplacian()
    s = str(reg)
    assert '1df556' in s


def test_html():
    reg = Laplacian()
    s = reg._repr_html_()
    assert '1df556' in s
