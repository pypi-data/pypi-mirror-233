import pytest # noqa
import numpy as np
from mumott.data_handling import DataContainer


def test_load():
    dc = DataContainer('tests/test_half_circle.h5')
    assert np.allclose(dc.data.shape, (1, 4, 4, 3))
    assert np.allclose(dc.weights.shape, (1, 4, 4, 3))
    assert np.allclose(dc.geometry.inner_axes, np.array((0., 0., -1.)))
    assert np.allclose(dc.geometry.outer_axes, np.array((1., 0., 0.)))
    old_gm = dc.geometry
    old_projection = dc.projections[0]
    dc = DataContainer('tests/test_half_circle.h5', skip_data=True)
    assert np.allclose(dc.diode.shape, (1, 4, 4))
    assert np.allclose(dc.weights.shape, (1, 4, 4))
    assert np.allclose(dc.geometry[0].rotation, old_gm[0].rotation)
    assert np.allclose(dc.geometry[0].j_offset, old_gm[0].j_offset)
    assert np.allclose(dc.geometry[0].k_offset, old_gm[0].k_offset)
    assert hash(dc.geometry) != hash(old_gm)
    old_gm.projection_shape = dc.geometry.projection_shape
    old_gm.detector_angles = dc.geometry.detector_angles
    assert hash(dc.geometry) == hash(old_gm)
    assert np.all(dc.projections[0].data == np.array([]).reshape(0, 0))
    assert np.allclose(dc.projections[0].diode, old_projection.diode)
    assert np.allclose(dc.projections[0].weights, old_projection.weights[..., 0])


def test_load_ragged():
    dc = DataContainer('tests/test_ragged.h5')
    for f in dc.projections:
        assert np.allclose(f.data.shape, (4, 4, 3))
        assert np.allclose(f.weights.shape, (4, 4, 3))
        assert np.allclose(f.geometry.inner_axis, np.array((0., 0., -1.)))
        assert np.allclose(f.geometry.outer_axis, np.array((1., 0., 0.)))
    for i, f in enumerate(dc.projections):
        if i > 0:
            assert np.allclose(f.weights[2:], 0.)
    dc = DataContainer('tests/test_ragged.h5', skip_data=True)
    for f in dc.projections:
        assert f.data.size == 0
        assert np.allclose(f.weights.shape, (4, 4, 3))
        assert np.allclose(f.geometry.inner_axis, np.array((0., 0., -1.)))
        assert np.allclose(f.geometry.outer_axis, np.array((1., 0., 0.)))
    for i, f in enumerate(dc.projections):
        if i > 0:
            assert np.allclose(f.weights[2:], 0.)


def test_load_rotvec():
    dc = DataContainer('tests/test_load_rotvec.h5')
    assert np.allclose(dc.geometry.rotations[0].ravel(),
                       [0.99886734, 0., 0.04758192, 0.,  1.,  0., -0.04758192, 0., 0.99886734])

    assert np.allclose(dc.geometry.inner_axes, np.array((0., 1., 0.)))
    assert np.allclose(dc.geometry.outer_axes, np.array((-1., 0., 0.)))
    assert np.isclose(dc.geometry.inner_angles[0], 0.0476)
    assert np.isclose(dc.geometry.outer_angles[0], 0.0)


new_diode = np.arange(16).reshape(1, 4, 4)
new_diode_list = [new_diode[0].copy()]


def test_set_diode():
    dc = DataContainer('tests/test_half_circle.h5')
    dc.projections.diode = new_diode
    assert np.allclose(dc.diode, new_diode)
    assert np.allclose(dc.projections[0].diode, new_diode[0])
    dc.projections.diode = new_diode_list
    assert np.allclose(dc.diode, new_diode_list)
    assert np.allclose(dc.projections[0].diode, new_diode_list[0])


def test_set_weights():
    dc = DataContainer('tests/test_half_circle.h5', skip_data=True)
    dc.projections.weights = new_diode
    assert np.allclose(dc.weights, new_diode)
    assert np.allclose(dc.projections[0].weights, new_diode[0])
    dc.projections.weights = new_diode_list
    assert np.allclose(dc.weights, new_diode_list)
    assert np.allclose(dc.projections[0].weights, new_diode_list[0])


def test_str():
    dc = DataContainer('tests/test_half_circle.h5')
    s = str(dc)
    assert s.count('\n') <= 50


def test_html():
    dc = DataContainer('tests/test_half_circle.h5')
    s = dc._repr_html_()
    assert s.count('</tr>') <= 25


def test_correct_for_transmission():
    dc = DataContainer('tests/test_half_circle.h5')
    dc.projections.diode = dc.diode * 0.5
    data = dc.projections.data
    dc.correct_for_transmission()
    assert np.allclose(data * 2, dc.projections.data)
    assert dc._correct_for_transmission_called


def test_get_str():
    dc = DataContainer('tests/test_half_circle.h5')
    s = dc._get_str_representation(5)
    assert s.count('\n') <= 6


def test_get_html():
    dc = DataContainer('tests/test_half_circle.h5')
    s = dc._get_html_representation(5)
    assert s.count('</tr>') <= 6


def test_loading_geometry_information():
    dc = DataContainer('tests/test_full_circle.h5')
    geom = dc.geometry
    assert np.allclose(geom.two_theta, 0.4363323129985824)
    assert np.allclose(geom.p_direction_0, np.array([0, 0, 1]))
    assert np.allclose(geom.j_direction_0, np.array([0, 1, 0]))
    assert np.allclose(geom.k_direction_0, np.array([1, 0, 0]))
    assert np.allclose(geom.detector_direction_origin, np.array([1, 0, 0]))
    assert np.allclose(geom.detector_direction_positive_90, np.array([0, 1, 0]))
