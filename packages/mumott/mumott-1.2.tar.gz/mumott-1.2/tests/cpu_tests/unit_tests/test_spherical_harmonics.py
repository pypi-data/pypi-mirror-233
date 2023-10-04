import pytest
import logging
import numpy as np
from numpy import array

from mumott.methods.basis_sets import SphericalHarmonics
from mumott import ProbedCoordinates


@pytest.fixture
def default_pc():
    return ProbedCoordinates()


@pytest.fixture
def default_ell_max():
    return 2


@pytest.fixture
def s(default_ell_max, default_pc):
    return SphericalHarmonics(default_pc, default_ell_max)


LOGGER = logging.getLogger(__name__)

output_dictionary = {'basis_set': {
    'name': 'SphericalHarmonics',
    'coefficients': array([[10, 15,  7,  9,  3,  6]]),
    'ell_max': 2,
    'ell_indices': array([0, 2, 2, 2, 2, 2]),
    'emm_indices': array([0, -2, -1,  0,  1,  2]),
    'projection_matrix': array([[[[1., 0., -0., -1.11803399, -0., 1.93649167]]]]),
    'hash': '0x1fc6a9246a9f8dfb'},
    'spherical_functions':
    {'means': array([10]),
     'variances': array([400]),
     'eigenvectors': array([[[0.53554753,  0.64567032, -0.54433324],
                             [-0.83389412,  0.30245493, -0.46167263],
                             [0.13345204, -0.70116393, -0.70039967]]]),
     'r2_tensors': array([[3, -43,  40,  27,  11,  58]]),
     'tensor_to_matrix_indices': [[0, 5, 4], [5, 1, 3], [4, 3, 2]],
     'eigenvalues': array([[-84.56998002,  18.22384166,  66.34613836]]),
     'main_orientations': array([[[0.53554753],
                                  [-0.83389412],
                                  [0.13345204]]]),
     'main_orientation_symmetries': array([-0.43097661]),
     'normalized_standard_deviations': array([2]),
     'power_spectra': array([[100., 400.]]),
     'power_spectra_ell': array([0, 2])}}

default_coeffs = array((10, 15, 7, 9, 3, 6)).reshape(1, 6)

probed_coordinate_list = [ProbedCoordinates(vector=np.array((0., 1., 0)).reshape(1, 1, 1, 3)),
                          ProbedCoordinates(vector=np.array((0., 0.7, -0.7)).reshape(1, 1, 1, 3))]

pc_vector_list = [np.array((0., 1., 0.)).reshape(1, 1, 1, 3),
                  np.array((0., 0.7, -0.7)).reshape(1, 1, 1, 3)]

pc_hash_list = ['642022', '173557']

ell_max_list = [2, 4, 6]
expected_hashes = ['228970', '791168', '374938']


@pytest.mark.parametrize('ell_max, expected_ell, expected_emm', [(0, [0], [0]),
                                                                 (2,
                                                                  [0, 2, 2, 2, 2, 2],
                                                                  [0, -2, -1, 0, 1, 2])])
def test_ell_max(ell_max, expected_ell, expected_emm, default_pc):
    s = SphericalHarmonics(default_pc, ell_max)
    assert s.ell_max == ell_max
    assert np.allclose(s.ell_indices, expected_ell)
    assert np.allclose(s.emm_indices, expected_emm)


@pytest.mark.parametrize('ell_max,expected_matrix', [(0, [[[1]]]),
                                                     (2, [[[[1., 0., -0., -1.11803399, -0., 1.93649167]]]])])
def test_projection_matrix(ell_max, expected_matrix, default_pc):
    s = SphericalHarmonics(default_pc, ell_max)
    assert np.allclose(s.projection_matrix, expected_matrix)


def test_r2_ell0(caplog, default_pc):
    s = SphericalHarmonics(default_pc, 0)
    caplog.set_level(logging.INFO)
    r2, eve, ev = s._get_rank2_tensor_analysis(default_coeffs[..., 0])
    assert 'ell_max < 2' in caplog.text
    assert np.allclose(ev[..., 0], -1)
    assert np.allclose(ev[..., 1], 0)
    assert np.allclose(ev[..., 2], 1)


@pytest.mark.parametrize('coeffs, expected_dictionary', [
    (default_coeffs, output_dictionary)])
def test_output(coeffs, expected_dictionary, s):
    d = s.get_output(coeffs)
    for key, value in d['basis_set'].items():
        if type(value) is str:
            assert expected_dictionary['basis_set'][key] == value
        else:
            assert np.allclose(expected_dictionary['basis_set'][key], value)
    for key, value in d['spherical_functions'].items():
        if type(value) is str:
            assert expected_dictionary['spherical_functions'][key] == value
        elif key == 'eigenvectors':
            assert np.allclose(abs(np.einsum('...ik, ...ik -> ...k',
                                   expected_dictionary['spherical_functions'][key],
                                   value)), 1.)
        elif key == 'main_orientations':
            assert np.allclose((abs(np.einsum('...i, ...i -> ...',
                               expected_dictionary['spherical_functions'][key].squeeze(),
                               value.squeeze()))), 1.)
        else:
            assert np.allclose(expected_dictionary['spherical_functions'][key], value)


@pytest.mark.parametrize('coeffs, expected_result', [
    (default_coeffs, array([[11.55664414]]))])
def test_forward(coeffs, expected_result, s):
    r = s.forward(default_coeffs, np.array((0,)))
    assert np.allclose(r, expected_result)


@pytest.mark.parametrize('coeffs, expected_result', [
    (array([[11.55664414]]), array([[[11.55664414, 0., 0., -12.92072094, 0., 22.37934515]]]))])
def test_gradient(coeffs, expected_result, s):
    r = s.gradient(coeffs)
    assert np.allclose(r, expected_result)
    r = s.gradient(coeffs, np.array([0]))
    assert np.allclose(r, expected_result[0])


def test_covariances(s):
    p = s.get_inner_product(default_coeffs, default_coeffs)
    assert p == 500
    p = s.get_inner_product(default_coeffs, default_coeffs, spectral_moments=[2])
    assert p == 400
    p = s.get_inner_product(default_coeffs, default_coeffs, resolve_spectrum=True)
    assert np.allclose(p, (100, 400))


@pytest.mark.parametrize('pc, pc_vec, pc_hash', [
                         t for t in zip(probed_coordinate_list,
                                        pc_vector_list,
                                        pc_hash_list)])
def test_probed_coordinates(pc, pc_vec, pc_hash):
    s = SphericalHarmonics(pc)
    assert np.allclose(s.probed_coordinates.vector, pc_vec)
    assert str(hash(s.probed_coordinates))[:6] == pc_hash
    s = SphericalHarmonics()
    s.probed_coordinates.vector = pc_vec
    assert s.is_dirty
    s._update()
    assert not s.is_dirty
    assert np.allclose(s.probed_coordinates.vector, pc.vector)
    assert str(hash(s.probed_coordinates))[:6] == pc_hash
    assert str(s._probed_coordinates_hash)[:6] == pc_hash


@pytest.mark.parametrize('ell_max, expected_hash', [t for t in zip(ell_max_list, expected_hashes)])
def test_hash(ell_max, expected_hash):
    s = SphericalHarmonics(ell_max=ell_max)
    assert str(hash(s))[:6] == expected_hash
    old_pm = s._projection_matrix.copy()
    where = abs(s._projection_matrix) > 0
    s._projection_matrix[where] += abs(s._projection_matrix[where]).min() * 1e-8
    assert np.any(old_pm != s._projection_matrix)
    assert np.allclose(old_pm, s._projection_matrix)
    assert str(hash(s))[:6] == expected_hash
    s._projection_matrix = s._projection_matrix + s._projection_matrix.min() * 1e-4
    assert str(hash(s))[:6] != expected_hash


def test_str():
    s = SphericalHarmonics(ell_max=6)
    string = str(s)
    assert '5340c5' in string


def test_html():
    s = SphericalHarmonics(ell_max=6)
    html = s._repr_html_()
    assert '5340c5' in html


def test_set_ell_max():
    s = SphericalHarmonics(ell_max=6)
    s.ell_max = 8
    assert s.ell_max == 8
    with pytest.raises(ValueError, match='even'):
        s.ell_max = -5

    with pytest.raises(ValueError, match='even'):
        s.ell_max = 3

    with pytest.raises(ValueError, match='even'):
        s.ell_max = 1.5


def test_dict():
    s = SphericalHarmonics(ell_max=6)
    d = dict(s)
    assert str(d['hash'])[:6] == '5340c5'
