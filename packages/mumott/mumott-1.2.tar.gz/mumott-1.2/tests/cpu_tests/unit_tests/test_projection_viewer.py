import pytest # noqa
from mumott.data_handling import DataContainer
from mumott.output_handling import ProjectionViewer


def test():
    dc = DataContainer('tests/test_half_circle.h5')
    p = ProjectionViewer(dc)
    p.change_projection(0)
