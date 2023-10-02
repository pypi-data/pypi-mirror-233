__all__ = ["random_split", "random_subset", "grid_data", "make_pv", "make_enthalpy", "integrand_preparation"]

from jaxtyping import Float, Array
from typing import Tuple

import jax.numpy as jnp
import jax.random as jr

from calcgp.containers import Observation, Input
from calcgp.typing import ScalarFloat

A3GPA2EV = 0.0062415091 # turns P*V into units of eV

def random_split(data: Array, key: jr.KeyArray, split_size: Float, axis: int=0) -> Tuple[Array, Array]:
    '''Splits an array in two along a given axis after randomizing the array.

    Parameters
    ----------
    data : Array
        Data to be split into training and test sets.
    key : jr.KeyArray
        A jax Key used to randomize the two sets.
    split_size : Float
        Relative size of the test set.
    axis : int, optional
        Axis along which to split the given array, by default 0.

    Returns
    -------
    Tuple[Array, Array]
        The full data randomized and split in two according to split_size.
    '''
    if split_size < 0.0 or split_size > 1.0:
        raise ValueError(f"split_size must be between 0 and 1 got {split_size}!")

    perm = jr.permutation(key, data, axis=axis)

    split_ind = int(data.shape[axis]*split_size)

    return (perm.take(jnp.arange(split_ind), axis=axis), perm.take(jnp.arange(split_ind, data.shape[axis]), axis=axis))

def random_subset(data: Array, key: jr.KeyArray, subset_size: Float, axis: int=0) -> Array:
    '''Creates a random subset of the given the along the given axis.

    Parameters
    -------
    data : Array
        Array from which the random subset is created.

    key : jr.KeyArray
        A jax Key used to randomize the subset.

    subset_size : Float
        Number of elements to keep in the subset along the chosen axis.

    axis : int, optional
        The axis, along which to take the subset, by default 0.

    Returns
    -------
    Array
        The random subset array along the given axis.
    '''
    if subset_size < 0.0 or subset_size > 1.0:
        raise ValueError(f"subset_size must be between 0 and 1 got {subset_size}!")

    perm = jr.permutation(key, data, axis=axis)

    split_ind = int(data.shape[axis]*subset_size)

    return perm.take(jnp.arange(split_ind), axis=axis)

def grid_data(bounds_X: Array, bounds_Y: Array, n_X: int=50, n_Y: int=50) -> Float[Array, "n_X*n_Y 2"]:
    '''Creates an regular 2d grid of points as a (n_X*n_Y, 2) array.

    Returns
    -------
    _type_
        _description_
    '''
    P_sl = jnp.linspace(*bounds_X, n_X)
    T_sl = jnp.linspace(*bounds_Y, n_Y)

    return jnp.array(jnp.meshgrid(P_sl, T_sl)).T.reshape(-1,2)

def make_pv(PTVUdata: Float[Array, "N 6"]) -> Tuple[Float[Array, "N"], Float[Array, "N"]]:
    '''Calculates P*V and err(P*V) from a given PTVU dataset.

    Parameters
    -------
    PTVUdata : Float[Array, "N 6"]
        Data for which to calculate P*V and the corresponding error.

    Returns
    -------
    Tuple[Float[Array, "N"], Float[Array, "N"]]
        The calculated values for P*V and err(P*V)
    '''
    P = PTVUdata[:,0]
    V = PTVUdata[:,2]
    V_err = PTVUdata[:,3]

    return P*V*A3GPA2EV, P*V_err*A3GPA2EV

def make_enthalpy(PTVUdata: Float[Array, "N 6"]) -> Tuple[Float[Array, "N"], Float[Array, "N"]]:
    '''Calculates the enthalpy H and the corresponding error from a given PTVU dataset.

    Parameters
    -------
    PTVUdata : Float[Array, "N 6"]
        Data for which to calculate H and the corresponding error.

    Returns
    -------
    Tuple[Float[Array, "N"], Float[Array, "N"]]
        The calculated values for H and err(H)
    '''
    P = PTVUdata[:,0]
    V = PTVUdata[:,2]
    V_err = PTVUdata[:,3]
    U = PTVUdata[:,4]
    U_err = PTVUdata[:,5]

    H = U + P*V*A3GPA2EV
    H_err = U_err + P*V_err*A3GPA2EV

    return H, H_err

def integrand_preparation(PTVUdata: Float[Array, "N 6"], scale_Y: bool, transformation_type: str="log-log") -> Tuple[Observation, ScalarFloat]:
    '''Prepares the data to be of the correct intregrand form depending on the chosen transformation type.

    Parameters
    ----------
    PTVUdata : Float[Array, "N M"]
        Data to be prepared.
    scale_Y : bool, optional
        Flag to set if the outputs should be scaled by the maximum temperature value in PTVU_data, by default True.
    transformation_type : str, optional
        Type of transformation applied to the integration variables and the corresponding transformations of the integrand, by default "log-log".
    
        - "log-log": The integration variables are $\log(P)$ and $\log(T)$. Thus, the gradient is of the form $(PV/T, -H/T)$.
        - No other transformation currently supported.

    Returns
    -------
    Tuple[Observation, ScalarFloat]
        The corresponding Observation as needed for the posterior calculation, together with the scaling factor of the outputs.
    '''
    if transformation_type == "log-log":
        return _loglog(PTVUdata, scale_Y)
        
def _loglog(PTVUdata: Float[Array, "N 6"], scale_Y: bool) -> Tuple[Observation, ScalarFloat]:
        PV, PV_err = make_pv(PTVUdata)
        H, H_err = make_enthalpy(PTVUdata)

        if scale_Y:
            T_max = jnp.max(PTVUdata[:,1])
        else:
            T_max = 1.0
        T_scaled = PTVUdata[:,1] / T_max

        dT = - H / T_scaled
        dT_err = H_err / T_scaled
        dP = PV / T_scaled
        dP_err = PV_err / T_scaled

        X_train = Input(jnp.log(PTVUdata[:,:2]), "grad")
        Y_train = jnp.vstack((dP, dT)).T.reshape(-1,1)
        Y_err = jnp.vstack((dP_err, dT_err)).T.reshape(-1)
        
        observation = Observation(X_train, Y_train, Y_err)

        return observation, T_max