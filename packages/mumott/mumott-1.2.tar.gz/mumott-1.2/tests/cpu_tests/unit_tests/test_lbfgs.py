import pytest  # noqa
import logging

import numpy as np
from mumott import DataContainer

from mumott.methods.basis_sets import SphericalHarmonics
from mumott.methods.projectors import SAXSProjectorNumba
from mumott.methods.residual_calculators import GradientResidualCalculator
from mumott.optimization.loss_functions import SquaredLoss
from mumott.optimization.optimizers import LBFGS

LOGGER = logging.getLogger(__name__)


def test_dict(caplog):
    caplog.set_level(logging.INFO)
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    lf = SquaredLoss(meth)
    test_dict = dict(test1=1, disp=False, test2=2, test3=123)
    opt = LBFGS(lf, **test_dict)
    for key, value in test_dict.items():
        assert np.allclose(opt[key], value)
    d = dict(opt)
    for key, value in test_dict.items():
        assert np.allclose(d[key], value)
    opt['test5'] = 100
    assert opt['test5'] == 100
    print(caplog.text)
    assert 'Key test5 added' in caplog.text


def test_optimise(caplog):
    caplog.set_level(logging.WARNING)
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    lf = SquaredLoss(meth)
    test_dict = dict(test1=1, disp=False, test2=2, test3=123, maxiter=1)
    opt = LBFGS(lf, **test_dict)
    result = opt.optimize()
    assert 'Unknown option test1' in caplog.text
    assert np.isclose(result['fun'], 5506.90)
    assert np.isclose(result['nit'], 1)


def test_x0(caplog):
    caplog.set_level(logging.WARNING)
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    lf = SquaredLoss(meth)
    test_dict = dict(disp=False, test1=2, test3=123, maxiter=1, x0=np.ones_like(lf.initial_values))
    opt = LBFGS(lf, **test_dict)
    result = opt.optimize()
    assert 'Unknown option test1' in caplog.text
    assert np.isclose(result['fun'], 3240.44)
    assert np.isclose(result['nit'], 1)


def test_hash(caplog):
    caplog.set_level(logging.WARNING)
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    lf = SquaredLoss(meth)
    test_dict = dict(test1=1, test2=2, test3=123, maxiter=1)
    opt = LBFGS(lf)
    assert hex(hash(opt))[2:8] == '9ff51a'
    for key, value in test_dict.items():
        opt[key] = value
    assert hex(hash(opt))[2:8] == '17685b'


def test_str():
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    lf = SquaredLoss(meth)
    test_dict = dict(test1=1, test2=2, test3=123, maxiter=1)
    opt = LBFGS(lf, **test_dict)
    s = str(opt)
    assert '17685b' in s
    assert 'maxiter' in s
    assert 'test1' in s


def test_html():
    dc = DataContainer('tests/test_half_circle.h5')
    bs = SphericalHarmonics()
    pr = SAXSProjectorNumba(dc.geometry)
    meth = GradientResidualCalculator(dc, bs, pr)
    lf = SquaredLoss(meth)
    test_dict = dict(test1=1, test2=2, test3=123, maxiter=1)
    opt = LBFGS(lf, **test_dict)
    s = opt._repr_html_()
    assert '17685b' in s
    assert 'maxiter' in s
    assert 'test1' in s
