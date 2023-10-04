import pytest # noqa
import numpy as np
from mumott.pipelines import run_mitra, run_sirt, run_sigtt, run_cross_correlation_alignment
from mumott.data_handling import DataContainer
from mumott.methods.projectors import SAXSProjectorBilinear
from mumott.methods.residual_calculators import GradientResidualCalculator
from mumott.methods.basis_sets import SphericalHarmonics, GaussianKernels, TrivialBasis
from mumott.optimization.loss_functions import SquaredLoss, HuberLoss
from mumott.optimization.regularizers import Laplacian, L1Norm
from mumott.optimization.optimizers import GradientDescent, LBFGS


@pytest.fixture
def data_container():
    return DataContainer('tests/test_half_circle.h5')


def test_mitra(data_container):
    result = run_mitra(data_container, maxiter=2)
    assert result['result']['loss'] == 0
    assert isinstance(result['basis_set'], TrivialBasis)
    assert result['projector']._geometry == data_container.geometry
    assert result['basis_set'].channels == 1
    result = run_mitra(data_container, use_absorbances=False, maxiter=2)
    assert result['projector']._geometry == data_container.geometry
    assert np.isclose(result['result']['loss'], 1305.527593)
    assert isinstance(result['projector'], SAXSProjectorBilinear)
    assert isinstance(result['residual_calculator'], GradientResidualCalculator)
    assert isinstance(result['basis_set'], GaussianKernels)
    assert isinstance(result['loss_function'], SquaredLoss)
    assert isinstance(result['optimizer'], GradientDescent)


def test_mitra_kwargs(data_container):
    result = run_mitra(data_container,
                       maxiter=3,
                       absorbances=data_container.diode,
                       use_absorbances=False,
                       projector=SAXSProjectorBilinear,
                       BasisSet=SphericalHarmonics,
                       basis_set_kwargs=dict(ell_max=2),
                       ResidualCalculator=GradientResidualCalculator,
                       residual_calculator_kwargs=dict(use_scalar_projections=False,
                                                       scalar_projections=data_container.diode[..., None]),
                       Regularizers=[dict(name='l1', regularizer=L1Norm(), regularization_weight=1e-3)],
                       LossFunction=HuberLoss,
                       loss_function_kwargs=dict(delta=1e2),
                       Optimizer=GradientDescent,
                       optimizer_kwargs=dict(ftol=1e-1))
    assert isinstance(result['projector'], SAXSProjectorBilinear)
    assert result['projector']._geometry == data_container.geometry
    assert isinstance(result['residual_calculator'], GradientResidualCalculator)
    assert isinstance(result['basis_set'], SphericalHarmonics)
    assert result['basis_set'].ell_max == 2
    assert not result['residual_calculator']._use_scalar_projections
    assert isinstance(result['loss_function'].regularizers['l1'], L1Norm)
    assert isinstance(result['loss_function'], HuberLoss)
    assert np.isclose(result['loss_function']._delta, 1e2)
    assert isinstance(result['optimizer'], GradientDescent)
    assert np.isclose(result['optimizer']['ftol'], 1e-1)
    assert np.isclose(result['result']['loss'], 10.10538)


def test_sirt(data_container):
    result = run_sirt(data_container, maxiter=2)
    assert result['result']['loss'] == 0
    assert isinstance(result['basis_set'], TrivialBasis)
    assert result['projector']._geometry == data_container.geometry
    assert result['basis_set'].channels == 1
    result = run_sirt(data_container, use_absorbances=False, maxiter=2)
    assert result['projector']._geometry == data_container.geometry
    assert np.isclose(result['result']['loss'], 1244.5244)
    assert isinstance(result['projector'], SAXSProjectorBilinear)
    assert isinstance(result['residual_calculator'], GradientResidualCalculator)
    assert isinstance(result['basis_set'], GaussianKernels)
    assert isinstance(result['loss_function'], SquaredLoss)
    assert isinstance(result['optimizer'], GradientDescent)


def test_sirt_kwargs(data_container):
    result = run_sirt(data_container,
                      maxiter=3,
                      absorbances=data_container.diode,
                      use_absorbances=False,
                      projector=SAXSProjectorBilinear,
                      ResidualCalculator=GradientResidualCalculator)
    assert isinstance(result['projector'], SAXSProjectorBilinear)
    assert result['projector']._geometry == data_container.geometry
    assert isinstance(result['residual_calculator'], GradientResidualCalculator)
    assert isinstance(result['basis_set'], GaussianKernels)
    assert isinstance(result['optimizer'], GradientDescent)
    assert np.isclose(result['result']['loss'], 850.455989)


def test_sigtt_kwargs(data_container):
    result = run_sigtt(data_container,
                       maxiter=3,
                       Projector=SAXSProjectorBilinear,
                       BasisSet=SphericalHarmonics,
                       basis_set_kwargs=dict(ell_max=4),
                       ResidualCalculator=GradientResidualCalculator,
                       residual_calculator_kwargs=dict(use_scalar_projections=False,
                                                       scalar_projections=data_container.diode[..., None]),
                       Regularizers=[dict(name='l1', regularizer=L1Norm(), regularization_weight=1e-3)],
                       LossFunction=HuberLoss,
                       loss_function_kwargs=dict(delta=1e2),
                       Optimizer=GradientDescent,
                       optimizer_kwargs=dict(ftol=1e-1))
    assert isinstance(result['projector'], SAXSProjectorBilinear)
    assert result['projector']._geometry == data_container.geometry
    assert isinstance(result['residual_calculator'], GradientResidualCalculator)
    assert isinstance(result['basis_set'], SphericalHarmonics)
    assert result['basis_set'].ell_max == 4
    assert not result['residual_calculator']._use_scalar_projections
    assert isinstance(result['loss_function'].regularizers['l1'], L1Norm)
    assert isinstance(result['loss_function'], HuberLoss)
    assert np.isclose(result['loss_function']._delta, 1e2)
    assert isinstance(result['optimizer'], GradientDescent)
    assert np.isclose(result['optimizer']['ftol'], 1e-1)
    assert np.isclose(result['result']['loss'], 8.2179718)


def test_sigtt(data_container):
    result = run_sigtt(data_container)
    assert np.isclose(result['result']['fun'], 22.14755)
    assert isinstance(result['projector'], SAXSProjectorBilinear)
    assert result['projector']._geometry == data_container.geometry
    assert isinstance(result['residual_calculator'], GradientResidualCalculator)
    assert isinstance(result['basis_set'], SphericalHarmonics)
    assert isinstance(result['loss_function'], SquaredLoss)
    assert isinstance(result['loss_function'].regularizers['laplacian'], Laplacian)
    assert isinstance(result['optimizer'], LBFGS)
    assert result['basis_set'].ell_max == 2


def test_alignment_upsampled(data_container, caplog):
    data_container.geometry.j_offsets[0] = 0.534
    data_container.geometry.k_offsets[0] = -0.754
    data_container.projections[0].diode = np.arange(16.).reshape(4, 4)
    run_cross_correlation_alignment(data_container, use_gpu=True,
                                    reconstruction_pipeline_kwargs=dict(maxiter=1,
                                                                        use_absorbances=True),
                                    maxiter=2, shift_tolerance=0.001, upsampling=20, relative_sample_size=1.,
                                    relaxation_weight=0., center_of_mass_shift_weight=0.)
    print(data_container.geometry.j_offsets, data_container.geometry.k_offsets)
    assert np.allclose(data_container.geometry.j_offsets, 0.60658623)
    assert np.allclose(data_container.geometry.k_offsets, -0.260367134)
    with pytest.raises(ValueError, match='align_j and align_k'):
        run_cross_correlation_alignment(data_container, align_j=False, align_k=False)


def test_alignment(data_container, caplog):
    data_container.geometry.j_offsets[0] = 0.534
    data_container.geometry.k_offsets[0] = -0.754
    data_container.projections[0].diode = np.arange(16.).reshape(4, 4)
    run_cross_correlation_alignment(data_container, use_gpu=True,
                                    reconstruction_pipeline_kwargs=dict(maxiter=1,
                                                                        use_absorbances=False),
                                    maxiter=2, shift_tolerance=0.001, upsampling=20, relative_sample_size=1.,
                                    relaxation_weight=0., center_of_mass_shift_weight=0.)
    print(data_container.geometry.j_offsets, data_container.geometry.k_offsets)
    assert np.allclose(data_container.geometry.j_offsets, 0.406994830)
    assert np.allclose(data_container.geometry.k_offsets, -0.314137704)


def test_alignment_no_k(data_container, caplog):
    data_container.geometry.j_offsets[0] = 0.534
    data_container.geometry.k_offsets[0] = -0.754
    data_container.projections[0].diode = np.arange(16.).reshape(4, 4)
    run_cross_correlation_alignment(data_container, use_gpu=True,
                                    reconstruction_pipeline_kwargs=dict(maxiter=1,
                                                                        use_absorbances=False),
                                    maxiter=2, shift_tolerance=0.001, upsampling=20, relative_sample_size=1.,
                                    relaxation_weight=0., center_of_mass_shift_weight=0., align_k=False)
    print(data_container.geometry.j_offsets, data_container.geometry.k_offsets)
    assert np.allclose(data_container.geometry.j_offsets, 0.409309239143207)
    assert np.allclose(data_container.geometry.k_offsets, -0.754)


def test_alignment_no_j(data_container, caplog):
    data_container.geometry.j_offsets[0] = 0.534
    data_container.geometry.k_offsets[0] = -0.754
    data_container.projections[0].diode = np.arange(16.).reshape(4, 4)
    run_cross_correlation_alignment(data_container, use_gpu=True,
                                    reconstruction_pipeline_kwargs=dict(maxiter=1,
                                                                        use_absorbances=True),
                                    maxiter=2, shift_tolerance=0.001, relative_sample_size=1.,
                                    relaxation_weight=0., center_of_mass_shift_weight=0., align_j=False)
    print(data_container.geometry.j_offsets, data_container.geometry.k_offsets)
    assert np.allclose(data_container.geometry.j_offsets, 0.534)
    assert np.allclose(data_container.geometry.k_offsets, 1.246)
