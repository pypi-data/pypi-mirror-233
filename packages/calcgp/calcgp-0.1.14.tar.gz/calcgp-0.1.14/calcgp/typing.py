__all__ = ["ScalarFloat", "ScalarOrVector", "TwoArrays", "ListOrTuple"]

from typing import List, Tuple, Union

from jaxtyping import Array, Float

ScalarFloat = Union[float, Float[Array, ""]]
ScalarOrVector = Union[ScalarFloat, Float[Array, "N"]]

TwoArrays = Union[List[Float[Array, "N D"]], Tuple[Float[Array, "N D"], Float[Array, "N D"]]]
ListOrTuple = Union[List, Tuple]