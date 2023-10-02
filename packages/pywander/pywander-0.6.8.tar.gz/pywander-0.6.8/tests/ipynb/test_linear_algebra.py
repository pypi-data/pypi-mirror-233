from pywander.ipynb.linear_algebra import solve, combine_system
import numpy as np
import pytest


def test_solve():
    m = np.array([
        [4, -3, 1],
        [2, 1, 3],
        [-1, 2, -5]
    ], dtype=np.dtype(float))

    b = np.array([-10, 0, 17], dtype=np.dtype(float))
    res = solve(m, b)
    assert res[0] == 1


def test_combine_system():
    m = np.array([
        [4, -3, 1],
        [2, 1, 3],
        [-1, 2, -5]
    ], dtype=np.dtype(float))

    b = np.array([-10, 0, 17], dtype=np.dtype(float))

    sys_a = combine_system(m, b)

    assert sys_a[0, 3] == -10


def test_cos():
    v1 = np.array([2, 1, 2, 3, 2, 9])
    v2 = np.array([3, 4, 2, 4, 5, 5])
    from pywander.ipynb.linear_algebra import cos
    res = cos(v1, v2)
    assert res == pytest.approx(0.8188, abs=1e-4)
