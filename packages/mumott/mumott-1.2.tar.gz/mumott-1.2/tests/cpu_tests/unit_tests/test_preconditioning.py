import pytest # noqa
import numpy as np

from scipy.spatial.transform import Rotation

from mumott.methods.projectors import SAXSProjectorBilinear
from mumott.methods.basis_sets import GaussianKernels
from mumott.core.geometry import Geometry, GeometryTuple
from mumott.methods.utilities import get_tensor_sirt_preconditioner, get_sirt_preconditioner, \
                                     get_tensor_sirt_weights, get_sirt_weights
from mumott.core.probed_coordinates import ProbedCoordinates


@pytest.fixture
def projector():
    r1 = Rotation.from_rotvec((0., 1.5, 0)).as_matrix()
    r2 = Rotation.from_rotvec((0., 0.5, 0)).as_matrix()
    tuple_list = [GeometryTuple(rotation=np.eye(3), j_offset=0., k_offset=0.),
                  GeometryTuple(rotation=r1, j_offset=0., k_offset=0.),
                  GeometryTuple(rotation=r2, j_offset=0., k_offset=0.)]
    geometry = Geometry()
    for t in tuple_list:
        geometry.append(t)
    geometry.volume_shape = np.array((2, 2, 2))
    geometry.projection_shape = np.array((3, 3))
    return SAXSProjectorBilinear(geometry)


@pytest.fixture
def basis_set():
    vec = np.arange(36.).reshape(3, 4, 1, 3)
    vec /= np.linalg.norm(vec, axis=-1)[..., None]
    pc = ProbedCoordinates(vector=vec)
    return GaussianKernels(probed_coordinates=pc, grid_scale=2)


def test_sirt_precon(projector):
    prc = get_sirt_preconditioner(projector)
    print(repr(prc))
    assert np.allclose(prc, 0.33333)


expect = np.array([[[[0.80798834, 7.58678368, 0.46601131, 0., 1.48291828,
                      0., 0., 3.46492309, 0., 6.34558506,
                      0.29732261, 3.70427564, 0.56490935, 0., 6.58046381,
                      0., 0.82330837, 4.90193263],
                     [0.80798834, 7.58678368, 0.46601131, 0., 1.48291828,
                      0., 0., 3.46492309, 0., 6.34558506,
                      0.29732261, 3.70427564, 0.56490935, 0., 6.58046381,
                      0., 0.82330837, 4.90193263]],
                    [[0.80798834, 7.58678368, 0.46601131, 0., 1.48291828,
                      0., 0., 3.46492309, 0., 6.34558506,
                      0.29732261, 3.70427564, 0.56490935, 0., 6.58046381,
                      0., 0.82330837, 4.90193263],
                     [0.80798834, 7.58678368, 0.46601131, 0., 1.48291828,
                      0., 0., 3.46492309, 0., 6.34558506,
                      0.29732261, 3.70427564, 0.56490935, 0., 6.58046381,
                      0., 0.82330837, 4.90193263]]],
                   [[[0.80798834, 7.58678368, 0.46601131, 0., 1.48291828,
                      0., 0., 3.46492309, 0., 6.34558506,
                      0.29732261, 3.70427564, 0.56490935, 0., 6.58046381,
                      0., 0.82330837, 4.90193263],
                     [0.80798834, 7.58678368, 0.46601131, 0., 1.48291828,
                      0., 0., 3.46492309, 0., 6.34558506,
                      0.29732261, 3.70427564, 0.56490935, 0., 6.58046381,
                      0., 0.82330837, 4.90193263]],
                    [[0.80798834, 7.58678368, 0.46601131, 0., 1.48291828,
                      0., 0., 3.46492309, 0., 6.34558506,
                      0.29732261, 3.70427564, 0.56490935, 0., 6.58046381,
                      0., 0.82330837, 4.90193263],
                     [0.80798834, 7.58678368, 0.46601131, 0., 1.48291828,
                      0., 0., 3.46492309, 0., 6.34558506,
                      0.29732261, 3.70427564, 0.56490935, 0., 6.58046381,
                      0., 0.82330837, 4.90193263]]]])


def test_tensor_sirt_precon(projector, basis_set):
    prc = get_tensor_sirt_preconditioner(projector, basis_set)
    print(repr(prc))
    assert np.allclose(prc, expect)


def test_sirt_wts(projector):
    prc = get_sirt_weights(projector, cutoff=1.)
    print(repr(prc))
    assert np.allclose(prc, 0.5)


expect_wts = np.array([[[[0.50370154, 0.51232442, 0.51097196, 0.50991338],
                         [0.50370154, 0.51232442, 0.51097196, 0.50991338],
                         [0.50370154, 0.51232442, 0.51097196, 0.50991338]],
                        [[0.50370154, 0.51232442, 0.51097196, 0.50991338],
                         [0.50370154, 0.51232442, 0.51097196, 0.50991338],
                         [0.50370154, 0.51232442, 0.51097196, 0.50991338]],
                        [[0.50370154, 0.51232442, 0.51097196, 0.50991338],
                         [0.50370154, 0.51232442, 0.51097196, 0.50991338],
                         [0.50370154, 0.51232442, 0.51097196, 0.50991338]]],
                       [[[0.50924457, 0.50879404, 0.50847217, 0.50823143],
                         [0.50924457, 0.50879404, 0.50847217, 0.50823143],
                         [0.50924457, 0.50879404, 0.50847217, 0.50823143]],
                        [[0.50924457, 0.50879404, 0.50847217, 0.50823143],
                         [0.50924457, 0.50879404, 0.50847217, 0.50823143],
                         [0.50924457, 0.50879404, 0.50847217, 0.50823143]],
                        [[0.50924457, 0.50879404, 0.50847217, 0.50823143],
                         [0.50924457, 0.50879404, 0.50847217, 0.50823143],
                         [0.50924457, 0.50879404, 0.50847217, 0.50823143]]],
                       [[[0.50804486, 0.50789613, 0.50777485, 0.5076741],
                         [0.50804486, 0.50789613, 0.50777485, 0.5076741],
                         [0.50804486, 0.50789613, 0.50777485, 0.5076741]],
                        [[0.50804486, 0.50789613, 0.50777485, 0.5076741],
                         [0.50804486, 0.50789613, 0.50777485, 0.5076741],
                         [0.50804486, 0.50789613, 0.50777485, 0.5076741]],
                        [[0.50804486, 0.50789613, 0.50777485, 0.5076741],
                         [0.50804486, 0.50789613, 0.50777485, 0.5076741],
                         [0.50804486, 0.50789613, 0.50777485, 0.5076741]]]])


def test_tensor_sirt_wts(projector, basis_set):
    prc = get_tensor_sirt_weights(projector, basis_set, cutoff=1)
    print(repr(prc))
    assert np.allclose(prc, expect_wts)
