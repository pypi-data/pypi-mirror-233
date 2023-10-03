__all__ = ["GibbsModel"]

import jax.numpy as jnp
from jaxtyping import Float, Array
from typing import Tuple
from jaxopt._src.base import IterativeSolver as JaxoptSolver

from calcgp.containers import Input
from calcgp.gps import InducingSet, Prior, sparsify
from calcgp.kernels import RBF
from calcgp.likelihood import LogMarginalLikelihood
from calcgp.mean_functions import ConstantMean
from calcgp.optimize import optimize
from calcgp.td_integration.data_functions import integrand_preparation


class GibbsModel():
    '''A model used to find the gibbs free energy from given PTVU data.'''
    def __init__(self, inducing_points: Float[Array, "N D"], optimizer: JaxoptSolver, num_iters: int) -> None:
        # Fitting
        self.inducing_points = inducing_points
        self.mll = LogMarginalLikelihood(negative=True)

        self.optimizer = optimizer
        self.num_iters = num_iters
    
    def fit(self, train_data: Float[Array, "N 6"]) -> Float[Array, "M"]:
        '''Optimizes a sparse gpr model via the given training data.

        Parameters
        -------
        train_data : Float[Array, "N 6"]
            PTVU data used for fitting the sparse gpr model for the gibbs free energy.

        Returns
        -------
        Float[Array, "M"]
            Loss of the optimization process for each iteration.
        '''
        # Training data
        observation, self.T_max = integrand_preparation(train_data, scale_Y=True) 
        observation = observation.replace_trainable(noise=False)

        # Model
        prior = Prior(ConstantMean(), RBF())
        self.posterior = sparsify(InducingSet(jnp.log(self.inducing_points)), prior * observation)

        # optimization
        optim_post, history = optimize(self.mll, self.optimizer, self.posterior, self.num_iters)
        self.optimized_posterior = optim_post

        return history
    
    def predict(self, PT_grid: Float[Array, "N 2"]) -> Tuple[Float[Array, "N"], Float[Array, "N"]]:
        '''Predicts the values of the gibbs free energy on a given PT grid.

        Parameters
        ----------
        PT_grid : Float[Array, "N 2"]
            PT grid on which G/T is predicted.

        Returns
        -------
        Tuple[Float[Array, "N"], Float[Array, "N"]]
            Predicted function values and errors of the gibbs free energy on the given grid.
        '''
        test_inputs = Input(jnp.log(PT_grid), "func")

        if not hasattr(self, "optimized_posterior"):
            raise ValueError("Can't call predict before fitting!")
        
        mean, std = self.optimized_posterior(test_inputs)

        mean /= self.T_max
        std /= self.T_max

        return  mean, std