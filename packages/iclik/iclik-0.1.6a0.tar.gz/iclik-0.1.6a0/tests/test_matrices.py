import numpy as np
from iclik.matrices import hessian, jacobian

# case 1
def f1(params):
    x, y, z = params
    return x**2 + 2*y + z**2

params1 = (5,6,7)
wolfram_hessmat1 = np.array([[2, 0, 0], [0, 0, 0], [0, 0, 2]])
wolfram_jacmat1 = np.array([[2*5, 2, 2*7]])

def test_hessian_case1():
    hessmat = hessian(f1, params1, initial_step=1e-2, step_factor=0.1)
    np.testing.assert_allclose(hessmat, wolfram_hessmat1, atol=1e-5)

def test_jacobian_case1():
    jacmat = jacobian(f1, params1, initial_step=1e-2, step_factor=0.1)
    np.testing.assert_allclose(jacmat, wolfram_jacmat1, atol=1e-5)
