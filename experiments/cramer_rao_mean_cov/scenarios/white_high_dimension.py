# ========================================
# FileName: white_high_dimension.py
# Date: 25 mai 2023 - 15:04
# Author: Ammar Mian
# Email: ammar.mian@univ-smb.fr
# GitHub: https://github.com/ammarmian
# Brief: Scenario for a case of correlated
#        low dimension data
# =========================================


import numpy as np

n_features = 70
n_samples_list = np.logspace(1, 2, 30,
                             base=n_features,
                             dtype=int)
n_samples_list = np.unique(n_samples_list)
n_trials = 10000

mean = np.zeros(n_features)
covariance = np.eye(n_features)
