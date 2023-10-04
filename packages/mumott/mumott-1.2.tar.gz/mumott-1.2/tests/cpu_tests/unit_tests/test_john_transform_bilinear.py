import pytest  # noqa:F401
import numpy as np

from mumott.data_handling import DataContainer
from mumott.core import john_transform_bilinear, john_transform_adjoint_bilinear

dc = DataContainer('tests/test_half_circle.h5')
gm = dc.geometry
fields = [np.arange(192, dtype=np.float64).reshape(4, 4, 4, 3)]
outs = [np.array([[[[72.,  76,  80],
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
                  [684, 688, 692]]]], dtype=np.float64)]

outs90 = [np.array([[[[288, 292, 296],
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
                      [468, 472, 476]]]], dtype=np.float64)]

out_fields = [np.arange(48)]
projs = [np.arange(48, dtype=np.float64).reshape(1, 4, 4, 3)]


@pytest.mark.parametrize('field,out', [t for t in zip(fields, outs)])
def test_john_transform_bilinear(field, out):
    vector_p = np.array([[0, 1., 0.]])
    vector_j = np.array([[1, 0., 0.]])
    vector_k = np.array([[0, 0., 1.]])
    offsets_j = np.zeros((len(gm)))
    offsets_k = np.zeros((len(gm)))
    projections = np.zeros_like(out).astype(np.float64)
    fun = john_transform_bilinear(field, projections, vector_p, vector_j, vector_k, offsets_j, offsets_k)
    fun(field, projections)
    print(projections)
    assert np.allclose(projections, out)


@pytest.mark.parametrize('field,out', [t for t in zip(fields, outs)])
def test_john_transform_bilinear_float32(field, out):
    vector_p = np.array([[0, 1., 0.]])
    vector_j = np.array([[1, 0., 0.]])
    vector_k = np.array([[0, 0., 1.]])
    offsets_j = np.zeros((len(gm)))
    offsets_k = np.zeros((len(gm)))
    projections = np.zeros_like(out).astype(np.float32)
    fun = john_transform_bilinear(field.astype(np.float32), projections,
                                  vector_p, vector_j,
                                  vector_k, offsets_j, offsets_k, 'float32')
    fun(field.astype(np.float32), projections)
    print(projections)
    assert np.allclose(projections, out)
    with pytest.raises(ValueError, match='float_type'):
        john_transform_bilinear(field, projections, vector_p, vector_j,
                                vector_k, offsets_j, offsets_k, np.float32)
    with pytest.raises(TypeError, match='projections.dtype'):
        john_transform_bilinear(field, projections.astype(np.float32), vector_p, vector_j,
                                vector_k, offsets_j, offsets_k)
    with pytest.raises(TypeError, match='field.dtype'):
        john_transform_bilinear(field.astype(np.float32), projections.astype(np.float64),
                                vector_p, vector_j,
                                vector_k, offsets_j, offsets_k)


@pytest.mark.parametrize('field,out', [t for t in zip(fields, outs90)])
def test_john_transform_bilinear90(field, out):
    vector_p = np.array([[1., 0., 0.]])
    vector_j = np.array([[0., 1., 0.]])
    vector_k = np.array([[0, 0., 1.]])
    offsets_j = np.zeros((len(gm)))
    offsets_k = np.zeros((len(gm)))
    projections = np.zeros_like(out).astype(np.float64)
    fun = john_transform_bilinear(field, projections, vector_p, vector_j, vector_k, offsets_j, offsets_k)
    fun(field, projections)
    print(projections)
    assert np.allclose(projections, out)


@pytest.mark.parametrize('proj,out', [t for t in zip(projs, out_fields)])
def test_john_transform_adjoint_bilinear(proj, out):
    vector_p = np.array([[0, 1., 0.]])
    vector_j = np.array([[1, 0., 0.]])
    vector_k = np.array([[0, 0., 1.]])
    offsets_j = np.zeros((len(gm)))
    offsets_k = np.zeros((len(gm)))
    field = np.zeros((4, 4, 4, 3,), dtype=np.float64)
    fun = john_transform_adjoint_bilinear(field, proj, vector_p, vector_j, vector_k, offsets_j, offsets_k)
    fun(field, proj)
    print(field)
    assert np.allclose(field[:, 0].ravel(), out)


@pytest.mark.parametrize('proj,out', [t for t in zip(projs, out_fields)])
def test_john_transform_adjoint_bilinear_float32(proj, out):
    vector_p = np.array([[0, 1., 0.]])
    vector_j = np.array([[1, 0., 0.]])
    vector_k = np.array([[0, 0., 1.]])
    offsets_j = np.zeros((len(gm)))
    offsets_k = np.zeros((len(gm)))
    field = np.zeros((4, 4, 4, 3,), dtype=np.float32)
    fun = john_transform_adjoint_bilinear(
              field, proj.astype(np.float32), vector_p, vector_j,
              vector_k, offsets_j, offsets_k, 'float32')
    fun(field, proj.astype(np.float32))
    print(field)
    assert np.allclose(field[:, 0].ravel(), out)
    with pytest.raises(ValueError, match='float_type'):
        john_transform_adjoint_bilinear(field, proj, vector_p, vector_j,
                                        vector_k, offsets_j, offsets_k, np.float32)
    with pytest.raises(TypeError, match='projections.dtype'):
        john_transform_adjoint_bilinear(field.astype(np.float64), proj.astype(np.float32),
                                        vector_p, vector_j,
                                        vector_k, offsets_j, offsets_k)
    with pytest.raises(TypeError, match='field.dtype'):
        john_transform_adjoint_bilinear(field.astype(np.float32), proj, vector_p, vector_j,
                                        vector_k, offsets_j, offsets_k)
