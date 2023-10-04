import pytest  # noqa:F401
from numba import cuda
import numpy as np

""" This test exists to check that the CI is compatible
with `numba.cuda`. """

test_array_1 = np.array([1, 2, 3]).astype(np.float32)
test_array_2 = np.array([0.5, -0.5, 1.5]).astype(np.float32)
result = np.array([1.5, 1.5, 4.5]).astype(np.float32)

device_array_1 = cuda.to_device(test_array_1)
device_array_2 = cuda.to_device(test_array_2)
out_device_array = cuda.device_array_like(device_array_1)

tpb = 3
bpg = test_array_1.size // tpb


@cuda.jit
def cuda_add(a, b, c):
    i = cuda.grid(1)
    if i < c.size:
        c[i] = a[i] + b[i]


@pytest.mark.parametrize('a,b,out,result', [(device_array_1, device_array_2,
                                             out_device_array, result)])
def test_cuda_add(a, b, out, result):
    cuda_add[tpb, bpg](a, b, out)
    assert np.allclose(out.copy_to_host(), result)
