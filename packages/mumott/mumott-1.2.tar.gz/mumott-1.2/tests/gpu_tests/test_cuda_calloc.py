import pytest  # noqa:F401
import numpy as np

from mumott.core import cuda_utils

dtype_list = [np.int32, np.float32, np.float64, np.int64]
shape_list = [(3, 3, 3) for _ in dtype_list]


@pytest.mark.parametrize('shape, dtype', [t for t in zip(shape_list, dtype_list)])
def test_cuda_calloc(shape, dtype):
    a = cuda_utils.cuda_calloc(shape, dtype)
    assert np.allclose(0, a.copy_to_host())
    assert np.allclose(shape, a.shape)
    if dtype == np.float64:
        assert a.dtype == np.float32
    else:
        assert a.dtype == dtype
