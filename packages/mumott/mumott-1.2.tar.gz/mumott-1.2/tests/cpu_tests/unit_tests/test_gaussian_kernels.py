import pytest
import logging
import numpy as np
from numpy import array

# robust imports to avoid having to update imports in tests in the future
from mumott.methods.basis_sets import GaussianKernels
from mumott.core.probed_coordinates import ProbedCoordinates
from mumott.core.spherical_harmonic_mapper import SphericalHarmonicMapper


@pytest.fixture
def default_pc():
    return ProbedCoordinates()


@pytest.fixture
def default_grid_scale():
    return 1


LOGGER = logging.getLogger(__name__)

output_dictionary = {'basis_set': {
    'name': 'GaussianKernels',
    'coefficients': array([[10, 15,  7,  9,  3,  6,  4,  1]]),
    'grid_scale': 1,
    'grid': (array([1.17809725, 1.17809725, 1.17809725, 1.17809725,
                    1.17809725, 1.17809725, 0.39269908, 0.39269908]),
             array([0.52359878, 5.75958653, 1.57079633, 4.71238898,
                    2.61799388, 3.66519143, 1.57079633, 4.71238898])),
    'kernel_scale_parameter': 1.0,
    'enforce_friedel_symmetry': True,
    'projection_matrix': array([[[0.22086663, 0.22086663, 0.01534498, 0.01534498,
                                  0.22086663, 0.22086663, 0.01620158, 0.01620158]]]),
    'hash': '0x1dd006132add98d5'},
    'spherical_harmonic_analysis': {
        'basis_set': {
            'name': 'SphericalHarmonics',
            'coefficients': array([[6.84521707, -0.12907381, -0.17674666,
                                    -1.19290282,  0.86693421, 0.04600325]]),
            'ell_max': 2,
            'ell_indices': array([0, 2, 2, 2, 2, 2]),
            'emm_indices': array([0, -2, -1,  0,  1,  2]),
            'projection_matrix': array([[[1., 0., -0., -1.11803399, -0.,  1.93649167]]]),
            'hash': '0x1fc6a9246a9f8dfb'},
        'spherical_functions': {
            'means': array([6.84521707]),
            'variances': array([2.22460778]),
            'eigenvectors': array([[[0.33319223,  0.35761505,  0.87240725],
                                   [-0.05279568,  0.9309034, -0.36142977],
                                   [-0.9413796,  0.07436626,  0.32905031]]]),
            'r2_tensors': array([[2.84558161,  2.48924196, -5.33482358,
                                  -0.68453688,  3.35762175, -0.49990071]]),
            'tensor_to_matrix_indices': [[0, 5, 4], [5, 1, 3], [4, 3, 2]],
            'eigenvalues': array([[-6.56161251,  2.24251554,  4.31909698]]),
            'main_orientations': array([[0.33319223, -0.05279568, -0.9413796]]),
            'main_orientation_symmetries': array([[-0.68352574]]),
            'normalized_standard_deviations': array([0.21789111]),
            'power_spectra': array([[46.85699668,  2.22460778]]),
            'power_spectra_ell': array([0, 2])
            }
        }
    }


default_coeffs = array((10, 15, 7, 9, 3, 6, 4, 1)).reshape(1, 8)

probed_coordinate_list = [ProbedCoordinates(vector=np.array((0., 1., 0)).reshape(1, 1, 1, 3)),
                          ProbedCoordinates(vector=np.array((0., 0.7, -0.7)).reshape(1, 1, 1, 3))]

pc_vector_list = [np.array((0., 1., 0.)).reshape(1, 1, 1, 3),
                  np.array((0., 0.7, -0.7)).reshape(1, 1, 1, 3)]

pc_hash_list = ['642022', '173557']

grid_scale_list = [2, 4, 6]
expected_hashes = ['243769', '163761', '965624']


@pytest.mark.parametrize('grid_scale, expected_len', [(0, 4),
                                                      (2, 8)])
def test_grid_scale(grid_scale, expected_len, default_pc):
    s = GaussianKernels(default_pc, grid_scale)
    assert s.grid_scale == grid_scale


@pytest.mark.parametrize('grid_scale, expected_matrix', [(0, np.array([[[0.31315763, 0.31315763]]])),
                                                         (1, np.array([[[0.22086663, 0.22086663,
                                                                        0.01534498, 0.01534498,
                                                                        0.22086663, 0.22086663,
                                                                        0.01620158, 0.01620158]]]))])
def test_projection_matrix(grid_scale, expected_matrix, default_pc):
    s = GaussianKernels(default_pc, grid_scale)
    assert np.allclose(s.projection_matrix, expected_matrix)


@pytest.mark.parametrize('coeffs, expected_dictionary', [
    (default_coeffs, output_dictionary)])
def test_output(coeffs, expected_dictionary, default_pc, default_grid_scale):
    s = GaussianKernels(default_pc, default_grid_scale)
    d = s.get_output(coeffs)
    print(repr(d))
    for key, value in d['basis_set'].items():
        if type(value) is str:
            assert expected_dictionary['basis_set'][key] == value
        else:
            assert np.allclose(expected_dictionary['basis_set'][key], value)
    for key, value in d['spherical_harmonic_analysis']['spherical_functions'].items():
        if type(value) is str:
            assert expected_dictionary['spherical_harmonic_analysis']['spherical_functions'][key] == value
        elif key == 'eigenvectors':
            assert np.allclose(
                abs(np.einsum('...ik, ...ik -> ...k',
                    expected_dictionary['spherical_harmonic_analysis']['spherical_functions'][key],
                    value)), 1.)
        elif key == 'main_orientations':
            assert np.allclose(
                (abs(np.einsum('...i, ...i -> ...',
                 expected_dictionary['spherical_harmonic_analysis']['spherical_functions'][key].squeeze(),
                 value.squeeze()))), 1.)
        else:
            assert np.allclose(
                expected_dictionary['spherical_harmonic_analysis']['spherical_functions'][key], value)


@pytest.mark.parametrize('coeffs, expected_result', [
    (default_coeffs, array([[7.8359929]]))])
def test_forward(coeffs, expected_result, default_pc, default_grid_scale):
    s = GaussianKernels(default_pc, default_grid_scale)
    r = s.forward(default_coeffs, np.array((0,)))
    assert np.allclose(r, expected_result)


@pytest.mark.parametrize('coeffs, expected_result', [
    (array([[7.8359929]]), array([[[1.73070935, 1.73070935, 0.12024314, 0.12024314,
                                    1.73070935, 1.73070935, 0.12695543, 0.12695543]]]))])
def test_gradient(coeffs, expected_result, default_pc, default_grid_scale):
    s = GaussianKernels(default_pc, default_grid_scale)
    r = s.gradient(coeffs)
    assert np.allclose(r, expected_result)
    r = s.gradient(coeffs, np.array([0]))
    assert np.allclose(r, expected_result[0])


def test_get_amplitudes(default_pc, default_grid_scale):
    s = GaussianKernels(default_pc, default_grid_scale)
    dh_grid_size = 5
    mapper = SphericalHarmonicMapper(ell_max=2, polar_resolution=dh_grid_size,
                                     azimuthal_resolution=dh_grid_size,
                                     enforce_friedel_symmetry=True)
    X, Y, Z = mapper.coordinates
    coordinates = np.concatenate((X[..., None], Y[..., None], Z[..., None]), axis=-1).reshape(1, -1, 1, 3)
    pc = ProbedCoordinates(coordinates)
    a = s.get_amplitudes(np.arange(len(s)), pc)
    assert np.allclose(a, array([4.94732689, 4.94732689, 4.94732689, 4.94732689, 4.94732689,
                                 4.35501828, 4.55395875, 3.2541336, 2.84648544, 3.90828001,
                                 2.49601168, 3.04988177, 2.81920269, 2.81920269, 3.04988177,
                                 2.78789956, 3.43801363, 4.15990153, 4.56754969, 4.08369237,
                                 4.94732689, 4.94732689, 4.94732689, 4.94732689, 4.94732689]))


@pytest.mark.parametrize('pc, pc_vec, pc_hash', [
                         t for t in zip(probed_coordinate_list,
                                        pc_vector_list,
                                        pc_hash_list)])
def test_probed_coordinates(pc, pc_vec, pc_hash):
    s = GaussianKernels(pc)
    assert np.allclose(s.probed_coordinates.vector, pc_vec)
    assert str(hash(s.probed_coordinates))[:6] == pc_hash
    s = GaussianKernels()
    s.probed_coordinates.vector = pc_vec
    assert s.is_dirty
    s._update()
    assert not s.is_dirty
    assert np.allclose(s.probed_coordinates.vector, pc.vector)
    assert str(hash(s.probed_coordinates))[:6] == pc_hash
    assert str(s._probed_coordinates_hash)[:6] == pc_hash


@pytest.mark.parametrize('grid_scale, expected_hash', [t for t in zip(grid_scale_list, expected_hashes)])
def test_hash(grid_scale, expected_hash, default_pc):
    s = GaussianKernels(grid_scale=grid_scale)
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
    s = GaussianKernels(grid_scale=6)
    string = str(s)
    assert 'd66964' in string


def test_html():
    s = GaussianKernels(grid_scale=6)
    html = s._repr_html_()
    assert 'd66964' in html


def test_set_grid_scale():
    s = GaussianKernels(grid_scale=6)
    assert len(s) == 98
    s.grid_scale = 8
    assert s.grid_scale == 8
    assert len(s) == 162
    with pytest.raises(ValueError, match='non-negative'):
        s.grid_scale = -5

    with pytest.raises(ValueError, match='non-negative'):
        s.grid_scale = 1.5


def test_set_kernel_scale_parameter():
    s = GaussianKernels(grid_scale=1)
    assert np.allclose(s.projection_matrix, [0.22086663, 0.22086663, 0.01534498, 0.01534498,
                                             0.22086663, 0.22086663, 0.01620158, 0.01620158])
    s.kernel_scale_parameter = 1.213414413
    assert s.kernel_scale_parameter == 1.213414413
    assert np.allclose(s.projection_matrix, [0.19613515, 0.19613515, 0.03225879, 0.03225879,
                                             0.19613515, 0.19613515, 0.03392352, 0.03392352])


def test_dict():
    s = GaussianKernels(grid_scale=6)
    d = dict(s)
    assert str(d['hash'])[:6] == 'd66964'
