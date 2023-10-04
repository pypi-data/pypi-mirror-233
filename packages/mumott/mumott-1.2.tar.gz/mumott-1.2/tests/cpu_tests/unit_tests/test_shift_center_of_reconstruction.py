import pytest
import numpy as np
from scipy.spatial.transform import Rotation
from mumott.core.geometry import Geometry, GeometryTuple
from mumott.pipelines.alignment import shift_center_of_reconstruction

geo_tuples = [GeometryTuple(rotation=np.eye(3), j_offset=0., k_offset=0.),
              GeometryTuple(rotation=Rotation.from_euler('y', np.pi/4).as_matrix(),
                            j_offset=0.,
                            k_offset=0.),
              GeometryTuple(rotation=Rotation.from_euler('z', np.pi/4).as_matrix(),
                            j_offset=0.,
                            k_offset=0.)]

results = [(-5.0, 3.0), (-1.4142, 5.6568), (-4.737615, 3.0)]


@pytest.mark.parametrize('geotup, results', (t for t in zip(geo_tuples, results)))
def test_geo_tuples(geotup, results):
    geo = Geometry()
    geo.append(geotup)
    shift_center_of_reconstruction(geo, shift_vector=(-5., 1.7, 3.))
    assert np.allclose(np.array((geo.j_offsets, geo.k_offsets)).ravel(), results)
