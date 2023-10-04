import pytest
import logging
import numpy as np
from numpy import array

from mumott.methods.basis_sets import TrivialBasis
from mumott import ProbedCoordinates

LOGGER = logging.getLogger(__name__)

default_coeffs = array((10, 15, 7, 9, 3, 6)).reshape(1, 6)

default_pc = ProbedCoordinates()

probed_coordinate_list = [ProbedCoordinates(vector=np.array((0., 1., 0)).reshape(1, 1, 1, 3)),
                          ProbedCoordinates(vector=np.array((0., 0.7, -0.7)).reshape(1, 1, 1, 3))]

pc_vector_list = [np.array((0., 1., 0.)).reshape(1, 1, 1, 3),
                  np.array((0., 0.7, -0.7)).reshape(1, 1, 1, 3)]

pc_hash_list = ['642022', '173557']

channels_list = [2, 4, 6]
expected_hashes = ['139402', '149136', '219323']


@pytest.mark.parametrize('channels,expected_matrix', [(0, np.eye(0)), (2, np.eye(2))])
def test_projection_matrix(channels, expected_matrix):
    s = TrivialBasis(channels)
    assert np.allclose(s.projection_matrix, expected_matrix)


def test_get_output():
    cf = np.arange(10).reshape(5, 2)
    s = TrivialBasis(2)
    d = s.get_output(cf)
    assert np.allclose(d['basis_set']['coefficients'], cf)


@pytest.mark.parametrize('channels, coeffs, expected_result', [
    (6, default_coeffs, default_coeffs)])
def test_forward(channels, coeffs, expected_result):
    s = TrivialBasis(channels)
    r = s.forward(default_coeffs, np.array((0,)))
    assert np.allclose(r, expected_result)


@pytest.mark.parametrize('channels, coeffs, expected_result', [
    (1, array([[11.55664414]]), array([[11.55664414]]))])
def test_gradient(channels, coeffs, expected_result):
    s = TrivialBasis(channels)
    r = s.gradient(coeffs)
    assert np.allclose(r, expected_result)
    r = s.gradient(coeffs, np.array([0]))
    assert np.allclose(r, expected_result[0])


@pytest.mark.parametrize('pc, pc_vec, pc_hash', [
                         t for t in zip(probed_coordinate_list,
                                        pc_vector_list,
                                        pc_hash_list)])
def test_probed_coordinates(pc, pc_vec, pc_hash):
    s = TrivialBasis()
    s.probed_coordinates.vector = pc_vec
    assert s.is_dirty
    s._update()
    assert not s.is_dirty
    assert np.allclose(s.probed_coordinates.vector, pc.vector)
    assert str(hash(s.probed_coordinates))[:6] == pc_hash
    assert str(s._probed_coordinates_hash)[:6] == pc_hash


@pytest.mark.parametrize('channels, expected_hash', [t for t in zip(channels_list, expected_hashes)])
def test_hash(channels, expected_hash):
    s = TrivialBasis(channels=channels)
    assert str(hash(s))[:6] == expected_hash


def test_str():
    s = TrivialBasis(channels=6)
    string = str(s)
    assert '1e6feb' in string


def test_html():
    s = TrivialBasis(channels=6)
    html = s._repr_html_()
    assert '1e6feb' in html
