import warnings
from typing import Union

from . import config


def set_up_precision(precision: Union[float, int] = None, default_precision: int = 15) -> int:
    """
    This method should not be used directly. It is meant for inside package use only.

    Parameters
    ----------
    precision : Union[float, int], optional
        by default None
    default_precision : int, optional
        by default 15

    Returns
    -------
    int
        

    Raises
    ------
    ValueError
        If the provided value can not be used as precision.
    """
    
    if precision is None:
        precision = default_precision
        
    if not isinstance(precision, (int, float)):
        warnings.warn("`precision` is not either `int` or `float`. "
                      "Using default value of precision `{0}`."
                      .format(default_precision), UserWarning)
        precision = default_precision
        
    if precision < 1 or precision > 15:
        raise ValueError("`precision` should be value from range `0` to `15`. It is `{0}`."
                         .format(precision))
        
    if precision != round(precision, 0):
        warnings.warn("`precision` should be number without decimal part. Retyping to Integer.")

    return int(precision)


def set_precision(precision: Union[float, int]) -> None:
    """
    Set default value for precision, used in creation of new objects.

    Parameters
    ----------
    precision : Union[float, int]
        Number of decimal numbers to be used.
    
    Returns
    ----------
    None
    """
    
    precision = set_up_precision(precision)

    config.precision = int(precision)


def get_precision() -> int:
    """
    Get precision number used.

    Returns
    -------
    int
        Number of decimal numbers that is used currently.
    """
    
    return config.precision
