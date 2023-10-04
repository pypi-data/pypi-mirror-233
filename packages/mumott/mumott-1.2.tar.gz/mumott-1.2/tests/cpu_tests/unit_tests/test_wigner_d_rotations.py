import numpy as np
from mumott.core import calculate_sph_coefficients_rotated_by_euler_angles, load_d_matrices
from mumott.core.wigner_d_utilities import (
    calculate_sph_coefficients_rotated_around_z,
    calculate_sph_coefficients_rotated_around_z_derived_wrt_the_angle,
    )

rotated_coeffs_expected = np.array([1., -0.18030734, 0.10651834, -0.11769562, -0.74725303,
                                    0.61959968, -0.2203116, 0.2799101, -0.09125825, -0.05911616,
                                    -0.29656749, 0.41471479, 0.31359554, -0.61883795, 0.34647819,
                                    -0.20868942, 0.36610613, -0.26654806, -0.02380877, 0.13614955,
                                    -0.01770037, 0.32023756, 0.12417254, -0.46785792, 0.05263752,
                                    0.41919305, -0.42769737, 0.18349328])


def test_loading():
    d = load_d_matrices(9)
    assert np.allclose(d[8]@d[8].T, np.identity(17))


def test_rotation():
    coeffs_test = np.array([1,
                            0, 0, 1, 0, 0,
                            0, 0, 0, 0, 1, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]).reshape((1, 1, 1, 28))

    coeffs_test = np.ones((2, 3, 3, 28)) * coeffs_test
    theta = 2.1
    phi = 3
    rotated_coeffs = calculate_sph_coefficients_rotated_by_euler_angles(coeffs_test, None, theta, phi)
    assert np.allclose(rotated_coeffs[0, 0, 0, :], rotated_coeffs_expected)


def test_differentiation():
    coeffs_test = np.array([1,
                            0, 0, 1, 0, 0,
                            0, 0, 0, 0, 1, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]).reshape((1, 1, 1, 28))

    coeffs_test = np.ones((2, 3, 3, 28)) * coeffs_test
    theta = 2.1
    phi = 3
    rotated_coeffs = calculate_sph_coefficients_rotated_by_euler_angles(coeffs_test, None, theta, phi)
    psi = 1
    del_psi = 0.01
    fd_deriv = calculate_sph_coefficients_rotated_around_z(rotated_coeffs,
                                                           np.ones((2, 3, 3)) * (psi+del_psi),
                                                           np.arange(0, 6+1, 2))
    fd_deriv -= calculate_sph_coefficients_rotated_around_z(rotated_coeffs,
                                                            np.ones((2, 3, 3)) * psi,
                                                            np.arange(0, 6+1, 2))
    fd_deriv = fd_deriv / del_psi
    analy_deriv = calculate_sph_coefficients_rotated_around_z_derived_wrt_the_angle(rotated_coeffs,
                                                                                    psi * np.ones((2, 3, 3)),
                                                                                    np.arange(0, 6+1, 2))
    assert np.allclose(fd_deriv, analy_deriv, atol=0.05, rtol=0.02)
