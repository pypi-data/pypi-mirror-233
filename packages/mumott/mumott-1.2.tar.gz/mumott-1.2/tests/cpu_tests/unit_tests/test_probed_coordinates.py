import pytest
import numpy as np

from mumott import ProbedCoordinates

vectors = [np.array((0.1, 1, 1), dtype=np.float64).reshape(1, 1, 1, 3),
           np.array((1, 2, 1), dtype=np.float64).reshape(1, 1, 1, 3)]

expected_r = [np.array((1.41774469)).reshape(1, 1, 1),
              np.array((2.44948974)).reshape(1, 1, 1)]

expected_theta = [np.array((0.78788574)).reshape(1, 1, 1),
                  np.array((1.15026199)).reshape(1, 1, 1)]

expected_phi = [np.array((1.47112767)).reshape(1, 1, 1),
                np.array((1.10714872)).reshape(1, 1, 1)]

expected_hash = ['109467', '220712']


@pytest.mark.parametrize('vector', [v for v in vectors])
def test_vector(vector):
    pc = ProbedCoordinates(vector)
    assert np.allclose(pc.vector, vector)
    pc = ProbedCoordinates
    pc.vector = vector
    assert np.allclose(pc.vector, vector)


@pytest.mark.parametrize('vector, exp_r, exp_theta, exp_phi', [t for t in zip(vectors,
                                                                              expected_r,
                                                                              expected_theta,
                                                                              expected_phi)])
def test_to_spherical(vector, exp_r, exp_theta, exp_phi):
    pc = ProbedCoordinates(vector)
    r, theta, phi = pc.to_spherical
    assert np.allclose(r, exp_r)
    assert np.allclose(theta, exp_theta)
    assert np.allclose(phi, exp_phi)


@pytest.mark.parametrize('vector, expected_hash', [t for t in zip(vectors, expected_hash)])
def test_hash(vector, expected_hash):
    pc = ProbedCoordinates(vector)
    assert expected_hash == str(hash(pc))[:6]
    # Should be rounded off by hash calculation
    pc.vector = vector + abs(vector) * 1e-8
    assert expected_hash == str(hash(pc))[:6]
    # Strict equality should fail
    assert np.all(vector != pc.vector)
    # Approximate equality should hold
    assert np.allclose(vector, pc.vector)
    pc.vector = vector + vector.min() * 1e-4
    assert str(hash(pc))[:6] != expected_hash
