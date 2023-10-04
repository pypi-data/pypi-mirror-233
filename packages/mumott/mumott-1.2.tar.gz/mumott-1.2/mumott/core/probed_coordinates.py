from dataclasses import dataclass
from typing import Tuple
import numpy as np

from numpy.typing import NDArray

from .hashing import list_to_hash


@dataclass
class ProbedCoordinates:
    """ A small container class for probed coordinates for the
    :class:` BasisSet <mumott.methods.BasisSet>` being used
    together with the :class:`Method <Method>`.

    Parameters
    ----------
    vector : NDArray[float]
        The coordinates on the sphere probed at each detector segment by the
        experimental method. Should be structured ``(N, M, I, 3)`` where ``N``
        is the number of projections, ``M`` is the number of detector segments,
        ``I`` is the number of points on the detector to be integrated over,
        and the last index gives the ``(x, y, z)`` components of the coordinates.
        ``I`` can be as small as ``1``, but the array still needs to be structured
        in this way explicitly.
        By default, the value will be ``np.array([1., 0., 0.]).reshape(1, 1, 1, 3)``.

    """
    vector: NDArray[float] = np.array([1., 0., 0.]).reshape(1, 1, 1, 3)

    def __hash__(self) -> int:
        return int(list_to_hash([self.vector]), 16)

    @property
    def to_spherical(self) -> Tuple:
        """ Returns spherical coordinates of :attr:`vector`, in the order
        ``(radius, polar angle, azimuthal angle)``. """
        r = np.linalg.norm(self.vector, axis=-1)
        theta = np.arccos(self.vector[..., 2] / r)
        phi = np.arctan2(self.vector[..., 1], self.vector[..., 0])
        return (r, theta, phi)
