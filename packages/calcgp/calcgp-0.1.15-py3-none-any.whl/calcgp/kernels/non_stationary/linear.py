__all__ = ["Linear"]

from dataclasses import dataclass

import jax.numpy as jnp
import tensorflow_probability.substrates.jax.bijectors as tfb
from jaxtyping import Array, Float

from calcgp.gpjax_base import param_field
from calcgp.kernels.base import AbstractKernel
from calcgp.typing import ScalarFloat


@dataclass  
class Linear(AbstractKernel):
    '''Kernel based on the dot-product of the two input vectors.
    '''
    variance: ScalarFloat = param_field(jnp.array(1.0), bijector=tfb.Softplus())

    def __call__(self, x1: Float[Array, "D"], x2: Float[Array, "D"]) -> ScalarFloat:
        '''Covariance between two function evaluations according to the dot product between the inputs.

        Parameters
        ----------
        x1 : Float[Array, "D"]
            Left hand input corresponding to a function evaluation.
        x2 : Float[Array, "D"]
            Right hand input corresponding to a function evaluation.

        Returns
        -------
        ScalarFloat
            Kernel evaluated at the inputs.
        '''
        res = self.variance * jnp.dot(x1, x2)
        return res.squeeze()