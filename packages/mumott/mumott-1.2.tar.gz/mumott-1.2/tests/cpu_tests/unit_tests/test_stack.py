import pytest  # noqa
import numpy as np
from mumott.data_handling import DataContainer
from mumott.core.projection_stack import ProjectionStack, Projection
from mumott.core.geometry import GeometryTuple


def test_hashes():
    dc = DataContainer('tests/test_half_circle.h5')
    assert dc.projections[0].hash_data.startswith('ab1de1')
    assert dc.projections[0].hash_diode.startswith('dcf160')
    assert dc.projections[0].hash_weights.startswith('65e22e')
    assert dc.projections.hash_data.startswith('ab1de1')
    assert dc.projections.hash_diode.startswith('dcf160')
    assert dc.projections.hash_weights.startswith('65e22e')
    dc = DataContainer('tests/test_full_circle.h5')
    assert dc.projections[0].hash_data.startswith('3f0ba8')
    assert dc.projections[0].hash_diode.startswith('808328')
    assert dc.projections[0].hash_weights.startswith('088d39')
    assert dc.projections.hash_data.startswith('e6963d')
    assert dc.projections.hash_diode.startswith('cac85f')
    assert dc.projections.hash_weights.startswith('11457e')


def test_empty_hashes():
    s = ProjectionStack()
    assert s.hash_data.startswith('786a02')
    assert s.hash_diode.startswith('786a02')
    assert s.hash_weights.startswith('786a02')
    f = Projection()
    assert f.hash_data.startswith('786a02')
    assert f.hash_diode.startswith('786a02')
    assert f.hash_weights.startswith('786a02')
    s.append(f)
    assert s.hash_data.startswith('786a02')
    assert s.hash_diode.startswith('786a02')
    assert s.hash_weights.startswith('786a02')
    assert s[0].hash_data.startswith('786a02')
    assert s[0].hash_diode.startswith('786a02')
    assert s[0].hash_weights.startswith('786a02')


def test_append():
    projections = ProjectionStack()
    for i in range(5):
        f = Projection(diode=np.array((0.5, 1.5)).reshape(1, 2), j_offset=i)
        projections.append(f)
    assert np.allclose(projections[0].diode, (0.5, 1.5))
    f = Projection(diode=np.array((0.5, 1.5)).reshape(2, 1))

    with pytest.raises(ValueError, match='Appended'):
        projections.append(f)
    with pytest.raises(ValueError, match='New'):
        projections[0] = f
    with pytest.raises(ValueError, match='Inserted'):
        projections.insert(0, f)


def test_insert():
    projections = ProjectionStack()
    for i in range(5):
        f = Projection(j_offset=i)
        projections.append(f)
    f = Projection(j_offset=5)
    projections.insert(1, f)
    assert len(projections) == 6
    assert projections[1] == f
    assert projections[1].j_offset == 5
    assert projections[5].j_offset == 4


def test_setitem():
    projections = ProjectionStack()
    for i in range(5):
        f = Projection(j_offset=i,
                       inner_angle=float(i),
                       inner_axis=np.array((0, 1, 0)))
        projections.append(f)
    assert np.allclose(projections.geometry.inner_axes[0], (0, 1, 0))
    f = Projection(j_offset=5,
                   inner_angle=float(5),
                   inner_axis=np.array((0, 1, 0)))
    projections[1] = f
    projections[2].inner_axis = np.array((1, 0, 0))
    assert len(projections) == 5
    assert projections[1] == f
    assert projections[1].j_offset == 5
    assert projections[1].inner_angle == 5.
    assert projections[4].inner_angle == 4.
    assert projections[4].j_offset == 4
    assert np.allclose(projections[4].inner_axis, (0, 1, 0))
    assert np.allclose(projections[2].inner_axis, (1, 0, 0))
    assert projections[4].outer_axis is None
    assert projections.geometry._get_hashable_axes_and_angles()[3] is None


def test_attached():
    projections = ProjectionStack()
    for i in range(5):
        f = Projection(j_offset=i)
        projections.append(f)
    other_projections = ProjectionStack()
    with pytest.raises(ValueError, match='attached'):
        other_projections.append(f)
    other_projections.append(Projection())

    with pytest.raises(ValueError, match='attached'):
        other_projections[0] = f

    with pytest.raises(ValueError, match='attached'):
        other_projections.insert(0, f)

    del projections[4]
    other_projections.append(f)


def test_size():
    projections = ProjectionStack()
    for i in range(5):
        f = Projection(j_offset=i)
        projections.append(f)
    with pytest.raises(IndexError, match='bounds'):
        f = projections[5]
    with pytest.raises(IndexError, match='bounds'):
        f = projections[-6]


def test_str():
    dc = DataContainer('tests/test_half_circle.h5')
    projections = dc.projections
    s = projections._get_str_representation(5)
    assert s.count('\n') <= 6


def test_html():
    dc = DataContainer('tests/test_half_circle.h5')
    projections = dc.projections
    s = projections._get_html_representation(5)
    assert s.count('</tr>') <= 6


def test_set_projection_geo():
    f = Projection()
    g = GeometryTuple(rotation=np.ones(3), j_offset=0, k_offset=5)
    f.geometry = g
    assert np.allclose(f.rotation, g.rotation)
    assert np.allclose(f.j_offset, g.j_offset)
    assert np.allclose(f.k_offset, g.k_offset)
