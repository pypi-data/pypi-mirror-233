__all__ = ["Input", "Observation"]

from dataclasses import dataclass
from typing import List, Tuple, Union

import tensorflow_probability.substrates.jax.bijectors as tfb
from jaxtyping import Array, Float

from calcgp.gpjax_base import Module, param_field, static_field
from calcgp.typing import ScalarFloat, ScalarOrVector, TwoArrays


@dataclass
class Input(Module):
    '''A wrapper for array inputs to the gp model that distinguishes if the inputs represent function or gradient values.
    '''
    data: Union[TwoArrays, Float[Array, "N D"]] = static_field()
    type: str = static_field("mix")
    dims: ScalarFloat = static_field(init=False)

    def __init__(self, data: Union[TwoArrays, Float[Array, "N D"]], type: str) -> None:
        '''A wrapper for array inputs to the gp model that distinguishes if the inputs represent function or gradient values.

        Parameters
        ----------
        data : TwoArrays | Float[Array, "N D"]
            Data input array (or Iterable of 2 arrays).
        type : str, optional
            Describes if data represents function values, gradient values or both, by default "mix".
            (Possible options are "func", "grad", "mix")
        '''

        if isinstance(data, Float[Array, "N D"]) and type not in ["func", "grad"]:
            raise ValueError(f"If data is a single array, type must be either 'func' or 'grad'! Given was {self.type}")

        if isinstance(data, Union[List, Tuple]) and type != "mix":
            raise ValueError(f"If data is a two arrays, type must be either 'mix'! Given was {self.type}")

        if type == "mix":
            if data[0].shape[1] != data[1].shape[1]:
                raise ValueError(f"Both array must have the same second dimension! Got dimensions {data[0].shape[1]} and {data[1].shape[1]}.")
            
            self.dims = data[0].shape[1]
        else:
            self.dims = data.shape[1]
        
        self.type = type

        self.data = data


@dataclass
class Observation(Module):
    '''Wrapper for an observation used to update the prior distribution of a gaussian process.

    Parameters
    ----------
    X : Input
        Data points at which the target function and/or its gradient was evaluated
    Y : Float[Array, "N 1"]
        A stacked array of first the function evaluations and then the gradient evaluations.
    noise : ScalarOrVector
        An array that is either a scalar representing the global noise present in the data or a vector that links a specific noise value for each element in Y.
    '''    
    X: Input = static_field()
    Y: Float[Array, "N 1"] = static_field()
    noise: ScalarOrVector = param_field(bijector=tfb.Softplus())

    def __post_init__(self) -> None:
        self.Y.reshape(-1,1)
        try:
            self.noise.reshape(-1)
        except AttributeError:
            pass