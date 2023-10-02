__all__ = ["optimize"]

from typing import Callable, Union

import jax
import jax.numpy as jnp
from jaxopt._src.base import IterativeSolver

from calcgp.gpjax_base import Module


def optimize(
        fun: Union[Module, Callable], 
        solver: IterativeSolver, 
        model: Module,
        num_iter: int = 500,
        ) -> Module:
    '''A function running the optimization of the parameter of the given model by minimzing the given loss function.

    Parameters
    ----------
    fun : Module | Callable
        Function that calculates the loss associated with the given model.
    solver : IterativeSolver
        The solver used for the minimization procedure.
        Supported are iterative solvers from the "jaxopt" package.
    model : Module
        The inital model which is to be optimized with respect to the given loss function.
    num_iter : int, optional
        Number of steps to be run of the given solver, by default 500.

    Returns
    -------
    Module
        A model with the same structure as the initial model but with optimized parameters.
    '''    
    def loss(model):
        # stop gradient calculation for leaves flagged as not trainable
        model = model.stop_gradient()
        # return objective evaluated at the contrained model
        return fun(model.constrain())
    
    # jaxopt needs all parameters to be of the same type and thus floats have to be turned into 0-d arrays
    def prepare(pytree):
        def vectorize(x):
            return jnp.array(x)
        
        return jax.tree_map(vectorize, pytree)

    model = prepare(model)
    model = model.unconstrain()

    solver = solver(loss)

    state = solver.init_state(model)

    iters = jnp.arange(num_iter)

    def step(carry, iter):
        model, state = carry

        loss_val = loss(model)

        model, state = solver.update(model, state)

        carry = (model, state)
        return carry, loss_val
    
    (optim_model, _), loss_history = jax.lax.scan(step, (model, state), iters) 

    return optim_model.constrain(), loss_history