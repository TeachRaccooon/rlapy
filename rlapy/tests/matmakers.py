from typing import Union
import numpy as np
import scipy.linalg as la
import rlapy.utils.sketching as sk


def rand_low_rank(n_rows, n_cols, spectrum: Union[int, np.ndarray], rng, factors=False):
    rng = np.random.default_rng(rng)
    if isinstance(spectrum, int):
        spectrum = rng.random(size=(spectrum,))
    spectrum = np.sort(spectrum)
    spectrum = spectrum[::-1]  # reverse
    spectrum /= spectrum[0]
    rank = spectrum.size
    U = sk.orthonormal_operator(n_rows, rank, rng)
    V = sk.orthonormal_operator(rank, n_cols, rng)
    M = (U * spectrum) @ V
    if factors:
        return M, U, spectrum, V
    else:
        return M


def simple_mat(n_rows, n_cols, scale, rng):
    rng = np.random.default_rng(rng)
    A = rng.normal(0, 1, (n_rows, n_cols))
    QA, RA = la.qr(A)
    damp = 1 / np.sqrt(1 + scale * np.arange(n_cols))
    RA *= damp
    A_bad = QA @ RA
    return A_bad


def exponent_spectrum(n_rows, n_cols, rank, rng, spectrum_param, factors=False):
    spectrum = np.exp((-np.arange(1, rank) + 1) / spectrum_param)
    return rand_low_rank(n_rows, n_cols, spectrum, rng, factors)     


def s_shaped_spectrum(n_rows, n_cols, rank, rng, factors=False):
    spectrum = 0.0001 + 1 / (1 + np.exp(np.arange(1, rank) - 29));
    return rand_low_rank(n_rows, n_cols, spectrum, rng, factors)      
