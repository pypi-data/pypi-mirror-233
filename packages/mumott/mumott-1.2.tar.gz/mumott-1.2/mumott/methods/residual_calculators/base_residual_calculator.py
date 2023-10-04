from abc import ABC, abstractmethod
from typing import Dict

import logging
import numpy as np
from numpy.typing import NDArray

from mumott import DataContainer
from mumott.methods.basis_sets.base_basis_set import BasisSet
from mumott.methods.projectors.base_projector import Projector


logger = logging.getLogger(__name__)


class ResidualCalculator(ABC):

    """This is the base class from which specific residual calculators are being derived.
    """

    def __init__(self,
                 data_container: DataContainer,
                 basis_set: BasisSet,
                 projector: Projector,
                 integration_samples: int = 11,
                 use_scalar_projections: bool = False,
                 scalar_projections: NDArray[float] = None):
        self._data_container = data_container
        self._geometry_hash = hash(data_container.geometry)
        self._basis_set = basis_set
        self._basis_set_hash = hash(self._basis_set)
        self._projector = projector
        # GPU-based projectors need float32
        self._dtype = projector.dtype
        self._coefficients = np.zeros((*self._data_container.geometry.volume_shape,
                                      len(self._basis_set)), dtype=self._dtype)
        self._use_scalar_projections = use_scalar_projections
        self._scalar_projections = scalar_projections
        self._integration_samples = integration_samples

        # Check if full circle appears covered in data or not.
        delta = np.abs(self._detector_angles[0] -
                       self._detector_angles[-1] % (2 * np.pi))
        if abs(delta - np.pi) < min(delta, abs(delta - 2 * np.pi)) or use_scalar_projections:
            self._full_circle_covered = False
        else:
            logger.warning('The detector angles appear to cover a full circle.'
                           ' Friedel symmetry will be assumed in the calculation.\n'
                           'If this is incorrect, please set the property full_circle_covered'
                           ' to False.')  # This warning is not appropriate in WAXS
            self._full_circle_covered = True
        self._basis_set.probed_coordinates.vector = self._get_probed_coordinates()

    @abstractmethod
    def get_residuals(self) -> Dict:
        pass

    @property
    def probed_coordinates(self) -> NDArray:
        """ An array of 3-vectors with the (x, y, z)-coordinates
        on the reciprocal space map probed by the method.
        Structured as ``(N, K, I, 3)``, where ``N``
        is the number of projections, ``K`` is the number of
        detector segments, ``I`` is the number of points to be
        integrated over, and the last axis contains the
        (x, y, z)-coordinates.

        Notes
        -----
        The region of the reciprocal space map spanned by
        each detector segment is represented as a parametric curve
        between each segment. This is intended to simulate the effect
        of summing up pixels on a detector screen. For other methods of
        generating data (e.g., by fitting measurements to a curve),
        it may be more appropriate to only include a single point, which
        will then have the same coordinates as the center of a detector
        segments. This can be achieved by setting the property
        :attr:`integration_samples`.
        """
        return self._get_probed_coordinates()

    def _get_probed_coordinates(self) -> NDArray:
        """
        Calculates and returns the probed polar and azimuthal coordinates on the unit sphere at
        each angle of projection and for each detector segment in the system's geometry.
        """
        n_proj = len(self._data_container.geometry)
        n_seg = len(self._detector_angles)
        probed_directions_zero_rot = np.zeros((n_seg,
                                               self._integration_samples,
                                               3))
        # Impose symmetry if needed.
        if not self._full_circle_covered:
            shift = np.pi
        else:
            shift = 0
        det_bin_middles_extended = np.copy(self._detector_angles)
        det_bin_middles_extended = np.insert(det_bin_middles_extended, 0,
                                             det_bin_middles_extended[-1] + shift)
        det_bin_middles_extended = np.append(det_bin_middles_extended, det_bin_middles_extended[1] + shift)

        for ii in range(n_seg):

            # Check if the interval from the previous to the next bin goes over the -pi +pi discontinuity
            before = det_bin_middles_extended[ii]
            now = det_bin_middles_extended[ii + 1]
            after = det_bin_middles_extended[ii + 2]

            if abs(before - now + 2 * np.pi) < abs(before - now):
                before = before + 2 * np.pi
            elif abs(before - now - 2 * np.pi) < abs(before - now):
                before = before - 2 * np.pi

            if abs(now - after + 2 * np.pi) < abs(now - after):
                after = after - 2 * np.pi
            elif abs(now - after - 2 * np.pi) < abs(now - after):
                after = after + 2 * np.pi

            # Generate a linearly spaced set of angles covering the detector segment
            start = 0.5 * (before + now)
            end = 0.5 * (now + after)
            inc = (end - start) / self._integration_samples
            angles = np.linspace(start + inc / 2, end - inc / 2, self._integration_samples)

            # Make the zero-rotation-projection vectors corresponding to the given angles
            probed_directions_zero_rot[ii, :, :] = np.cos(angles[:, np.newaxis]) * \
                self._data_container.geometry.detector_direction_origin[np.newaxis, :]
            probed_directions_zero_rot[ii, :, :] += np.sin(angles[:, np.newaxis]) * \
                self._data_container.geometry.detector_direction_positive_90[np.newaxis, :]

        # Initialize array for vectors
        probed_direction_vectors = np.zeros((n_proj,
                                             n_seg,
                                             self._integration_samples,
                                             3), dtype=np.float64)
        # Calculate all the rotations
        probed_direction_vectors[...] = \
            np.einsum('kij,mli->kmlj',
                      self._data_container.geometry.rotations_as_array,
                      probed_directions_zero_rot)
        return probed_direction_vectors

    @property
    def _data(self) -> NDArray:
        """ Internal method for choosing between scalar_projections and data. """
        if self._use_scalar_projections:
            return self._scalar_projections
        else:
            return self._data_container.data

    @property
    def _weights(self) -> NDArray:
        """ Internal method for choosing between weights for the
        scalar_projections or weights for the data. """
        if self._use_scalar_projections:
            return np.mean(self._data_container.weights, axis=-1)[..., None]
        else:
            return self._data_container.weights

    @property
    def _detector_angles(self) -> NDArray:
        """ Internal method for choosing between detector angles for the data
        or detector angles for the scalar_projections. """
        if self._use_scalar_projections:
            return np.array((0.,))
        else:
            return self._data_container.geometry.detector_angles

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def _repr_html_(self) -> str:
        pass
