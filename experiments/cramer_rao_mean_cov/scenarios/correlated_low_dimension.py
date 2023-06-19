# ========================================
# FileName: correlated_low_dimension.py
# Date: 25 mai 2023 - 15:04
# Author: Ammar Mian
# Email: ammar.mian@univ-smb.fr
# GitHub: https://github.com/ammarmian
# Brief: Scenario for a case of correlated
#        low dimension data
# =========================================


import numpy as np
from scipy.linalg import toeplitz

n_features = 10
n_samples_list = np.logspace(1, 3, 30,
                             base=n_features,
                             dtype=int)
n_samples_list = np.unique(n_samples_list)
n_trials = 100000

mean = np.zeros(n_features)
covariance = toeplitz(0.75 ** np.arange(n_features))
