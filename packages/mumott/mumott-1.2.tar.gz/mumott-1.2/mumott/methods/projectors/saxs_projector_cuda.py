import logging

import numpy as np
from numpy.typing import NDArray
from numba.cuda import is_cuda_array

from mumott.core.cuda_utils import cuda_calloc
from mumott.core.john_transform_cuda import john_transform_cuda, john_transform_adjoint_cuda
from .saxs_projector_bilinear import SAXSProjectorBilinear

logger = logging.getLogger(__name__)


class SAXSProjectorCUDA(SAXSProjectorBilinear):
    """
    Projector for transforms of tensor fields from three-dimensional space
    to projection space. Uses a projection algorithm implemented in
    ``numba.cuda``.

    Parameters
    ----------
    geometry : Geometry
        An instance of :class:`Geometry <mumott.Geometry>` containing the
        necessary vectors to compute forwared and adjoint projections.
    """
    @staticmethod
    def _get_zeros_method(array: NDArray):
        """ Internal method for returning `cupy` or `numpy` based on the type of array given. """
        if is_cuda_array(array):
            return cuda_calloc
        else:
            return np.zeros

    def _compile_john_transform(self,
                                field: NDArray[float],
                                projections: NDArray[float],
                                *args) -> None:
        """ Internal method for compiling John transform only as needed. """
        self._compiled_john_transform = john_transform_cuda(
                                            field, projections, *args)
        self._compiled_john_transform_adjoint = john_transform_adjoint_cuda(
                                                    field, projections, *args)

    @property
    def dtype(self) -> np.typing.DTypeLike:
        """ Preferred dtype of this ``Projector``. """
        return np.float32
