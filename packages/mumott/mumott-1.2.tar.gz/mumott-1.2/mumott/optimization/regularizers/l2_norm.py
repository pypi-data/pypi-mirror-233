from typing import Dict

import numpy as np
from numpy.typing import NDArray

from mumott.optimization.regularizers.base_regularizer import Regularizer


class L2Norm(Regularizer):

    r"""Regularizes using the :math:`L_2` norm of the coefficient vector, also known as the Euclidean norm.
    Suitable for most representations, including non-local ones. Tends to reduce large values,
    and often leads to fast convergence.

    The :math:`L_2` norm of a vector :math:`x` is given by :math:`\sum{\vert x \vert^2}`.

    See also `the Wikipedia article on the Euclidean norm
    <https://en.wikipedia.org/wiki/Euclidean_space#Euclidean_norm>`_
    """

    def __init__(self):
        super().__init__()

    def get_regularization_norm(self,
                                coefficients: NDArray[float],
                                get_gradient: bool = False) -> Dict:
        """Retrieves the :math:`L_2` norm, of the coefficient vector. Appropriate for
        use with scalar coefficients or local basis sets.

        Parameters
        ----------
        coefficients
            An ``np.ndarray`` of values, with shape ``(X, Y, Z, W)``, where
            the last channel contains, e.g., tensor components.
        get_gradient
            If ``True``, returns a ``'gradient'`` of the same shape as :attr:`coefficients`.
            Otherwise, the entry ``'gradient'`` will be ``None``. Defaults to ``False``.

        Returns
        -------
            A dictionary with two entries, ``regularization_norm`` and ``gradient``.
        """
        result = dict(regularization_norm=None, gradient=None)
        if get_gradient:
            result['gradient'] = coefficients
        result['regularization_norm'] = np.sum(coefficients ** 2)
        return result

    @property
    def _function_as_str(self) -> str:
        return 'R(x) = lambda * abs(x) ** 2'

    @property
    def _function_as_tex(self) -> str:
        return r'$R(\vec{x}) = \lambda \Vert \vec{x} \Vert_2^2$'
