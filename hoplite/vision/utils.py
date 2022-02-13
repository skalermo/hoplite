import numpy as np


def is_close(tgt, ref, tol=.001):
    """Check if two pixels are of same color.

    Parameters
    ----------
    tgt : numpy.ndarray
        Target pixel (vector).
    ref : numpy.ndarray
        Rerence pixel (vector).

    Returns
    -------
    bool
        `True` if pixels are the same.

    """
    return bool(np.isclose(tgt - ref, 0, atol=tol).all())
