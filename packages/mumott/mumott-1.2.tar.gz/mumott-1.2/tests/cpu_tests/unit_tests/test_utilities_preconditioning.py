import numpy as np
from mumott.methods.projectors.saxs_projector_numba import SAXSProjectorNumba
from mumott.methods.basis_sets.spherical_harmonics import SphericalHarmonics
from mumott.methods.utilities.preconditioning import get_largest_eigenvalue
from mumott.data_handling import DataContainer


def test_matrix_norm():
    geom = DataContainer('tests/test_half_circle.h5').geometry
    proj = SAXSProjectorNumba(geom)
    bs = SphericalHarmonics(ell_max=6)
    assert np.isclose(get_largest_eigenvalue(bs, proj, seed=0), 95.93905298060979)
