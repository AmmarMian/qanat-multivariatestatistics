# ========================================
# FileName: cramer_rao.py
# Date: 26 mai 2023 - 16:32
# Author: Ammar Mian
# Email: ammar.mian@univ-smb.fr
# GitHub: https://github.com/ammarmian
# Brief: Cramer-Rao lower bound functions
# =========================================

import numpy as np
from statsmodels.tsa.tsatools import (
        duplication_matrix
)
from numba import njit


# Multivariate Gaussian
# =====================
@njit
def basis_euc_sym_mat_real(M: int) -> np.ndarray:
    """Construction of the cannonical basis of M*M
    symetric matrices

    Args:
        M (int): Dimension of the matrix

    Returns:
        np.ndarray: Cannonical basis of M*M symetric matrices
    """

    lindex = int(M*(M+1)/2)
    Omega = np.zeros((M, M, lindex), dtype=float)
    index = 0
    # Basis of the diag parts
    for i in range(M):
        Omega[i, i, index] = 1
        index = index+1

    for i in range(M):
        for j in range(i+1):
            if (i != j):
                Omega[i, j, index] = 1/np.sqrt(2)
                Omega[j, i, index] = 1/np.sqrt(2)
                index = index+1
    return Omega

#TODO: DEBUG
def basis_euc_sym_mat_real_vec(M: int) -> np.ndarray:
    """Alternative implementation of the cannonical basis of M*M
    symetric matrices using vectorization.

    Args:
        M (int): Dimension of the matrix

    Returns:
        np.ndarray: Cannonical basis of M*M symetric matrices
    """
    lindex = int(M*(M+1)/2)
    Omega = np.zeros((M, M, lindex), dtype=float)
    triu_indices = np.triu_indices(M, k=1)
    tril_indices = np.tril_indices(M, k=-1)
    diag_indices = np.diag_indices(M, ndim=3)
    Omega[diag_indices] = 1
    Omega[(*triu_indices, np.arange(M, lindex))] = \
        1/np.sqrt(2)
    Omega[(*tril_indices, np.arange(M, lindex))] = \
        1/np.sqrt(2)
    return Omega


def crb_centered_multivariate_gaussian_basis(
        cov: np.ndarray, n_samples: int) -> np.ndarray:
    """Compute Cramer-Rao lower bound for centered multivariate Gaussian.
    Version with Basis. Slower in high dimension.

    Args:
        cov (np.ndarray): Covariance matrix of the centered multivariate
        n_samples (int): Number of samples

    Returns:
        np.ndarray: Cramer-Rao lower bound matrix
    """
    n_features = cov.shape[0]
    icov = np.linalg.inv(cov)
    Omega = basis_euc_sym_mat_real(n_features)
    M = Omega.shape[2]

    # Constructing the Fisher information matrix
    F = np.zeros((M, M), dtype=float)
    for i in range(M):
        for j in range(M):
            F[i, j] = np.trace(icov @ Omega[:, :, i] @ icov @ Omega[:, :, j])

    # Constructing the Cramer-Rao lower bound matrix
    crb = np.linalg.inv(F)
    return 2*crb/n_samples


# TODO: debug this. Not quite right
def crb_centered_multivariate_gaussian_kron(
        cov: np.ndarray, n_samples: int) -> np.ndarray:
    """Compute Cramer-Rao lower bound for centered multivariate Gaussian.
    Version with Kronecker formula.

    Args:
        cov (np.ndarray): Covariance matrix of the centered multivariate
        n_samples (int): Number of samples

    Returns:
        np.ndarray: Cramer-Rao lower bound matrix
    """

    icov = np.linalg.inv(cov)
    n_features = cov.shape[0]

    return np.linalg.inv(
            n_samples * duplication_matrix(n_features).T @
            np.kron(icov, icov) @ duplication_matrix(n_features)
        )
