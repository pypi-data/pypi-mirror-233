import numpy as np
from iclik.matrices import jacobian, hessian


def _cl_akaike(likelihood, jacobian_mat, hessian_mat):
    """Compute CLAIC from matrices."""
    return (-2 * likelihood 
            + 2 * np.trace(jacobian_mat @ np.linalg.inv(hessian_mat)))


def _cl_bayes(likelihood, jacobian_mat, hessian_mat, n_samples):
    """Compute CLBIC from matrices."""
    return (-2 * likelihood
            + np.log(n_samples)
            * np.trace(jacobian_mat @ np.linalg.inv(hessian_mat)))


def _detect_zeros(estimates, warn, error):
    """Detect whether array of parameter estimates contains zeros."""
    if (estimates < 0).any():
        if error:
            raise ValueError("Zero or negative values detected")
        elif warn:
            print("Warning: zero or negative values detected")


def _detect_nan_inf(estimates, warn, error):
    """Detect whether array of parameter estimates contains NaN/inf."""
    if not (np.isfinite(estimates)).all():
        if error:
            raise ValueError("NaN or Inf values detected")
        elif warn:
            print("Warning: NaN or Inf values detected")


def _information_criterion(calc_claic, calc_clbic, f, estimates, n_samples=None,
                           step=1e-2, step_factor=0.5,
                           zeros="allow", nan_infs="error"):
    """Compute CLAIC or CLBIC from function."""
    
    assert zeros in ["allow", "warn", "error"]
    if zeros == "warn":
        _detect_zeros(estimates, warn=True, error=False)
    elif zeros == "error":
        _detect_zeros(estimates, warn=True, error=True)

    assert nan_infs in ["allow", "warn", "error"]
    if nan_infs == "warn":
        _detect_nan_inf(estimates, warn=True, error=False)
    elif nan_infs == "error":
        _detect_nan_inf(estimates, warn=True, error=True)

    jacobian_mat = jacobian(f, estimates, initial_step=step, step_factor=step_factor)
    hessian_mat = hessian(f, estimates, initial_step=step, step_factor=step_factor)

    likelihood = f(estimates)

    res = []
    if calc_claic is True:
        res.append(_cl_akaike(likelihood=likelihood, jacobian_mat=jacobian_mat, hessian_mat=hessian_mat))
    if calc_clbic is True:
        assert n_samples is not None, "n_samples must be provided if calculating CLBIC"
        res.append(_cl_bayes(likelihood=likelihood, jacobian_mat=jacobian_mat, hessian_mat=hessian_mat, n_samples=n_samples))

    return res


def claic(f, estimates, step=1e-2, step_factor=0.5, zeros="allow", nan_infs="error"):
    """Compute composite likelihood Akaike information criterion (CLAIC).

    Args:
        f (function): Composite log-likelihood function.
        estimates (ndarray): Parameter estimates at which to evaluate CLAIC.
        step (float): Step size for finding Hessian and Jacobian matrices.
        zeros (str, optional): What to do with zeros in input, one of {"allow", "warn", "error"}. Defaults to "allow".
        nan_infs (str, optional): What to do with NaNs and infs in input, one of {"allow", "warn", "error"}. Defaults to "error".

    Returns:
        float: Composite likelihood AIC estimate.
    """
    return _information_criterion(calc_claic=True, calc_clbic=False,
                                  f=f,
                                  estimates=estimates,
                                  step=step,
                                  step_factor=step_factor,
                                  zeros=zeros,
                                  nan_infs=nan_infs)[0]


def clbic(f, estimates, n_samples, step=1e-2, step_factor=0.5, zeros="allow", nan_infs="error"):
    """Compute composite likelihood Bayesian information criterion (CLBIC).

    Args:
        f (function): Composite log-likelihood function.
        estimates (ndarray): Parameter estimates at which to evaluate CLBIC.
        step (float): Step size for finding Hessian and Jacobian matrices.
        n_samples (int): Number of samples in data.
        zeros (str, optional): What to do with zeros in input, one of {"allow", "warn", "error"}. Defaults to "allow".
        nan_infs (str, optional): What to do with NaNs and infs in input, one of {"allow", "warn", "error"}. Defaults to "error".

    Returns:
        float: Composite likelihood BIC estimate.
    """
    return _information_criterion(calc_claic=False, calc_clbic=True,
                                  f=f,
                                  estimates=estimates,
                                  n_samples=n_samples,
                                  step=step,
                                  step_factor=step_factor,
                                  zeros=zeros,
                                  nan_infs=nan_infs)[0]

