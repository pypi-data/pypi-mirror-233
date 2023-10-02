__all__ = ["RBF"]

from dataclasses import dataclass
from typing import Union

import jax.numpy as jnp
import tensorflow_probability.substrates.jax.bijectors as tfb
from jaxtyping import Array, Float

from calcgp.gpjax_base import param_field
from calcgp.kernels.base import AbstractKernel
from calcgp.typing import ScalarFloat


@dataclass
class RBF(AbstractKernel):
    '''Kernel based on radial basis function / gaussian
    '''
    lengthscale: Union[ScalarFloat, Float[Array, "D"]] = param_field(jnp.array(1.0), bijector=tfb.Softplus())
    variance: ScalarFloat = param_field(jnp.array(1.0), bijector=tfb.Softplus())
    
    def __call__(self, x1: Float[Array, "D"], x2: Float[Array, "D"]) -> ScalarFloat:
        '''Covariance between two function evaluations according to a gaussian distribution.

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
        diff = (x1 - x2) / self.lengthscale
        res = self.variance * jnp.exp(-0.5*jnp.dot(diff, diff))
        return res.squeeze()