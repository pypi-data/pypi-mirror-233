__all__ = ["AbstractMultivariateNormal", "MultivariateNormal", "SparseMultivariateNormal"]

from dataclasses import dataclass
from abc import abstractmethod

import jax.numpy as jnp
import jax.scipy as jsp
from jaxtyping import Array, Float
from jax import vmap

from calcgp.gpjax_base import Module
from calcgp.typing import ScalarFloat, ScalarOrVector
from calcgp.utils import matmul_diag


@dataclass
class AbstractMultivariateNormal(Module):
    '''Abstract base class for a multi variate normal distribution.
    '''
    @abstractmethod
    def mean(self) -> Float[Array, "N 1"]:
        '''Returns the mean of the given distribution.

        Returns
        ------
        Float[Array, "N 1"]
            Mean of the distribution.
        '''        
        raise NotImplementedError
    
    @abstractmethod
    def covariance(self) -> Float[Array, "N N"]:
        '''Returns the covariance matrix of the given distribution.

        Returns
        ------
        Float[Array, "N 1"]
            Covariance of the distribution.
        '''   
        raise NotImplementedError
    
    @abstractmethod
    def stddev(self) -> Float[Array, "N 1"]:
        '''Returns the standard deviation (sqrt of the diagonal of the covariance matrix) of the given distribution.

        Returns
        ------
        Float[Array, "N 1"]
            Standard deviation of the distribution.
        '''     
        raise NotImplementedError
    
    @abstractmethod
    def log_prob(self, Y: Float[Array, "N 1"], noise: ScalarOrVector = jnp.zeros(1)) -> ScalarFloat:
        '''Calculates the log of the probability of a given (possibly noisy) sample.

        Parameters
        ----------
        Y : Float[Array, "N 1"]
            Possibly noisy sample of which to calculate the log probability.
        noise : ScalarOrVector, optional
            Additional gaussian noise present in the given sample, by default jnp.zeros(1).

        Returns
        -------
        ScalarFloat
            The log probability of the given sample.
        '''        
        raise NotImplementedError


@dataclass
class MultivariateNormal(AbstractMultivariateNormal):
    '''A multivariate normal distribution.

    Parameters
    -------
    loc : Float[Array, "N 1"]
        Mean vector of the distribution.
    covariance_matrix : Float[Array, "N N"]
        Covariance matrix of the distribution.
    '''    
    loc: Float[Array, "N 1"]
    covariance_matrix: Float[Array, "N N"]

    def __post_init__(self) -> None:
        if len(self.loc.shape) < 2:
            self.loc = self.loc.reshape(-1,1)
    
    def mean(self) -> Float[Array, "N 1"]:
        '''Returns the mean of the given distribution.

        Returns
        ------
        Float[Array, "N 1"]
            Mean of the distribution.
        '''        
        return self.loc
    
    def covariance(self) -> Float[Array, "N N"]:
        '''Returns the covariance matrix of the given distribution.

        Returns
        ------
        Float[Array, "N N"]
            Covariance of the distribution.
        '''   
        return self.covariance_matrix
    
    def stddev(self) -> Float[Array, "N 1"]:
        '''Returns the standard deviation (sqrt of the diagonal of the covariance matrix) of the given distribution.

        Returns
        ------
        Float[Array, "N 1"]
            Standard deviation of the distribution.
        '''

        return jnp.sqrt(jnp.diag(self.covariance_matrix)).reshape(-1,1)

    def log_prob(self, Y: Float[Array, "N 1"], noise: Float[Array, "N"] = jnp.zeros(1)) -> ScalarFloat:
        '''Calculates the log of the probability of a given (possibly noisy) sample.

        Parameters
        ----------
        Y : Float[Array, "N 1"]
            Possibly noisy sample of which to calculate the log probability.
        noise : ScalarOrVector, optional
            Additional gaussian noise present in the given sample, by default jnp.zeros(1).

        Returns
        -------
        ScalarFloat
            The log probability of the given sample.
        '''    
        K_xx = self.covariance_matrix
        diag = jnp.diag_indices(len(K_xx))
        K_xx = K_xx.at[diag].add(noise**2)

        # lower cholesky factor of K_xx
        L_xx = jsp.linalg.cholesky(K_xx, lower=True)

        L_xx_diag = jnp.diag(L_xx)
        log_det = 2*jnp.sum(jnp.log(L_xx_diag))

        fit = Y.T @ jsp.linalg.cho_solve((L_xx, True), Y)

        log_prob = -0.5*(log_det + fit + len(Y)*jnp.log(2*jnp.pi))

        return log_prob

@dataclass
class SparseMultivariateNormal(AbstractMultivariateNormal):
    '''A sparse approximation of a multivariate normal distribution.

    Parameters
    ----------
    loc : Float[Array, "N 1"]
        The full mean vector of the distribution.
    scale : Float[Array, "M N"]
        "Square root" of the covariance matrix.
    fic_diag : Float[Array, "N"]
        Additional diagonal offset to be subtracted from scale @ scale.T
    L_uu : Float[Array, "M M"]
        Additional factor needed for the calculation of the posterior.
    '''    
    loc: Float[Array, "N 1"]
    scale: Float[Array, "M N"]
    fic_diag: Float[Array, "N"]
    L_uu: Float[Array, "M M"]

    def __post_init__(self) -> None:
        if len(self.loc.shape) < 2:
            self.loc = self.loc.reshape(-1,1)
    
    def mean(self) -> Float[Array, "N 1"]:
        '''Returns the mean of the given distribution.

        Returns
        ------
        Float[Array, "N 1"]
            Mean of the distribution.
        '''        
        return self.loc
    
    def covariance(self) -> Float[Array, "N N"]:
        '''Returns the covariance matrix of the given distribution.

        Returns
        ------
        Float[Array, "N N"]
            Covariance of the distribution.
        '''   
        Q_xx = self.scale @ self.scale.T

        diag = jnp.diag_indices(len(Q_xx))
        return Q_xx.at[diag].add(-self.fic_diag)
    
    def stddev(self) -> Float[Array, "N 1"]:
        '''Returns the standard deviation (sqrt of the diagonal of the covariance matrix) of the given distribution.

        Returns
        ------
        Float[Array, "N 1"]
            Standard deviation of the distribution.
        '''
        Q_xx_diag = vmap(lambda x: x.T@x, in_axes=(1,))(self.scale)

        return jnp.sqrt(Q_xx_diag - self.fic_diag).reshape(-1,1)

    def log_prob(self, Y: Float[Array, "N 1"], noise: Float[Array, "N"]) -> ScalarFloat:
        '''Calculates the log of the probability of a given (possibly noisy) sample.

        Parameters
        ----------
        Y : Float[Array, "N 1"]
            Possibly noisy sample of which to calculate the log probability.
        noise : Optional[ScalarOrVector]
            Additional gaussian noise present in the given sample. Per default 0.

        Returns
        -------
        ScalarFloat
            The log probability of the given sample.
        ''' 
        Lambda = noise**2 - self.fic_diag

        # solve the inner matrix to be inverted
        # V.T @ Lambda**(-1) @ V + id
        V_scaled = matmul_diag(1 / jnp.sqrt(Lambda), self.scale.T)
        K_inner = V_scaled.T@V_scaled
        diag = jnp.diag_indices(len(K_inner))
        K_inner = K_inner.at[diag].add(1.0)

        # cholesky factor of the inner matrix
        L_inner = jsp.linalg.cholesky(K_inner, lower=True)

        L_inner_diag = jnp.diag(L_inner)
        log_det_inner = 2*jnp.sum(jnp.log(L_inner_diag))

        logdet_Lambda = jnp.sum(jnp.log(Lambda))

        Y_scaled = (Y - self.loc) / jnp.sqrt(Lambda.reshape(-1,1))
        sqrt_fit = jsp.linalg.solve_triangular(L_inner, self.scale@((Y - self.loc) / Lambda.reshape(-1,1)), lower=True)
        fit = Y_scaled.T@Y_scaled - sqrt_fit.T@sqrt_fit

        log_prob = -0.5*(log_det_inner + logdet_Lambda + fit + len(Y)*jnp.log(2*jnp.pi))

        return log_prob