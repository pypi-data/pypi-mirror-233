__all__ = ["AbstractPrior", "Prior", "SparsePrior", "AbstractPosterior", "Posterior", "SparsePosterior", "InducingSet", "sparsify"]

from abc import abstractmethod
from dataclasses import dataclass
from typing import Tuple, Union

import jax.numpy as jnp
import jax.scipy as jsp
import tensorflow_probability.substrates.jax.bijectors as tfb
from jax import vmap
from jaxtyping import Array, Float

from calcgp.containers import Input, Observation
from calcgp.distributions import (
    AbstractMultivariateNormal, 
    MultivariateNormal, 
    SparseMultivariateNormal
)
from calcgp.gpjax_base import Module, param_field, static_field
from calcgp.kernels.base import AbstractKernel
from calcgp.mean_functions import AbstractMean
from calcgp.typing import ScalarFloat
from calcgp.utils import inner_map, matmul_diag

# -------------------------------------------------------------------
# Priors

@dataclass
class AbstractPrior(Module):
    '''Abstract base class for the calculation of a prior distribution.

    Parameters
    -------
    mean : AbstractMean
        Mean function used to calculate the prior.
    covariance : AbstractKernel
        Covariance function (Kernel) used to calculate the prior.
    jitter : ScalarFloat
        A small value added to the diagonal in order to make the computation more stable.
        (Should not be changed unless there is no other way to make the posterior calculation work.)
    '''
    mean: AbstractMean
    covariance: AbstractKernel
    jitter: ScalarFloat = static_field(default=1e-6)

    def __call__(self, test_inputs: Input) -> AbstractMultivariateNormal:
        '''Returns a multivariate normal distribution over the given inputs.

        Parameters
        ----------
        test_inputs : Input
            Inputs at which to evalute the mean and covariance functions.

        Returns
        -------
        AbstractMultivariateNormal
            Multivariate normal distribution over the given inputs.
        '''
        return self.forward(test_inputs)

    @abstractmethod
    def forward(self, test_inputs: Input) -> AbstractMultivariateNormal:
        '''Returns a multivariate normal distribution over the given inputs.

        Parameters
        ----------
        test_inputs : Input
            Inputs at which to evalute the mean and covariance functions.

        Returns
        -------
        AbstractMultivariateNormal
            Multivariate normal distribution over the given inputs.
        '''
        raise NotImplementedError
    
    @abstractmethod
    def __mul__(self, other: Observation) -> "AbstractPosterior":
        '''To mimic the mathematical expression of the posterior distribution multiplying a posterior can be created by multiplying a prior and an observation.

        Parameters
        ----------
        other : Observation
            Observation to be used to create a posterior distribution.

        Returns
        -------
        AbstractPosterior
            Posterior that combines the given prior and observation.
        '''        
        return NotImplemented

    def __rmul__(self, other: Observation) -> "AbstractPosterior":
        '''To mimic the mathematical expression of the posterior distribution multiplying a posterior can be created by multiplying a prior and an observation.

        Parameters
        ----------
        other : Observation
            Observation to be used to create a posterior distribution.

        Returns
        -------
        AbstractPosterior
            Posterior that combines the given prior and observation.
        '''   
        return self.__mul__(other)


@dataclass
class Prior(AbstractPrior):
    '''A class for calculating the prior over given data.

    Parameters
    -------
    mean : AbstractMean
        Mean function used to calculate the prior.
    covariance : AbstractKernel
        Covariance function (Kernel) used to calculate the prior.
    jitter : ScalarFloat
        A small value added to the diagonal in order to make the computation more stable.
        (Should not be changed unless there is no other way to make the posterior calculation work.)
    '''

    def forward(self, test_inputs: Input) -> MultivariateNormal:
        '''Returns a multivariate normal distribution over the given inputs.

        Parameters
        ----------
        test_inputs : Input
            Inputs at which to evalute the mean and covariance functions.

        Returns
        -------
        MultivariateNormal
            Multivariate normal distribution over the given inputs.
        '''
        m_x = self.mean.mean_vector(test_inputs)
        K_xx = self.covariance.gram_matrix(test_inputs)

        diag = jnp.diag_indices(len(K_xx))
        K_xx = K_xx.at[diag].add(self.jitter)

        return MultivariateNormal(m_x, K_xx)
    
    def __mul__(self, other: "Observation") -> "Posterior":
        '''To mimic the mathematical expression of the posterior distribution multiplying a posterior can be created by multiplying a prior and an observation.

        Parameters
        ----------
        other : Observation
            Observation to be used to create a posterior distribution.

        Returns
        -------
        Posterior
            Posterior that combines the given prior and observation.
        '''  
        return Posterior(other, self)


@dataclass
class SparsePrior(AbstractPrior):
    '''A class used to calculate the sparsified prior distribution over given data.

    Parameters
    -------
    mean : AbstractMean
        Mean function used to calculate the prior.
    covariance : AbstractKernel
        Covariance function (Kernel) used to calculate the prior.
    jitter : ScalarFloat
        A small value added to the diagonal in order to make the computation more stable.
        (Should not be changed unless there is no other way to make the posterior calculation work.)
    inducing_set : InducingSet
        Inducing set used to sparsify the prior.
    '''
    inducing_set: "InducingSet" = None

    def __post_init__(self) -> None:
        if self.inducing_set is None:
            raise TypeError("An inducing set must be given!")

    def forward(self, test_inputs: Input) -> SparseMultivariateNormal:
        '''Returns a sparsified multivariate normal distribution over the given inputs.

        Parameters
        ----------
        test_inputs : Input
            Inputs at which to evalute the mean and covariance functions.

        Returns
        -------
        SparseMultivariateNormal
            Sparsified multivariate normal distribution over the given inputs.
        '''
        # mean is not sparsified
        m_x = self.mean.mean_vector(test_inputs)

        # gram matrix for the inducing set
        K_uu = self.covariance.gram_matrix(self.inducing_set.to_Input())
        diag = jnp.diag_indices(len(K_uu))
        K_uu = K_uu.at[diag].add(self.jitter)

        # Lower cholesky factor of K_uu
        L_uu = jsp.linalg.cholesky(K_uu, lower=True)

        # covariance between inducing set and test inputs
        K_ux = self.covariance.covariance_matrix(self.inducing_set.to_Input(), test_inputs)

        # FIC approximation: K_xx approx. Q_xx - diag(Q_xx - K_xx), Q_xx = K_ux.T @ (K_uu)**(-1) @ K_ux
        # Q_xx = V.T @ V
        V = jsp.linalg.solve_triangular(L_uu, K_ux, lower=True)
        Q_xx_diag = vmap(lambda x: x.T@x, in_axes=(1,))(V)
        K_xx_diag = self.covariance.gram_diagonal(test_inputs)
        fic_diag = Q_xx_diag - K_xx_diag

        return SparseMultivariateNormal(m_x, V, fic_diag, L_uu)
    
    def __mul__(self, other: "Observation") -> "SparsePosterior":
        '''To mimic the mathematical expression of the posterior distribution multiplying a posterior can be created by multiplying a prior and an observation.

        Parameters
        ----------
        other : Observation
            Observation to be used to create a posterior distribution.

        Returns
        -------
        Posterior
            SparsePosterior that combines the given prior and observation.
        '''  
        return SparsePosterior(other, self)


# -------------------------------------------------------------------
# Posteriors

@dataclass
class AbstractPosterior(Module):
    '''A base class for calculating the posterior distribution of given data with respect to another observation.
    '''
    observation: Observation

    def __call__(self, test_inputs: Input) -> Tuple[Float[Array, "N"], Float[Array, "N"]]:
        '''Calculates the posterior distribution of given data with respect to another observation.

        Parameters
        -------
        test_inputs : Input
            Inputs at which to calculate the posterior distribution.

        Returns
        -------
        Tuple[Float[Array, "N"], Float[Array, "N"]]
            A tuple of two arrays representing the mean and stddev of the resulting posterior distribution.
        '''        
        return self.forward(test_inputs)

    @abstractmethod
    def forward(self, test_inputs: Input) -> Tuple[Float[Array, "N"], Float[Array, "N"]]:
        '''Calculates the posterior distribution of given data with respect to another observation.

        Parameters
        -------
        test_inputs : Input
            Inputs at which to calculate the posterior distribution.

        Returns
        -------
        Tuple[Float[Array, "N"], Float[Array, "N"]]
            A tuple of two arrays representing the mean and stddev of the resulting posterior distribution.
        '''  
        raise NotImplementedError

@dataclass
class Posterior(AbstractPosterior):
    '''A class for calculating the posterior distribution of given data with respect to another observation.

    Parameters
    -------
    observation : Observation
        Previous observation used to update the probabilties of the prior distribution.
    prior : Prior
        Prior distribution that is to be updated via the previous observation.
    '''
    prior: Prior

    def forward(self, test_inputs: Input) -> Tuple[Float[Array, "N"], Float[Array, "N"]]:
        '''Calculates the posterior distribution of given data with respect to another observation.

        Parameters
        -------
        test_inputs : Input
            Inputs at which to calculate the posterior distribution.

        Returns
        -------
        Tuple[Float[Array, "N"], Float[Array, "N"]]
            A tuple of two arrays representing the mean and stddev of the resulting posterior distribution.
        '''  
        # calculate mean and covariance of prior distribution
        prior_distr = self.prior(self.observation.X)

        m_x = prior_distr.mean()

        # add the observational noise to the prior covariance
        K_xx = prior_distr.covariance()
        diag = jnp.diag_indices(len(K_xx))
        K_xx = K_xx.at[diag].add(self.observation.noise**2)

        # lower cholesky factor of K_xx
        L_xx = jsp.linalg.cholesky(K_xx, lower=True)

        # covariance between test inputs and observations
        K_tx = self.prior.covariance.covariance_matrix(test_inputs, self.observation.X)

        # covariance between the different test inputs
        K_tt_diag = self.prior.covariance.gram_diagonal(test_inputs)

        # posterior mean via K_tx @ (K_xx)**(-1) @ (Y - m_x)
        m_t = self.prior.mean.mean_vector(test_inputs)
        mean = m_t + K_tx@jsp.linalg.cho_solve((L_xx, True), self.observation.Y - m_x)

        # diag(K_tx @ (K_xx)**(-1) @ K_tx.T)
        K_txt_diag = inner_map(L_xx, K_tx.T)
        
        # posterior std
        stddef = jnp.sqrt(K_tt_diag - K_txt_diag)

        return (mean.squeeze(), stddef.squeeze())


@dataclass
class SparsePosterior(AbstractPosterior):
    '''A class for calculating the sparse posterior distribution of given data with respect to another observation.

    Parameters
    -------
    observation : Observation
        Previous observation used to update the probabilties of the prior distribution.
    prior : SparsePrior
        Sparse prior distribution that is to be updated via the previous observation.
    '''
    prior: SparsePrior

    def forward(self, test_inputs: Input) -> Tuple[Float[Array, "N"], Float[Array, "N"]]:
        '''Calculates the sparified posterior distribution of given data with respect to another observation.

        Parameters
        -------
        test_inputs : Input
            Inputs at which to calculate the posterior distribution.

        Returns
        -------
        Tuple[Float[Array, "N"], Float[Array, "N"]]
            A tuple of two arrays representing the mean and stddev of the resulting sparse posterior distribution.
        '''  
        # calculate the sparse prior for the given observations
        prior_dist = self.prior(self.observation.X)

        # Lambda = fic_diag + noise**2
        Lambda = self.observation.noise**2 - prior_dist.fic_diag

        # solve the inner matrix to be inverted
        # V.T @ Lambda**(-1) @ V + id
        V_scaled = matmul_diag(1 / jnp.sqrt(Lambda), prior_dist.scale.T)
        K_inner = V_scaled.T@V_scaled
        diag = jnp.diag_indices(len(K_inner))
        K_inner = K_inner.at[diag].add(1.0)

        # cholesky factor of the inner matrix
        L_inner = jsp.linalg.cholesky(K_inner, lower=True)

        # projected Y onto u-space via K_ut @ Lambda**(-1) @ (Y - m_x)
        m_x = prior_dist.mean()
        Y_u = (self.observation.Y - prior_dist.mean()) / Lambda.reshape(-1,1)
        Y_u = prior_dist.scale @ Y_u

        # covariance between u and test inputs
        K_ut = self.prior.covariance.covariance_matrix(self.prior.inducing_set.to_Input(), test_inputs)
        # V factor for the new inputs
        V_ut = jsp.linalg.solve_triangular(prior_dist.L_uu, K_ut, lower=True)

        # posterior mean
        m_t = self.prior.mean.mean_vector(test_inputs)
        mean = m_t + V_ut.T@jsp.linalg.cho_solve((L_inner, True), Y_u)

        # posterior std
        K_tt_diag = self.prior.covariance.gram_diagonal(test_inputs)
        Q_tt_diag = vmap(lambda x: x.T@x, in_axes=(1,))(V_ut)
        K_tut_diag = inner_map(L_inner, V_ut)

        stddef = jnp.sqrt(K_tt_diag - Q_tt_diag + K_tut_diag)

        return (mean.squeeze(), stddef.squeeze())


# -------------------------------------------------------------------
# Sparsify
    
@dataclass
class InducingSet(Module):
    '''A container used to hold an inducing set that can be optimized over.
    
    Parameters
    -------
    X : Float[Array, "N D"]
        Array used as the inducing set. 
        
    The positions of the indiviual inducing points can be optimized, but not the overall number of inducing points.
    '''
    X: Float[Array, "N D"] = param_field(bijector=tfb.Identity())
    
    def to_Input(self) -> Input:
        '''Transforms the inducing set into an Input that represents function values.

        Returns
        -------
        Input
            An Input containing the same points as the inducing set.
        '''        
        return Input(self.X, "func")

def sparsify(inducing_set: Union[InducingSet, Float[Array, "N D"]], model: Union[Prior, Posterior]) -> Union[SparsePrior, SparsePosterior]:
    '''Sparsifies a given model by adding the given inducing set to the prior.

    - If the model is a prior model the inducing set is added to the model.
    - If the model is a posterior the inducing set is added to the prior contained in the posterior.
    - If the model is neither the model is just return without any modifications.

    Parameters
    ----------
    inducing_set : InducingSet | Float[Array, "N D"]
        Inducing set used to sparsify the given model
    model : Prior | Posterior
        Model to be sparsified.

    Returns
    -------
    SparsePrior or SparsePosterior
        The given model sparsified by adding the given inducing set.
    '''
    if isinstance(inducing_set, Array):
        inducing_set = InducingSet(inducing_set)

    if isinstance(model, Prior):
        return SparsePrior(model.mean, model.covariance, model.jitter, inducing_set)
    
    if isinstance(model, Posterior):
        sp_prior = SparsePrior(model.prior.mean, model.prior.covariance, model.prior.jitter, inducing_set)
        return SparsePosterior(model.observation, sp_prior)
    
    return model