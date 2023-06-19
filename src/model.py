# ========================================
# FileName: model.py
# Date: 25 mai 2023 - 10:25
# Author: Ammar Mian
# Email: ammar.mian@univ-smb.fr
# GitHub: https://github.com/ammarmian
# Brief: Models for the project
# =========================================

import numpy as np
from scipy.stats import multivariate_normal


def make_gaussian_corrupted(mean: np.ndarray, cov: np.ndarray, n_samples: int,
                            corruption: float = 0.1) -> np.ndarray:
    """Generate a Gaussian corrupted dataset.

    Args:
        mean (np.ndarray): Mean of the Gaussian distribution.
        cov (np.ndarray): Covariance matrix of the Gaussian distribution.
        n_samples (int): Number of samples to generate.
        corruption (float, optional): Corruption ratio. Defaults to 0.1.

    Returns:
        np.ndarray: Generated dataset.
    """

    # Generate the dataset
    X = multivariate_normal.rvs(mean=mean, cov=cov, size=n_samples)

    # Generate the corruption mask
    mask = np.random.choice(
        [0, 1], size=X.shape, p=[corruption, 1 - corruption])

    # Generate corruption values very far from the mean
    corruption_values = multivariate_normal.rvs(
            mean=mean * 100, cov=cov * 100, size=n_samples)

    # Apply the corruption mask
    X = X * mask + corruption_values * (1 - mask)
