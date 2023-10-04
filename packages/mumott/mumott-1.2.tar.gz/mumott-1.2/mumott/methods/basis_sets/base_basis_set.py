from abc import ABC, abstractmethod
from mumott import ProbedCoordinates

from numpy.typing import NDArray


class BasisSet(ABC):

    """This is the base class from which specific basis sets are being derived.
    """

    def __init__(self,
                 probed_coordinates: ProbedCoordinates):
        pass

    @abstractmethod
    def forward(self,
                coefficients: NDArray,
                indices: NDArray = None) -> NDArray:
        pass

    @abstractmethod
    def gradient(self,
                 coefficients: NDArray,
                 indices: NDArray = None) -> NDArray:
        pass

    @abstractmethod
    def get_output(self,
                   coefficients: NDArray) -> dict:
        pass

    @abstractmethod
    def get_inner_product(self, u: NDArray, v: NDArray) -> NDArray:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __dict__(self) -> dict:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def _repr_html_(self) -> str:
        pass
