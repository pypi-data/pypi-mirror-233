import logging

from typing import Tuple

import numpy as np
from numpy.typing import NDArray
from numba import get_num_threads


from mumott.core.john_transform import john_transform, john_transform_adjoint
from mumott.core.hashing import list_to_hash
from mumott.core.deprecation_warning import deprecated

from mumott import Geometry

from .base_projector import Projector

logger = logging.getLogger(__name__)


@deprecated('Use SAXSProjectorBilinear instead.')
class SAXSProjectorNumba(Projector):
    """
    Projector for transforms of tensor fields from three-dimensional space
    to projection space.

    Parameters
    ----------
    geometry : Geometry
        An instance of :class:`Geometry <mumott.Geometry>` containing the
        necessary vectors to compute forwared and adjoint projections.
    step_size : np.float64
        A number ``0 < step_size <= 1`` that indicates the degree of
        upsampling when computing projections. Default is ``0.5``.
    """
    def __init__(self,
                 geometry: Geometry,
                 step_size: np.float64 = np.float64(0.5)):

        super().__init__(geometry)

        self._sampling_kernel = np.array((1.,), dtype=np.float64)
        self._kernel_offsets = np.array((0., 0.), dtype=np.float64)
        self._created_sampling_kernel = False
        self.step_size = step_size
        self._update(force_update=True)

    def _get_john_transform_parameters(self,
                                       index: int) -> Tuple:
        vector_p = self._basis_vector_projection[index]
        vector_j = self._basis_vector_j[index]
        vector_k = self._basis_vector_k[index]
        projection_offsets = np.array((self._geometry[index].j_offset,
                                       self._geometry[index].k_offset)).ravel()
        return (vector_p, vector_j, vector_k, self._step_size, projection_offsets,
                self._sampling_kernel.ravel(), self._kernel_offsets.reshape(2, -1))

    def forward(self,
                field: NDArray,
                indices: NDArray[int] = None) -> NDArray:
        """ Compute the forward projection of a tensor field.

        Parameters
        ----------
        field
            An array containing coefficients in its fourth dimension,
            which are to be projected into two dimensions. The first three
            dimensions should match the ``volume_shape`` of the sample.
        indices
            A one-dimensional array containing one or more indices
            indicating which projections are to be computed. If ``None``,
            all projections will be computed.

        Returns
        -------
            An array with four dimensions ``(I, J, K, L)``, where
            the first dimension matches :attr:`indices`, such that
            ``projection[i]`` corresponds to the geometry of projection
            ``indices[i]``. The second and third dimension contain
            the pixels in the ``J`` and ``K`` dimension respectively, whereas
            the last dimension is the coefficient dimension, matching ``field[-1]``.
        """
        if not np.allclose(field.shape[:-1], self._geometry.volume_shape):
            raise ValueError(f'The shape of the input field ({field.shape}) does not match the'
                             f' volume shape expected by the projector ({self._geometry.volume_shape})')
        self._update()
        if indices is None:
            return self._forward_stack(field)
        return self._forward_subset(field, indices)

    def _forward_subset(self,
                        field: NDArray,
                        indices: NDArray[int]) -> NDArray:
        """ Internal method for computing a subset of projections.

        Parameters
        ----------
        field
            The field to be projected.
        indices
            The indices indicating the subset of all projections in the
            system geometry to be computed.

        Returns
        -------
            The resulting projections.
        """
        indices = np.array(indices).ravel()
        projections = np.zeros((indices.size,) +
                               tuple(self._geometry.projection_shape) +
                               (field.shape[-1],), dtype=np.float64)
        self._check_indices_kind_is_integer(indices)
        for i, index in enumerate(indices):
            john_transform(projections[i], field, *self._get_john_transform_parameters(index))
        return projections

    def _forward_stack(self,
                       field: NDArray) -> NDArray:
        """Internal method for forward projecting an entire stack.

        Parameters
        ----------
        field
            The field to be projected.

        Returns
        -------
            The resulting projections.
        """
        projections = np.zeros((len(self._geometry),) +
                               tuple(self._geometry.projection_shape) +
                               (field.shape[-1],), dtype=np.float64)
        for i, g in enumerate(self._geometry):
            john_transform(projections[i], field, *self._get_john_transform_parameters(i))
        return projections

    def adjoint(self,
                projections: NDArray,
                indices: NDArray[int] = None) -> NDArray:
        """ Compute the adjoint of a set of projections according to the system geometry.

        Parameters
        ----------
        projections
            An array containing coefficients in its last dimension,
            from e.g. the residual of measured data and forward projections.
            The first dimension should match :attr:`indices` in size, and the
            second and third dimensions should match the system projection geometry.
        indices
            A one-dimensional array containing one or more indices
            indicating from which projections the adjoint is to be computed.

        Returns
        -------
            The adjoint of the provided projections.
            An array with four dimensions ``(X, Y, Z, P)``, where the first
            three dimensions are spatial and the last dimension runs over
            coefficients.
        """
        if not np.allclose(projections.shape[-3:-1], self._geometry.projection_shape):
            raise ValueError(f'The shape of the projections ({projections.shape}) does not match the'
                             f' projection shape expected by the projector'
                             f' ({self._geometry.projection_shape})')
        self._update()
        if indices is None:
            return self._adjoint_stack(projections)
        return self._adjoint_subset(projections, indices)

    def _adjoint_subset(self,
                        projections: NDArray,
                        indices: NDArray[int]) -> NDArray:
        """ Internal method for computing the adjoint of only a subset of projections.

        Parameters
        ----------
        projections
            An array containing coefficients in its last dimension,
            from e.g. the residual of measured data and forward projections.
            The first dimension should match :attr:`indices` in size, and the
            second and third dimensions should match the system projection geometry.
        indices
            A one-dimensional array containing one or more indices
            indicating from which projections the adjoint is to be computed.

        Returns
        -------
            The adjoint of the provided projections.
            An array with four dimensions ``(X, Y, Z, P)``, where the first
            three dimensions are spatial and the last dimension runs over
            coefficients. """
        indices = np.array(indices).ravel()
        if projections.ndim == 3:
            assert indices.size == 1
            projections = projections[np.newaxis, ...]
        else:
            assert indices.size == projections.shape[0]
        self._check_indices_kind_is_integer(indices)
        field = np.zeros((get_num_threads(),) +
                         tuple(self._geometry.volume_shape) +
                         (projections.shape[-1],), dtype=np.float64)
        for num, i in enumerate(indices):
            # Note that we assume projections match ``indices`` in their layout.
            john_transform_adjoint(projections[num], field, *self._get_john_transform_parameters(i))
        # each thread writes into a separate array, they are reduced by summation.
        return field.sum(0)

    def _adjoint_stack(self,
                       projections: NDArray) -> NDArray:
        """ Internal method for computing the adjoint of a whole stack of projections.

        Parameters
        ----------
        projections
            An array containing coefficients in its last dimension,
            from e.g. the residual of measured data and forward projections.
            The first dimension should run over all the projection directions
            in the system geometry.

        Returns
        -------
            The adjoint of the provided projections.
            An array with four dimensions ``(X, Y, Z, P)``, where the first
            three dimensions are spatial, and the last dimension runs over
            coefficients. """
        assert projections.shape[0] == len(self._geometry)
        field = np.zeros((get_num_threads(),) +
                         tuple(self._geometry.volume_shape) +
                         (projections.shape[-1],), dtype=np.float64)
        for i, g in enumerate(self._geometry):
            john_transform_adjoint(projections[i], field, *self._get_john_transform_parameters(i))
        # each thread writes into a separate array, they are reduced by summation.
        return field.sum(0)

    def create_sampling_kernel(self,
                               kernel_dimensions: Tuple[int, int] = (3, 3),
                               kernel_width: Tuple[float, float] = (1., 1.),
                               kernel_type: str = 'bessel') -> None:
        """ Creates a kernel to emulate the point spread function (PSF) of the
        beam. This can improve the accuracy of the projection function.

        Parameters
        ----------
        kernel_dimensions
            A tuple of how many points should be sampled in each direction of the kernel.
            The total number of line integrals per pixel in the data is
            ``kernel_dimensions[0] * kernel_dimensions[1]``.
        kernel_width
            Width parameter for the kernel in units of pixels.
            Typically the full-width-half-maximum (FWHM) of the beam used for data acquisition.
        kernel_type
            The type of kernel to use.
            Acceptable values are ``'bessel'``, ``'rectangular'``, and ``'gaussian'``.

            ``'bessel'`` uses a sinc function multiplied by a
            Lanczos window with the width parameter being the first Bessel zero. This
            gives a sharply peaked distribution that goes to zero at twice the full
            width half maximum, and samples are taken up to this zero.

            ``'rectangular'`` samples uniformly in a rectangle of size :attr:`kernel_width`.

            ``'gaussian'`` uses a normal distribution with the FWHM given by
            :attr:`kernel_width` sampled up to twice the FWHM.
        """
        if self._created_sampling_kernel:
            logger.warning('It appears that you have already created a sampling kernel.'
                           ' The old sampling kernel will be overwritten.')
        if kernel_type == 'bessel':
            L = 0.7478
            ji = np.linspace(-kernel_width[0], kernel_width[0], kernel_dimensions[0] * 100)
            fj = np.sinc(ji * L / kernel_width[0]) * np.sinc(ji / kernel_width[0])
            ki = np.linspace(-kernel_width[1], kernel_width[1], kernel_dimensions[1] * 100)
            fk = np.sinc(ki * L / kernel_width[1]) * np.sinc(ki / kernel_width[1])
        elif kernel_type == 'rectangular':
            ji = np.linspace(-kernel_width[0] / 2, kernel_width[0] / 2, kernel_dimensions[0] * 100)
            fj = np.ones_like(ji)
            ki = np.linspace(-kernel_width[1] / 2, kernel_width[1] / 2, kernel_dimensions[1] * 100)
            fk = np.ones_like(ki)
        elif kernel_type == 'gaussian':
            std = np.array(kernel_width) / (2 * np.sqrt(2 * np.log(2)))
            ji = np.linspace(-kernel_width[0], kernel_width[0], kernel_dimensions[0] * 100)
            fj = np.exp(-0.5 * (ji ** 2) / ((std[0]) ** 2))
            ki = np.linspace(-kernel_width[1], kernel_width[1], kernel_dimensions[1] * 100)
            fk = np.exp(-0.5 * (ki ** 2) / ((std[1]) ** 2))
        else:
            raise ValueError(f'Unknown kernel type: {kernel_type}.')
        fr = fj.reshape(-1, 1) * fk.reshape(1, -1)
        fr = fr.reshape(kernel_dimensions[0], 100, kernel_dimensions[1], 100)
        fi = fr.sum(axis=(1, 3))
        fi = (fi / fi.sum()).astype(np.float64)
        J = ji.reshape(-1, 1) * np.ones((1, ki.size))
        K = ki.reshape(1, -1) * np.ones((ji.size, 1))
        J = J.reshape(kernel_dimensions[0], 100, kernel_dimensions[1], 100)
        K = K.reshape(kernel_dimensions[0], 100, kernel_dimensions[1], 100)
        Ji = J.mean(axis=(1, 3)).flatten()
        Ki = K.mean(axis=(1, 3)).flatten()
        offset = np.concatenate((Ji, Ki)).astype(np.float64)
        self._sampling_kernel = fi
        self._kernel_offsets = offset
        self._sampling_kernel_size = np.int32(kernel_dimensions[0] * kernel_dimensions[1])
        self._created_sampling_kernel = True

    @property
    def step_size(self) -> np.float64:
        """
        One-dimensional upsampling ratio for the integration of each projection line.
        """
        return self._step_size

    @step_size.setter
    def step_size(self,
                  val: np.float64) -> None:
        if not 0.0 < val <= 1.0:
            raise ValueError('Integration step size must be less than or'
                             ' equal to 1.0, and greater than 0.0, but the'
                             f' provided value is {val}.')
        # under normal circumstances this casting is not needed, but it is a safeguard
        self._step_size = np.float64(val)

    @property
    def sampling_kernel(self) -> NDArray[np.float64]:
        """ Convolution kernel for the sampling profile. """
        return self._sampling_kernel

    @property
    def dtype(self) -> np.typing.DTypeLike:
        """ Preferred dtype of this ``Projector``. """
        return np.float64

    @property
    def kernel_offsets(self) -> NDArray[np.float64]:
        """ Offsets for the sampling profile kernel. """
        return self._kernel_offsets

    def __hash__(self) -> int:
        to_hash = [self._step_size,
                   self._sampling_kernel,
                   self._kernel_offsets,
                   self._basis_vector_projection,
                   self._basis_vector_j,
                   self._basis_vector_k,
                   self._geometry_hash,
                   hash(self._geometry)]
        return int(list_to_hash(to_hash), 16)

    def __str__(self) -> str:
        wdt = 74
        s = []
        s += ['-' * wdt]
        s += [self.__class__.__name__.center(wdt)]
        s += ['-' * wdt]
        with np.printoptions(threshold=4, edgeitems=2, precision=5, linewidth=60):
            s += ['{:18} : {}'.format('step_size', self.step_size)]
            s += ['{:18} : {}'.format('is_dirty', self.is_dirty)]
            s += ['{:18} : {}'.format('sampling_kernel', self.sampling_kernel)]
            s += ['{:18} : {}'.format('kernel_offsets', self.kernel_offsets)]
            s += ['{:18} : {}'.format('hash', hex(hash(self))[2:8])]
        s += ['-' * wdt]
        return '\n'.join(s)

    def _repr_html_(self) -> str:
        s = []
        s += [f'<h3>{self.__class__.__name__}</h3>']
        s += ['<table border="1" class="dataframe">']
        s += ['<thead><tr><th style="text-align: left;">Field</th><th>Size</th><th>Data</th></tr></thead>']
        s += ['<tbody>']
        with np.printoptions(threshold=4, edgeitems=2, precision=2, linewidth=40):
            s += ['<tr><td style="text-align: left;">step_size</td>']
            s += [f'<td>1</td><td>{self.step_size}</td></tr>']
            s += ['<tr><td style="text-align: left;">is_dirty</td>']
            s += [f'<td>1</td><td>{self.is_dirty}</td></tr>']
            s += ['<tr><td style="text-align: left;">sampling_kernel</td>']
            s += [f'<td>{self.sampling_kernel.shape}</td><td>{self.sampling_kernel}</td></tr>']
            s += ['<tr><td style="text-align: left;">kernel_offsets</td>']
            s += [f'<td>{self.kernel_offsets.shape}</td><td>{self.kernel_offsets}</td></tr>']
            s += ['<tr><td style="text-align: left;">hash</td>']
            s += [f'<td>{len(hex(hash(self)))}</td><td>{hex(hash(self))[2:8]}</td></tr>']
        s += ['</tbody>']
        s += ['</table>']
        return '\n'.join(s)
