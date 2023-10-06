from iclik.inform_crit import claic, clbic
import numpy as np
import math

# case 1
def f1(params):
    x, y, z = params
    return x**2 + y**2 + z**2

params1 = (1,2,3)
wolfram_hessmat1 = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 2]])
wolfram_jacmat1 = np.array([[2*1, 2*2, 2*3]])

def test_claic():
    likelihood = f1(params1)
    claic_manual = (-2*likelihood + 2 * np.trace(wolfram_jacmat1 
                               @ np.linalg.inv(wolfram_hessmat1)))
    
    assert math.isclose(claic_manual, claic(f1, params1), abs_tol=1e-5)

def test_clbic():
    likelihood = f1(params1)
    n_samples = 100
    clbic_manual = (-2 * likelihood
                    + np.log(n_samples)
                    * np.trace(wolfram_jacmat1 
                               @ np.linalg.inv(wolfram_hessmat1)))
    
    assert math.isclose(clbic_manual,
                                       clbic(f1, params1, n_samples=100), abs_tol=1e-5)



