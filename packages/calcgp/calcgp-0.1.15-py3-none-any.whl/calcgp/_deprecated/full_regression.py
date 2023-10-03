from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, Union

import jax.numpy as jnp
from jax import jit
from jax.numpy import ndarray
from jax.tree_util import register_pytree_node_class, tree_map

from .covar import DataMode, Prior
from .distributions import PosteriorDistribution
from .kernels import Kernel
from .likelihood import NegativeLogMarginalLikelihood
from .logger import Logger
from .posterior import Posterior
from .optimizer import OptimizerTypes, parameter_optimize


@register_pytree_node_class
@dataclass
class FullGPRBase(ABC):
    kernel: Kernel
    kernel_params: Union[float, ndarray] = jnp.log(2)
    noise: Union[float, ndarray] = jnp.log(2)
    optim_method: OptimizerTypes = OptimizerTypes.SLSQP
    optim_noise: bool = False
    logger: Logger = None

    def __post_init__(self):
        if jnp.isscalar(self.kernel_params):
            self.kernel_params = tree_map(lambda x: x*self.kernel_params, self.kernel.param_tree_base())

        self.prior_result = None
        self.nlml = NegativeLogMarginalLikelihood()

    @abstractmethod
    def train(self, X_data, Y_data):
        pass

    @abstractmethod
    def predict(self, X_test):
        pass

    def _train(self, X_data, Y_data):
        prior_func = self.prior()
        nlml_func = self.nlml()

        if self.optim_noise:
            def optim_fun(params):
                return nlml_func(prior_func(X_data, Y_data, self.kernel, *params))
        
            lb = (jnp.ones_like(self.kernel_params)*1e-3, jnp.ones_like(self.noise)*1e-3)
            ub = (jnp.ones_like(self.kernel_params)*jnp.inf, jnp.ones_like(self.noise)*jnp.inf)

            bounds = (lb, ub)

            init_params = (self.kernel_params, self.noise)

        else:
            def optim_fun(params):
                return nlml_func(prior_func(X_data, Y_data, self.kernel, params, self.noise))
        
            bounds = (1e-3, jnp.inf)  

            init_params = self.kernel_params

        optimized_params = parameter_optimize(fun=optim_fun,
                                              params=init_params,
                                              bounds=bounds,
                                              method=self.optim_method,
                                              callback=self.logger,
                                              jit_fun=True)
        
        if self.optim_noise:
            self.kernel_params, self.noise = optimized_params
        else:
            self.kernel_params = optimized_params

        self.prior_result = jit(prior_func)(X_data, Y_data, self.kernel, self.kernel_params, self.noise)

    def _predict(self, X_test):
        post_func = self.posterior()

        return jit(post_func)(X_test, self.prior_result, self.kernel, self.kernel_params)
    
    def tree_flatten(self):
        '''necessary for this class to be an argument in a jitted function (jax)
        '''
        return ((self.kernel, 
                 self.kernel_params,
                 self.noise,
                 self.optim_method,
                 self.optim_noise,
                 self.logger,
                 self.prior,
                 self.prior_result), 
                None)
    
    @classmethod
    def tree_unflatten(cls, aux_data, children):
        '''necessary for this class to be an argument in a jitted function (jax)
        '''
        new_class = cls(*children[:-2])
        new_class.prior = children[-2]
        new_class.prior_result = children[-1]
        return new_class


@register_pytree_node_class
@dataclass
class FullGradient(FullGPRBase):
    '''A model that predicts gradient values from observations of the function.
    '''
    def train(self, X_data, Y_data):
        if isinstance(X_data, Tuple):
            self.prior = Prior(mode=DataMode.MIX)
        else:
            self.prior = Prior(mode=DataMode.FUNC)

        return self._train(X_data, Y_data)
    
    def predict(self, X_test):
        self.posterior = Posterior(prior_mode=self.prior.mode, posterior_mode=DataMode.GRAD)

        mean, std = self._predict(X_test)

        mean = mean.reshape(X_test.shape)
        std = std.reshape(X_test.shape)

        return PosteriorDistribution(mean, std)


@register_pytree_node_class
@dataclass
class FullIntegral(FullGPRBase):
    '''A model that predicts function values from observations of the gradient.
    '''
    def train(self, X_data, Y_data):
        if isinstance(X_data, Tuple):
            self.prior = Prior(mode=DataMode.MIX)
        else:
            self.prior = Prior(mode=DataMode.GRAD)

        return self._train(X_data, Y_data)
    
    def predict(self, X_test):
        self.posterior = Posterior(prior_mode=self.prior.mode, posterior_mode=DataMode.FUNC)

        return self._predict(X_test)



@register_pytree_node_class    
@dataclass
class FullFunction(FullGPRBase):
    '''A model that predicts function values from observations of the function.
    '''
    def train(self, X_data, Y_data):
        self.prior = Prior(mode=DataMode.FUNC)

        return self._train(X_data, Y_data)
    
    def predict(self, X_test):
        self.posterior = Posterior(prior_mode=self.prior.mode, posterior_mode=DataMode.FUNC)

        return self._predict(X_test)