__all__ = ["Periodic"]

from dataclasses import dataclass
from typing import Union

import jax.numpy as jnp
import tensorflow_probability.substrates.jax.bijectors as tfb
from jaxtyping import Array, Float

from calcgp.gpjax_base import param_field
from calcgp.kernels.base import AbstractKernel
from calcgp.typing import ScalarFloat


@dataclass  
class Periodic(AbstractKernel):
    '''Kernel based on a periodic function.
    '''
    lengthscale: Union[ScalarFloat, Float[Array, "D"]] = param_field(jnp.array(1.0), bijector=tfb.Softplus())
    period: ScalarFloat = param_field(jnp.array(1.0), bijector=tfb.Softplus())
    variance: ScalarFloat = param_field(jnp.array(1.0), bijector=tfb.Softplus())

    
    def __call__(self, x1: Float[Array, "D"], x2: Float[Array, "D"]) -> ScalarFloat:
        '''Covariance between two function evaluations according to the periodic kernel.

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
        sine = jnp.sin(jnp.pi*(x1-x2) / self.period) / self.lengthscale
        res = self.variance * jnp.exp(-0.5*jnp.sum(sine))
        return res.squeeze()