__all__ = ["cut_plot_above_curve", "cut_plot_above_curve", "min_nan", "max_nan", "greater_nan", "less_nan"]

import jax.numpy as jnp
from jaxtyping import Array, Float


def _cutoff(X, TM, shift):
    def _interp1d(x, TM):
        return jnp.interp(x, TM[:,0], TM[:,1])
    
    return _interp1d(X[:,0], TM) - X[:,1] + shift

def cut_plot_above_curve(plot_vals: Float[Array, "N 2"], plot_grid: Float[Array, "N 2"], line_points: Float[Array, "M 2"], shift: Float = 0.0) -> Float[Array, "N 2"]:
    '''A plotting helper function that replaces all function values on a grid by NAN if they are lying ABOVE a certain curve.

    Parameters
    ----------
    plot_vals : Float[Array, "N 2"]
        Function values to be replaced depending on where on the grid they lie.
    plot_grid : Float[Array, "N 2"]
        Grid points describing the positions of the above function values.
    line_points : Float[Array, "M 2"]
        Points describing a curve in 2D. Any function values where the corresponding location in plot_grid is above the given function will be set to NAN.
    shift : Float, optional
        Optional shift to be applied to the line points, i.e., if shift=1.0, only points that lie 1.0 above the given curve will be set to NAN.

    Returns
    -------
    Float[Array, "N 2"]
        Array of the same shape as plot_vals with certain elements replaced by NAN.
    '''
    return jnp.where(_cutoff(plot_grid, line_points, shift)<0.0, jnp.nan, plot_vals)

def cut_plot_below_curve(plot_vals: Float[Array, "N 2"], plot_grid: Float[Array, "N 2"], line_points: Float[Array, "M 2"], shift: Float = 0.0) -> Float[Array, "N 2"]:
    '''A plotting helper function that replaces all function values on a grid by NAN if they are lying BELOW a certain curve.

    Parameters
    ----------
    plot_vals : Float[Array, "N 2"]
        Function values to be replaced depending on where on the grid they lie.
    plot_grid : Float[Array, "N 2"]
        Grid points describing the positions of the below function values.
    line_points : Float[Array, "M 2"]
        Points describing a curve in 2D. Any function values where the corresponding location in plot_grid is below the given function will be set to NAN.
    shift : Float, optional
        Optional shift to be applied to the line points, i.e., if shift=1.0, only points that lie 1.0 below the given curve will be set to NAN.

    Returns
    -------
    Float[Array, "N 2"]
        Array of the same shape as plot_vals with certain elements replaced by NAN.
    '''
    return jnp.where(_cutoff(plot_grid, line_points, shift)>0.0, jnp.nan, plot_vals)

def min_nan(X: Float[Array, "..."], axis: int=None) -> Float[Array, "..."]:
    '''Wrapper around jnp.min that ignores NAN values in the given array.

    Parameters
    ----------
    X : Float[Array, "..."]
        Array over which to find the minimum.
    
    axis : int, optional
        Axis over which to calculate the minimum, by default None. If None finds the minimum of the flattened array.

    Returns
    -------
    Float[Array, "..."]
        Resulting array holding the minimum values.
    '''
    X = jnp.where(jnp.isnan(X), jnp.inf, X)
    return jnp.min(X, axis=axis)

def max_nan(X: Float[Array, "..."], axis: int=None) -> Float[Array, "..."]:
    '''Wrapper around jnp.max that ignores NAN values in the given array.

    Parameters
    ----------
    X : Float[Array, "..."]
        Array over which to find the maximum.
    
    axis : int, optional
        Axis over which to calculate the maximum, by default None. If None finds the maximum of the flattened array.

    Returns
    -------
    Float[Array, "..."]
        Resulting array holding the maximum values.
    '''
    X = jnp.where(jnp.isnan(X), -jnp.inf, X)
    return jnp.max(X, axis=axis)

def greater_nan(X: Float[Array, "..."], Y: Float[Array, "..."]=0.0) -> Float[Array, "..."]:
    '''Wrapper around jnp.greater that carries NAN values over.

    Parameters
    ----------
    X : Float[Array, "..."]
        Left array to compare.

    Y : Float[Array, "..."]
        Right array to compare.

    Returns
    -------
    Float[Array, "..."]
        Resulting array holding the truth values of the pointwise comparisons, or jnp.nan at points where either array is NAN.
    '''
    return jnp.where(jnp.logical_or(jnp.isnan(X), jnp.isnan(Y)), jnp.nan, jnp.greater(X,Y))

def less_nan(X: Float[Array, "..."], Y: Float[Array, "..."]=0.0) -> Float[Array, "..."]:
    '''Wrapper around jnp.less that carries NAN values over.

    Parameters
    ----------
    X : Float[Array, "..."]
        Left array to compare.

    Y : Float[Array, "..."]
        Right array to compare.

    Returns
    -------
    Float[Array, "..."]
        Resulting array holding the truth values of the pointwise comparisons, or jnp.nan at points where either array is NAN.
    '''
    return jnp.where(jnp.logical_or(jnp.isnan(X), jnp.isnan(Y)), jnp.nan, jnp.less(X,Y))