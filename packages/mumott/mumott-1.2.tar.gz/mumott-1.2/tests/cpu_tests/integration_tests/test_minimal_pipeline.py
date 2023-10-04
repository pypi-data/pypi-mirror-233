import pytest # noqa
from io import StringIO
import logging
import numba
import numpy as np
from mumott.data_handling import DataContainer
from mumott.methods.basis_sets import SphericalHarmonics
from mumott.methods.projectors import SAXSProjectorNumba
from mumott.methods.residual_calculators import GradientResidualCalculator
from mumott.optimization.loss_functions import SquaredLoss
from mumott.optimization.optimizers import LBFGS


def test_minimal_pipeline():
    numba.config.NUMBA_NUM_THREADS = 1
    numba.set_num_threads(1)

    # check that the functionality for deleting projections works
    data_container = DataContainer(data_path='tests/test_half_circle.h5', data_type='h5')
    projections = data_container.projections
    assert len(projections) == 1
    del projections[0]
    assert len(projections) == 0

    # minimal check for append functionality
    dc1 = DataContainer(data_path='tests/test_half_circle.h5', data_type='h5')
    projections1 = dc1.projections
    dc2 = DataContainer(data_path='tests/test_half_circle.h5', data_type='h5')
    projections2 = dc2.projections
    assert len(projections1) == 1
    projection = projections2[0]
    del projections2[0]
    projections1.append(projection)
    assert len(projections1) == 2

    # minimal check for setitem functionality
    dc1 = DataContainer(data_path='tests/test_half_circle.h5', data_type='h5')
    dc2 = DataContainer(data_path='tests/test_half_circle.h5', data_type='h5')
    projection = dc2.projections[0]
    projection.j_offset = 1.243

    assert dc2.geometry.j_offsets[0] == 1.243

    dc2.geometry.k_offsets[0] = 4.214

    assert projection.k_offset == 4.214

    assert dc2.projections.geometry[0] == projection.geometry

    del dc2.projections[0]

    assert projection.j_offset == 1.243
    assert projection.k_offset == 4.214
    projection.data[0][0] = [1, 2, 3]
    dc1.projections[0] = projection

    assert np.all(dc1.projections[0].data[0][0] == [1, 2, 3])
    assert dc1.projections[0].j_offset == 1.243
    assert dc1.projections[0].k_offset == 4.214
    assert dc1.projections[0].geometry == dc1.projections.geometry[0]

    # load data container and check its basic output
    data_container = DataContainer(data_path='tests/test_half_circle.h5', data_type='h5')
    s = str(data_container)
    assert 'DataContainer' in s
    assert 'Corrected for transmission' in s
    assert 'Corrected for transmission' in s
    s = data_container._repr_html_()
    assert 'DataContainer' in s
    assert 'Corrected for transmission' in s
    assert 'Corrected for transmission' in s

    s = str(data_container.geometry)
    assert 'Geometry' in s
    s = data_container.geometry._repr_html_()
    assert 'Geometry' in s
    s = str(data_container.projections)
    assert 'ProjectionStack' in s
    s = data_container.projections._repr_html_()
    assert 'ProjectionStack' in s

    s = str(data_container.projections[0])
    assert 'Projection' in s
    assert 'diode' in s
    assert 'dcf160' in s
    s = data_container.projections[0]._repr_html_()
    assert 'Projection' in s
    assert 'diode' in s
    assert 'dcf160' in s

    bs = SphericalHarmonics(ell_max=6)
    pr = SAXSProjectorNumba(data_container.geometry)
    meth = GradientResidualCalculator(data_container, bs, pr)
    lf = SquaredLoss(meth)
    optimizer = LBFGS(lf, maxiter=5)
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    # - send logging to stream
    f = StringIO()
    logging.basicConfig(stream=f, level=logging.INFO)
    # run optimization
    optimizer.optimize()

    # check that coefficients are correct
    coeffs = meth.coefficients
    assert coeffs.size == 1792
    reference_coeffs = np.array(
        [0.87601399, 0.08113027, -0.00716787,  0.48052269, -0.15047219, 0.84963459,
         0.13741241, -0.01485878, 0.05635246, -0.00441374,  0.31243902, -0.09265587,
         0.5901497, -0.10334509, 0.71296326, 0.18458887, -0.01809086, 0.10050705,
         -0.01510339, 0.04192086, -0.00137633,  0.26808559, -0.02889264, 0.43901513,
         -0.10504635, 0.52148008, -0.07457155,  0.62865195, 0.88099492, 0.07854443,
         -0.01004529, 0.53877781, -0.21087649,  0.82255451, 0.1297739, -0.02188681,
         0.0632176, -0.00524503, 0.29931401, -0.11010673])

    print(coeffs.ravel()[:40])
    assert np.allclose(coeffs.ravel()[:40], reference_coeffs)
