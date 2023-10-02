__all__ = ["inner_map", "matmul_diag"]

from functools import partial

import jax.scipy as jsp
from jax import vmap
from jaxtyping import Array, Float


@partial(vmap, in_axes=(None, 1))
def inner_map(tri: Float[Array, "N N"], rhs: Float[Array, "N M"], lower: bool=True) -> Float[Array, "M"]:
    '''Calculates diag(rhs.T @ (tri @ tri.T)**(-1) @ rhs) by using vmap to only calculate the diagonal entries and nothing else.

    Parameters
    -------
    tri : Float[Array, "N N"]
        A triangular matrix describing the Cholesky factor of a matrix.
    rhs : Float[Array, "N M"]
        The outer matrix
    lower : bool, optional
        Flag showing if tri is a lower triangular matrix, by default True.

    Returns
    -------
    Float[Array, "M"]
        An array with length equal to the second dimension of rhs describing the result of the above equation.
    '''    
    sol = jsp.linalg.solve_triangular(tri, rhs, lower=lower)
    return sol.T@sol

@partial(vmap, in_axes=(0,0))
def matmul_diag(diagonal: Float[Array, "N"], rhs: Float[Array, "N M"]) -> Float[Array, "N M"]:
    '''Faster matrix multiplication for a diagonal matrix. 

    Parameters
    ----------
    diagonal : Float[Array, "N"]
        A diagonal matrix represented by a 1d vector.
    rhs : Float[Array, "N M"]
        A generic matrix to be multiplied with a diagonal matrix from the left.

    Returns
    -------
    Float[Array, "N M"]
        Reulting product matrix.
    '''
    return diagonal*rhs