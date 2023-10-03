__all__ = ["LogMarginalLikelihood"]

from dataclasses import dataclass
from typing import Union

import jax.numpy as jnp
import jax.tree_util as jtu

from calcgp.gpjax_base import Module, static_field
from calcgp.gps import AbstractPosterior, Posterior, SparsePosterior
from calcgp.typing import ScalarFloat


@dataclass
class LogMarginalLikelihood(Module):
    '''Class used to calculate the logarithm of the marginal likelihood of a given model.
    
    Parameters
    -------
    negative : bool
        Boolean value used decide if the positive or negative LML should be calculated.
    '''
    negative: bool = static_field(False)
    constant: ScalarFloat = static_field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.constant = jnp.array(-1.0) if self.negative else jnp.array(1.0)
    
    def __call__(self, posterior: AbstractPosterior) -> ScalarFloat:
        '''Calculates the logarithm of the marginal liklihood of a given posterior.

        Parameters
        ----------
        posterior : Posterior | SparsePosterior
            Posterior for which the LML should be calculated.

        Returns
        -------
        ScalarFloat
            Value of the LML of the given posterior divided by the number of samples.
            (Maybe gives better behaviour of the optimization.)
        ''' 
        return self.forward(posterior)

    def __hash__(self):
        '''Creates a simple hash of the class which is necessary to jit-compile it for the optimization.
        '''        
        return hash(tuple(jtu.tree_leaves(self)))

    def forward(self, posterior: Union[Posterior, SparsePosterior]):
        '''Calculates the logarithm of the marginal liklihood of a given posterior.

        Parameters
        ----------
        posterior : Posterior | SparsePosterior
            Posterior for which the LML should be calculated.

        Returns
        -------
        ScalarFloat
            Value of the LML of the given posterior divided by the number of samples.
            (Maybe gives better behaviour of the optimization.)
        '''        
        X = posterior.observation.X
        Y = posterior.observation.Y
        noise = posterior.observation.noise

        prior_dist = posterior.prior(X)

        log_prob = prior_dist.log_prob(Y, noise)

        return self.constant * log_prob.squeeze() / len(Y)