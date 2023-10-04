import pytest
from mumott.core.hashing import list_to_hash

import numpy as np


class myclass:
    a = 0


list_of_lists = [[1, 2, 3],
                 [np.array([0]), dict(a=1, b=(1, 2, 3))],
                 ['stringstring', b'bytestring', np.array(['array', 'of', 'strings'])],
                 [1 + 1j, np.array((1 + 1j)), [np.array((1, 2)), np.array((4, 5))]],
                 [np.sin(np.pi / 5), np.sqrt(2) / 10, np.sqrt(3) * 1e-32],
                 [None, dict(val=None)],
                 [np.array([None])],
                 [myclass()]]

list_of_hashes = ['e64cb9', 'ae9dc0', 'fddfa8', '247c1d', '953a23', 'cade30', None, None]


@pytest.mark.parametrize('inlist, list_hash', [t for t in zip(list_of_lists, list_of_hashes)])
def test_hashing(inlist, list_hash):
    if list_hash is None:
        with pytest.raises(TypeError, match='object'):
            list_to_hash(inlist)
    else:
        my_hash = list_to_hash(inlist)
        assert my_hash[:6] == list_hash
