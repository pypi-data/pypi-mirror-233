__all__ = ["covariance_matrix_computation", "covariance_diagonal_computation", "cov_ff", "cov_fg", "cov_gg", "gram_diag_f", "gram_diag_g"]

from typing import TypeVar

import jax.numpy as jnp
from jax import vmap
from jaxtyping import Array, Float

from calcgp.containers import Input

AbstractKernel = TypeVar("AbstractKernel", bound="calcgp.kernels.base.AbstractKernel")
    
def covariance_matrix_computation(kernel: AbstractKernel, X1: Input, X2: Input) -> Float[Array, "N M"]:
    '''Convenience function to compute the covariance matrix between the elements of two arrays via a given kernel. 
    Returns different shapes of the matrix depending on if the inputs represent function values, gradient values, or a mix of both.

    Parameters
    ----------
    kernel : AbstractKernel
        The kernel to use for the covariance calculation.
    X1 : Input
        First array from which to construct the covariance matrix.
    X2 : Input
        Second array from which to construct the covariance matrix.

    Returns
    -------
    Float[Array, "N M"]
        The covariance matrix constructed from the inputs.
    '''

    # -----------------------------------------------------------
    # Single type functions
    if X1.type == "func" and X2.type == "func":
        return cov_ff(kernel, X1.data, X2.data)
    
    if X1.type == "func" and X2.type == "grad":
        return cov_fg(kernel, X1.data, X2.data)
    
    if X1.type == "grad" and X2.type == "func":
        return cov_fg(kernel, X2.data, X1.data).T
    
    if X1.type == "grad" and X2.type == "grad":
        return cov_gg(kernel, X1.data, X2.data)
    
    # -----------------------------------------------------------
    # Mixed type functions
    if X1.type == "func" and X2.type == "mix":
        KF = cov_ff(kernel, X1.data, X2.data[0])
        KD = cov_fg(kernel, X1.data, X2.data[1])
        return jnp.hstack((KF,KD))
    
    if X1.type == "grad" and X2.type == "mix":
        KD = cov_fg(kernel, X2.data[0], X1.data).T
        KG = cov_gg(kernel, X1.data, X2.data[1])
        return jnp.hstack((KD,KG))
    
    if X1.type == "mix" and X2.type == "func":
        KF = cov_ff(kernel, X2.data, X1.data[0])
        KD = cov_fg(kernel, X2.data, X1.data[1])
        return jnp.hstack((KF,KD)).T
    
    if X1.type == "mix" and X2.type == "grad":
        KD = cov_fg(kernel, X1.data[0], X2.data)
        KG = cov_gg(kernel, X1.data[1], X2.data)
        return jnp.hstack((KD,KG))
    
    if X1.type == "mix" and X2.type == "mix":
        KF = cov_ff(kernel, X1.data[0], X2.data[0])
        KD = cov_fg(kernel, X1.data[0], X2.data[1])
        KDD = cov_gg(kernel, X1.data[1], X2.data[1])

        return jnp.vstack((jnp.hstack((KF,KD)), 
                        jnp.hstack((KD.T,KDD))))
        

def covariance_diagonal_computation(kernel: AbstractKernel, X: Input) -> Float[Array, "N"]:
    '''Convenience function to compute the diagonal of the covariance matrix between the elements of a single array via a given kernel. 
    Returns different shapes of the matrix depending on if the input represent function values, gradient values, or a mix of both.

    Parameters
    ----------
    kernel : AbstractKernel
        The kernel to use for the covariance calculation.
    X : Input
        Inputs from which to construct the covariance matrix diagonal.

    Returns
    -------
    Float[Array, "N"]
        The diagonal of the covariance matrix constructed from the inputs.
    '''
    if X.type == "func":
        return gram_diag_f(kernel, X.data)
    
    if X.type == "grad":
        return gram_diag_g(kernel, X.data)

    if X.type == "mix":
        return jnp.hstack((gram_diag_f(kernel, X.data[0]), gram_diag_g(kernel, X.data[1])))


def cov_ff(kernel: AbstractKernel, X1: Float[Array, "N D"], X2: Float[Array, "M D"]) -> Float[Array, "N M"]:
    '''Covariance matrix between the points corresponding to function values via the given kernel.

    Parameters
    ----------
    kernel : AbstractKernel
        The kernel to use for the covariance calculation.
    X1 : Float[Array, "N D"]
        Left hand input corresponding to a function evaluation.
    X2 : Float[Array, "M D"]
        Right hand input corresponding to a gradient evaluation.

    Returns
    -------
    Float[Array, "N M"]
        Function covariance matrix evaluated at the inputs.
    '''
    _func = lambda v1, v2: kernel(v1, v2)
    func = vmap(vmap(_func, in_axes=(None,0)), in_axes=(0,None))
    return func(X1, X2)

def cov_fg(kernel: AbstractKernel, X1: Float[Array, "N D"], X2: Float[Array, "M D"]) -> Float[Array, "N MD"]:
    '''Covariance matrix between the points corresponding to function (LHS) and gradient (RHS) values via the given kernel.

    Parameters
    ----------
    kernel : AbstractKernel
        The kernel to use for the covariance calculation.
    X1 : Float[Array, "N D"]
        Left hand input corresponding to a function evaluation.
    X2 : Float[Array, "N D"]
        Right hand input corresponding to a gradient evaluation.

    Returns
    -------
    Float[Array, "N MD"]
        Mixed covariance matrix evaluated at the inputs.
    '''
    _func = lambda v1, v2: kernel.grad(v1, v2) 
    func = vmap(vmap(_func, in_axes=(None,0)), in_axes=(0,None))
    return vmap(jnp.ravel, in_axes=0)(func(X1, X2))

def cov_gg(kernel: AbstractKernel, X1: Float[Array, "N D"], X2: Float[Array, "M D"]) -> Float[Array, "ND MD"]:
    '''Covariance matrix between the points corresponding to gradient values via the given kernel.

    Parameters
    ----------
    kernel : AbstractKernel
        The kernel to use for the covariance calculation.
    X1 : Float[Array, "N D"]
        Left hand input corresponding to a function evaluation.
    X2 : Float[Array, "M D"]
        Right hand input corresponding to a gradient evaluation.

    Returns
    -------
    Float[Array, "ND MD"]
        Gradient covariance matrix evaluated at the inputs.
    '''
    _func = lambda v1, v2: kernel.hess(v1, v2)
    func = vmap(vmap(_func, in_axes=(None,0)), in_axes=(0,None))
    return jnp.hstack(jnp.hstack((*func(X1, X2),)))

def gram_diag_f(kernel: AbstractKernel, X: Float[Array, "N D"]) -> Float[Array, "N"]:
    '''Gram matrix diagonal for functional values via the given kernel.

    Parameters
    ----------
    kernel : AbstractKernel
        The kernel to use for the covariance calculation.
    X : Float[Array, "N D"]
        Inputs corresponding to a function evaluation.

    Returns
    -------
    Float[Array, "N"]
        Function gram matrix diagonal evaluated at the inputs.
    '''
    _func = lambda v: kernel(v, v)
    func = vmap(_func, in_axes=(0))
    return func(X)

def gram_diag_g(kernel: AbstractKernel, X: Float[Array, "N D"]) -> Float[Array, "ND"]:
    '''Gram matrix diagonal for gradient values via the given kernel.

    Parameters
    ----------
    kernel : AbstractKernel
        The kernel to use for the covariance calculation.
    X : Float[Array, "N D"]
        Inputs corresponding to a function evaluation.

    Returns
    -------
    Float[Array, "ND"]
        Gradient gram matrix diagonal evaluated at the inputs.
    '''
    _func = lambda v: jnp.diag(kernel.hess(v, v))
    func = vmap(_func, in_axes=(0))
    return jnp.ravel(func(X))