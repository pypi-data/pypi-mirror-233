import logging

import pytest
import numpy as np

from mumott.methods.projectors.saxs_projector_numba import SAXSProjectorNumba
from mumott.data_handling import DataContainer
from mumott.core.geometry import GeometryTuple


@pytest.fixture
def dc():
    return DataContainer('tests/test_half_circle.h5')


@pytest.fixture
def gm(dc):
    return dc.geometry


default_step_size = 1.0

gm_tuples = [GeometryTuple(rotation=np.eye(3), j_offset=0.2, k_offset=0.5),
             GeometryTuple(rotation=np.eye(3)[[2, 0, 1]], j_offset=0.2453, k_offset=0.5222),
             GeometryTuple(rotation=np.eye(3)[[1, 0, 2]], j_offset=-0.2453, k_offset=0.2)]

gm_hash_table = ['155882', '845567', '209690']

kernel_params = [dict(kernel_dimensions=(2, 2), kernel_width=(0.4, 1.2), kernel_type='bessel'),
                 dict(kernel_dimensions=(4, 7), kernel_width=(0.6, 0.2), kernel_type='gaussian'),
                 dict(kernel_dimensions=(3, 1), kernel_width=(0.1, 1.3), kernel_type='rectangular')]

kernel_density = [np.array(((0.25, 0.25), (0.25, 0.25))),
                  np.array([[0.00420072, 0.01253808, 0.02415652, 0.03005694,
                             0.02415652, 0.01253808, 0.00420072],
                           [0.01457805, 0.04351176, 0.08383206, 0.10430868,
                            0.08383206, 0.04351176, 0.01457805],
                           [0.01457805, 0.04351176, 0.08383206, 0.10430868,
                            0.08383206, 0.04351176, 0.01457805],
                           [0.00420072, 0.01253808, 0.02415652, 0.03005694,
                            0.02415652, 0.01253808, 0.00420072]]),
                  np.array([[1 / 3, 1 / 3, 1 / 3]])]
kernel_offsets = [np.array([-0.20100503, -0.20100503, 0.20100503, 0.20100503, -0.60301508,
                            0.60301508, -0.60301508, 0.60301508]),
                  np.array([-4.51127820e-01, -4.51127820e-01, -4.51127820e-01, -4.51127820e-01,
                            -4.51127820e-01, -4.51127820e-01, -4.51127820e-01, -1.50375940e-01,
                            -1.50375940e-01, -1.50375940e-01, -1.50375940e-01, -1.50375940e-01,
                            -1.50375940e-01, -1.50375940e-01, 1.50375940e-01, 1.50375940e-01,
                            1.50375940e-01, 1.50375940e-01, 1.50375940e-01, 1.50375940e-01,
                            1.50375940e-01, 4.51127820e-01, 4.51127820e-01, 4.51127820e-01,
                            4.51127820e-01, 4.51127820e-01, 4.51127820e-01, 4.51127820e-01,
                            -1.71673820e-01, -1.14449213e-01, -5.72246066e-02, 3.05311332e-18,
                            5.72246066e-02, 1.14449213e-01, 1.71673820e-01, -1.71673820e-01,
                            -1.14449213e-01, -5.72246066e-02, 3.05311332e-18, 5.72246066e-02,
                            1.14449213e-01, 1.71673820e-01, -1.71673820e-01, -1.14449213e-01,
                            -5.72246066e-02, 3.05311332e-18, 5.72246066e-02, 1.14449213e-01,
                            1.71673820e-01, -1.71673820e-01, -1.14449213e-01, -5.72246066e-02,
                            3.05311332e-18, 5.72246066e-02, 1.14449213e-01, 1.71673820e-01]),
                  np.array([-3.34448161e-02, 2.48689958e-18, 3.34448161e-02, 4.15667500e-17,
                            4.15667500e-17, 4.15667500e-17])]
kernel_hash = ['570373', '146088', '596834']

fields = [np.arange(128, dtype=float).reshape(4, 4, 4, 2)]

bad_field = [np.arange(72, dtype=float).reshape(4, 3, 3, 2)]

bad_field_projs = [np.array([[[[0., 0.],
                             [12., 14.5],
                             [22., 24.5],
                             [0., 0.]],
                            [[0., 0.],
                             [57., 59.5],
                             [67., 69.5],
                             [0., 0.]],
                            [[0., 0.],
                             [102., 104.5],
                             [112., 114.5],
                             [0., 0.]],
                            [[0., 0.],
                             [147., 149.5],
                             [157., 159.5],
                             [0., 0.]]]])]

projs = [np.array([[[[40., 44.],
                     [48., 52.],
                     [56., 60.],
                     [64., 68.]],
                    [[120., 123.],
                     [126., 129.],
                     [132., 135.],
                     [138., 141.]],
                    [[216., 219.],
                     [222., 225.],
                     [228., 231.],
                     [234., 237.]],
                    [[312., 315.],
                     [318., 321.],
                     [324., 327.],
                     [330., 333.]]]])]

adjs = [np.array([[[[40., 44.],
                 [48., 52.],
                 [56., 60.],
                 [64., 68.]],
                [[40., 44.],
                 [48., 52.],
                 [56., 60.],
                 [64., 68.]],
                [[40., 44.],
                 [48., 52.],
                 [56., 60.],
                 [64., 68.]],
                [[20., 22.],
                 [24., 26.],
                 [28., 30.],
                 [32., 34.]]],
               [[[120., 123.],
                 [126., 129.],
                 [132., 135.],
                 [138., 141.]],
                [[120., 123.],
                 [126., 129.],
                 [132., 135.],
                 [138., 141.]],
                [[120., 123.],
                 [126., 129.],
                 [132., 135.],
                 [138., 141.]],
                [[60., 61.5],
                 [63., 64.5],
                 [66., 67.5],
                 [69., 70.5]]],
               [[[216., 219.],
                 [222., 225.],
                 [228., 231.],
                 [234., 237.]],
                [[216., 219.],
                 [222., 225.],
                 [228., 231.],
                 [234., 237.]],
                [[216., 219.],
                 [222., 225.],
                 [228., 231.],
                 [234., 237.]],
                [[108., 109.5],
                 [111., 112.5],
                 [114., 115.5],
                 [117., 118.5]]],
               [[[312., 315.],
                 [318., 321.],
                 [324., 327.],
                 [330., 333.]],
                [[312., 315.],
                 [318., 321.],
                 [324., 327.],
                 [330., 333.]],
                [[312., 315.],
                 [318., 321.],
                 [324., 327.],
                 [330., 333.]],
                [[156., 157.5],
                 [159., 160.5],
                 [162., 163.5],
                 [165., 166.5]]]])]

bad_projs = [np.arange(24.).reshape(1, 4, 3, 2)]

bad_adjs = [np.array([[[[0., 1.],
                        [0., 0.],
                        [2., 3.],
                        [4., 5.]],
                       [[0., 1.],
                        [0., 0.],
                        [2., 3.],
                        [4., 5.]],
                       [[0., 1.],
                        [0., 0.],
                        [2., 3.],
                        [4., 5.]],
                       [[0., 0.5],
                        [0., 0.],
                        [1., 1.5],
                        [2., 2.5]]],
                      [[[6., 7.],
                        [0., 0.],
                        [8., 9.],
                        [10., 11.]],
                       [[6., 7.],
                        [0., 0.],
                        [8., 9.],
                        [10., 11.]],
                       [[6., 7.],
                        [0., 0.],
                        [8., 9.],
                        [10., 11.]],
                       [[3., 3.5],
                        [0., 0.],
                        [4., 4.5],
                        [5., 5.5]]],
                      [[[12., 13.],
                        [0., 0.],
                        [14., 15.],
                        [16., 17.]],
                       [[12., 13.],
                        [0., 0.],
                        [14., 15.],
                        [16., 17.]],
                       [[12., 13.],
                        [0., 0.],
                        [14., 15.],
                        [16., 17.]],
                       [[6., 6.5],
                        [0., 0.],
                        [7., 7.5],
                        [8., 8.5]]],
                      [[[18., 19.],
                        [0., 0.],
                        [20., 21.],
                        [22., 23.]],
                       [[18., 19.],
                        [0., 0.],
                        [20., 21.],
                        [22., 23.]],
                       [[18., 19.],
                        [0., 0.],
                        [20., 21.],
                        [22., 23.]],
                       [[9., 9.5],
                        [0., 0.],
                        [10., 10.5],
                        [11., 11.5]]]])]

kernels = ['bessel', 'rectangular', 'gaussian', 'asdf']
valid = [True, True, True, False]


@pytest.mark.parametrize('step_size, expected_value', [(0.5, 0.5),
                                                       (0.1, 0.1),
                                                       (1.5, None),
                                                       (-0.5, None)])
def test_step_size(step_size, expected_value, gm):
    if expected_value is None:
        with pytest.raises(ValueError, match=r".* step size .*"):
            pr = SAXSProjectorNumba(gm, step_size)
        with pytest.raises(ValueError, match=r".* step size .*"):
            pr = SAXSProjectorNumba(gm)
            pr.step_size = step_size
    else:
        pr = SAXSProjectorNumba(gm, step_size)
        assert np.isclose(pr.step_size, expected_value)
        pr = SAXSProjectorNumba(gm, default_step_size)
        pr.step_size = step_size
        assert np.isclose(pr.step_size, expected_value)


@pytest.mark.parametrize('gm_tuple, expected_value', [(g, h) for g, h in zip(gm_tuples, gm_hash_table)])
def test_gm_hash(gm_tuple, expected_value, gm):
    pr = SAXSProjectorNumba(gm, default_step_size)
    gm[0] = gm_tuple
    assert pr.is_dirty
    pr._update()
    assert expected_value == str(pr._geometry_hash)[:6]


@pytest.mark.parametrize('step_size, expected_value', [(1.0, '108699'),
                                                       (0.5, '211240')])
def test_hash(step_size, expected_value, gm):
    pr = SAXSProjectorNumba(gm, step_size)
    assert expected_value == str(hash(pr))[:6]


@pytest.mark.parametrize('kernel_pars, kernel_dens, kernel_offs, kernel_h',
                         [t for t in
                          zip(kernel_params, kernel_density, kernel_offsets, kernel_hash)])
def test_sampling_kernel(kernel_pars, kernel_dens, kernel_offs, kernel_h, gm, caplog):
    pr = SAXSProjectorNumba(gm, default_step_size)
    pr.create_sampling_kernel(**kernel_pars)
    assert np.allclose(kernel_dens, pr.sampling_kernel)
    assert np.allclose(kernel_offs, pr.kernel_offsets)
    assert kernel_h == str(hash(pr))[:6]


@pytest.mark.parametrize('kernel_pars', [k for k in kernel_params])
def test_kernel_warning(kernel_pars, caplog, gm):
    caplog.set_level(logging.WARNING)
    pr = SAXSProjectorNumba(gm)
    pr.create_sampling_kernel(**kernel_pars)
    pr.create_sampling_kernel(**kernel_pars)
    assert 'The old sampling kernel will be overwritten.' in caplog.text
    caplog.clear()
    caplog.set_level(logging.CRITICAL)
    pr.create_sampling_kernel(**kernel_pars)
    assert 'The old sampling kernel will be overwritten.' not in caplog.text


@pytest.mark.parametrize('field, proj', [f for f in zip(fields, projs)])
def test_forward(field, proj, gm):
    pr = SAXSProjectorNumba(gm, default_step_size)
    print(repr(pr.forward(field)))
    assert np.allclose(proj, pr.forward(field))


@pytest.mark.parametrize('field, proj', [f for f in zip(fields, projs)])
def test_forward_subset(field, proj, gm):
    gm.append(gm[0])
    pr = SAXSProjectorNumba(gm, default_step_size)
    p = pr.forward(field, indices=0)
    assert np.allclose(proj, p)
    with pytest.raises(TypeError, match='integer kind'):
        pr.forward(field, indices=np.array('abc'))


@pytest.mark.parametrize('field, expected', [f for f in zip(bad_field, bad_field_projs)])
def test_forward_failure(field, expected, gm):
    pr = SAXSProjectorNumba(gm)
    with pytest.raises(ValueError, match='volume shape expected'):
        pr.forward(field)
    gm.volume_shape = np.array(field.shape[:-1])
    proj = pr.forward(field)
    assert np.allclose(proj, expected)


@pytest.mark.parametrize('proj, adj', [f for f in zip(projs, adjs)])
def test_adj(proj, adj, gm):
    pr = SAXSProjectorNumba(gm)
    print(repr(pr.adjoint(proj)))
    assert np.allclose(adj, pr.adjoint(proj))


@pytest.mark.parametrize('proj, expected', [f for f in zip(bad_projs, bad_adjs)])
def test_adj_failure(proj, expected, gm):
    pr = SAXSProjectorNumba(gm)
    with pytest.raises(ValueError, match='projection shape expected'):
        pr.adjoint(proj)
    gm.projection_shape = np.array(proj.shape[1:-1])
    adj = pr.adjoint(proj)
    print(repr(adj))
    assert np.allclose(adj, expected)


@pytest.mark.parametrize('proj, adj', [f for f in zip(projs, adjs)])
def test_adj_subset(proj, adj, gm):
    gm.append(gm[0])
    pr = SAXSProjectorNumba(gm)
    assert np.allclose(adj, pr.adjoint(proj, indices=0,))
    with pytest.raises(TypeError, match='integer kind'):
        pr.adjoint(proj, indices=np.array('abc'))
    assert np.allclose(adj, pr.adjoint(proj[0], indices=0,))


@pytest.mark.parametrize('kernel, validity', [t for t in zip(kernels, valid)])
def test_kernel_type(kernel, validity, gm):
    pr = SAXSProjectorNumba(gm, default_step_size)
    if validity is True:
        pr.create_sampling_kernel(kernel_type=kernel)
    else:
        with pytest.raises(ValueError, match='.* kernel .*'):
            pr.create_sampling_kernel(kernel_type=kernel)


def test_str(gm):
    pr = SAXSProjectorNumba(gm)
    string = str(pr)
    assert '1d50c6' in string


def test_html(gm):
    pr = SAXSProjectorNumba(gm)
    html = pr._repr_html_()
    assert '1d50c6' in html
