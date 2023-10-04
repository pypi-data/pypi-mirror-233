import pytest  # noqa:F401
import cupy as cp

""" This test exists to check that the CI is compatible
with `cupy`. """

a = cp.array([1, 2, 3])
b = cp.array([-0.5, -1, -4])

res = cp.array([1.5, 3, 7])

c = cp.arange(1, 10).reshape(3, 3)
d = cp.arange(1, 16).reshape(3, 5)

res2 = cp.array([[46, 52, 58, 64, 70],
                 [100, 115, 130, 145, 160],
                 [154, 178, 202, 226, 250]])


@pytest.mark.parametrize('in1, in2, result', [(a, b, res)])
def test_diff(in1, in2, result):
    out = in1 - in2
    assert cp.allclose(out, result)


@pytest.mark.parametrize('in1, in2, result', [(c, d, res2)])
def test_matmul(in1, in2, result):
    out = in1 @ in2
    assert cp.allclose(out, result)
