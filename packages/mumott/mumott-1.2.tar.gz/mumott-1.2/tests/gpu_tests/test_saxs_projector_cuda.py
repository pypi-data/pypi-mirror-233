import pytest
import numpy as np

from numba import cuda

from mumott.methods.projectors.saxs_projector_cuda import SAXSProjectorCUDA
from mumott.data_handling import DataContainer
from mumott.core.geometry import GeometryTuple


@pytest.fixture
def dc():
    return DataContainer('tests/test_half_circle.h5')


@pytest.fixture
def gm(dc):
    gm = dc.geometry
    gm.rotations[0] = np.eye(3)
    return gm


@pytest.fixture
def gm_no_change(dc):
    gm = dc.geometry
    return gm


gm_tuples = [GeometryTuple(rotation=np.eye(3), j_offset=0.2, k_offset=0.5),
             GeometryTuple(rotation=np.eye(3)[[2, 0, 1]], j_offset=0.2453, k_offset=0.5222),
             GeometryTuple(rotation=np.eye(3)[[1, 0, 2]], j_offset=-0.2453, k_offset=0.2)]

gm_hash_table = ['155882', '845567', '209690']

kernel_hash = ['222572', '167889', '185810']

fields = [np.arange(192, dtype=np.float32).reshape(4, 4, 4, 3)]

test_projs = [np.array([[[[72.,  76,  80],
                          [84,  88,  92],
                          [96, 100, 104],
                          [108, 112, 116]],
                         [[264, 268, 272],
                          [276, 280, 284],
                          [288, 292, 296],
                          [300, 304, 308]],
                         [[456, 460, 464],
                          [468, 472, 476],
                          [480, 484, 488],
                          [492, 496, 500]],
                         [[648, 652, 656],
                          [660, 664, 668],
                          [672, 676, 680],
                          [684, 688, 692]]]], dtype=np.float32)]

test_projs90 = [np.array([[[[288, 292, 296],
                          [300, 304, 308],
                          [312, 316, 320],
                          [324, 328, 332]],
                         [[336, 340, 344],
                          [348, 352, 356],
                          [360, 364, 368],
                          [372, 376, 380]],
                         [[384, 388, 392],
                          [396, 400, 404],
                          [408, 412, 416],
                          [420, 424, 428]],
                         [[432, 436, 440],
                          [444, 448, 452],
                          [456, 460, 464],
                          [468, 472, 476]]]], dtype=np.float32)]

adjs = [np.arange(48)]
projs = [np.arange(48, dtype=np.float32).reshape(1, 4, 4, 3)]


@pytest.mark.parametrize('gm_tuple, expected_value', [(g, h) for g, h in zip(gm_tuples, gm_hash_table)])
def test_gm_hash(gm_tuple, expected_value, gm):
    dc = DataContainer('tests/test_half_circle.h5')
    geom = dc.geometry
    pr = SAXSProjectorCUDA(geom)
    geom[0] = gm_tuple
    assert pr.is_dirty
    pr._update()
    assert expected_value == str(pr._geometry_hash)[:6]


@pytest.mark.parametrize('field, proj', [f for f in zip(fields, test_projs)])
def test_forward(field, proj, gm):
    pr = SAXSProjectorCUDA(gm)
    p = pr.forward(field)
    assert np.allclose(proj, p)


@pytest.mark.parametrize('field, proj', [f for f in zip(fields, test_projs)])
def test_forward_repeat(field, proj, gm):
    pr = SAXSProjectorCUDA(gm)
    assert hex(hash(pr))[2:8] == '191b19'
    p = pr.forward(field)
    assert np.allclose(proj, p)
    assert hex(hash(pr))[2:8] == '51a7e4'
    p = pr.forward(field)
    assert np.allclose(proj, p)
    assert hex(hash(pr))[2:8] == '51a7e4'
    field_limited = np.ascontiguousarray(field[..., 1:])
    p = pr.forward(field_limited)
    assert np.allclose(proj[..., 1:], p)
    assert hex(hash(pr))[2:8] == '128a69'


@pytest.mark.parametrize('field, proj', [f for f in zip(fields, test_projs90)])
def test_forward90(field, proj, gm):
    pr = SAXSProjectorCUDA(gm)
    gm.j_direction_0 = np.array((0., 1., 0.))
    gm.p_direction_0 = np.array((1., 0., 0.))
    p = pr.forward(field)
    assert np.allclose(proj, p)


@pytest.mark.parametrize('field,', [f for f in fields])
def test_forward_failure(field, gm):
    gm.volume_shape = np.array((1, 1, 1))
    pr = SAXSProjectorCUDA(gm)
    with pytest.raises(ValueError, match='volume shape expected'):
        pr.forward(field)


@pytest.mark.parametrize('field, proj', [f for f in zip(fields, test_projs)])
def test_forward_subset(field, proj, gm):
    gm.append(gm[0])
    pr = SAXSProjectorCUDA(gm)
    p = pr.forward(field, indices=0)
    assert np.allclose(proj, p)
    with pytest.raises(TypeError, match='integer kind'):
        pr.forward(field, indices=np.array('abc'))


@pytest.mark.parametrize('proj, adj', [f for f in zip(projs, adjs)])
def test_adj(proj, adj, gm):
    pr = SAXSProjectorCUDA(gm)
    a = pr.adjoint(proj)
    assert np.allclose(adj, a[:, 0].ravel())


@pytest.mark.parametrize('proj', [f for f in projs])
def test_adj_failure(proj, gm):
    gm.projection_shape = np.array((1, 1))
    pr = SAXSProjectorCUDA(gm)
    with pytest.raises(ValueError, match='projection shape expected'):
        pr.adjoint(proj)


@pytest.mark.parametrize('proj, adj', [f for f in zip(projs, adjs)])
def test_adj_subset(proj, adj, gm):
    gm.append(gm[0])
    pr = SAXSProjectorCUDA(gm)
    a = pr.adjoint(proj, indices=0)
    assert np.allclose(adj, a[:, 0].ravel())


@pytest.mark.parametrize('field, proj', [f for f in zip(fields, test_projs)])
def test_device_forward(field, proj, gm):
    pr = SAXSProjectorCUDA(gm)
    p = pr.forward(cuda.to_device(field))
    assert np.allclose(proj, p.copy_to_host())


@pytest.mark.parametrize('proj, adj', [f for f in zip(projs, adjs)])
def test_device_adj(proj, adj, gm):
    pr = SAXSProjectorCUDA(gm)
    a = pr.adjoint(cuda.to_device(proj))
    print(a)
    assert np.allclose(adj, a.copy_to_host()[:, 0].ravel())


def test_str(gm_no_change):
    pr = SAXSProjectorCUDA(gm_no_change)
    string = str(pr)
    assert '1635b5' in string


def test_html(gm_no_change):
    pr = SAXSProjectorCUDA(gm_no_change)
    html = pr._repr_html_()
    assert '1635b5' in html
