IClik: Information Criteria for Composite Likelihoods
=====================================================

``IClik`` is a minimal package for evaluating composite likelihood
models using Composite Likelihood AIC and BIC (CLAIC/CLBIC).

For a review of these information criteria, please see: *Ng, C. T., &
Joe, H. (2014). Model comparison with composite likelihood information
criteria. Bernoulli, 20(4), 1738–1764.
http://www.jstor.org/stable/43590422*

**This package is in development. Please let me know about any bugs or
problems by raising an issue on GitHub.**

Available information criteria
------------------------------

Composite Likelihood AIC (CLAIC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The composite likelihood version of the Akaike information criterion
(AIC) was proposed by Varin et al (2011). It is calculated as:

.. math::  CLAIC = -2L_{CL}(\hat\theta_{CL}) + 2tr[\mathbf{J}(\hat\theta_{CL})\mathbf{H}^{-1}(\hat\theta_{CL})] 

Where :math:`\mathbf{J(\theta)}` and :math:`\mathbf{H(\theta)}` are the
Jacobian and Hessian matrices of the likelihood function, and
:math:`\hat\theta_{CL}` represents the composite maximum likelihood
estimate.

**Reference:** *Varin, C., Reid, N., & Firth, D. (2011). AN OVERVIEW OF
COMPOSITE LIKELIHOOD METHODS. Statistica Sinica, 21(1), 5–42.
http://www.jstor.org/stable/24309261*

Composite Likelihood BIC (CLBIC)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CLBIC, formulated by Gao and Song (2010), is similar to CLAIC, but
adjusts for sample size *n*:

.. math::  CLBIC = -2L_{CL}(\hat\theta_{CL}) + log(n) tr[\mathbf{J}(\hat\theta_{CL})\mathbf{H}^{-1}(\hat\theta_{CL})] 

**Reference:** *Gao, X., & Song, P. X.-K. (2010). Composite Likelihood
Bayesian Information Criteria for Model Selection in High-Dimensional
Data. Journal of the American Statistical Association, 105(492),
1531–1540. http://www.jstor.org/stable/27920184*

Installation
------------

``IClik`` is available via PyPi: ``pip install iclik``.

Syntax
------

``IClik`` is very easy to use, provided that you have a correctly
formulated likelihood function. A simple example of how to use it is
provided here.

Import ``claic``:

.. code:: python

   from iclik.inform_crit import claic

First we need to define a composite likelihood function.

.. code:: python

   def f(params):
       """I'm a composite likelihood function"""
       x, y, z = params
       return x**2 + y**2 + z**2

Running ``IClik`` is then a one-liner:

.. code:: python

   claic(f, (1,2,3))

Output:

.. code:: python

   -26.000000000000004
