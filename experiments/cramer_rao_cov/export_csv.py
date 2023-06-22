# ========================================
# FileName: export_csv.py
# Date: 25 mai 2023 - 10:36
# Author: Ammar Mian
# Email: ammar.mian@univ-smb.fr
# GitHub: https://github.com/ammarmian
# Brief: Export MSE and lower bound as csv
# =========================================

import argparse
import os
import numpy as np
import pickle
import rich
import sys
from tqdm import tqdm
import pandas as pd
file_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(file_dir, '../..'))
from src.cramer_rao import (
        crb_centered_multivariate_gaussian_basis,
)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--storage_path', type=str,
                        default='data/',
                        help='Path to the data folder where '
                        'results.pkl is located.')
    parser.add_argument('--aggregate', action='store_true', default=False,
                        help='Aggregate results from different groups folders')
    args = parser.parse_args()

    rich.print('[bold green]Folder: {}'.format(args.storage_path))
    rich.print('[bold red]Sorry, the lower-bound is very slow to compute.'
               'for larger size of the covariance matrix.')

    # Check if subfolders with name "group_" exist
    # Which means that several parameters have been
    # estimated and stored in different folders
    if os.path.isdir(os.path.join(args.storage_path, 'group_0')):
        folders = [os.path.join(args.storage_path, f) for f in
                   os.listdir(args.storage_path) if 'group_' in f
                   and os.path.isdir(os.path.join(args.storage_path, f))]
    else:
        folders = [args.storage_path]

    # We aggregate the restults from all the folders if wanted
    if args.aggregate:
        mse_covariance_mean = []
        mse_covariance_std = []
        trials_per_group = []
        for folder in folders:

            # Load results
            with open(os.path.join(folder, 'results.pkl'), 'rb') as f:
                results = pickle.load(f)

            # Aggregate results
            mse_covariance_mean.append(results['mse_covariance_mean'])
            mse_covariance_std.append(results['mse_covariance_std'])
            trials_range = results['trials_range']
            trials_per_group.append(trials_range[1] - trials_range[0] + 1)
            n_samples_list = results['n_samples_list']

        # Compute the weighted average
        mse_covariance_mean = np.array(mse_covariance_mean)
        mse_covariance_mean = np.average(mse_covariance_mean, axis=0,
                                         weights=trials_per_group)

        # Compute the weighted standard deviation
        # TODO: VERIFY THIS FORMULA!!!!!!!
        mse_covariance_std = np.array(mse_covariance_std)
        mse_covariance_std = np.sqrt(np.average(
            (mse_covariance_std**2 + mse_covariance_mean**2), axis=0,
            weights=trials_per_group) - mse_covariance_mean**2)

        # Compute the lower bound
        crb = np.zeros((len(n_samples_list),))
        print("Computing CRB")
        for i, n_samples in enumerate(tqdm(n_samples_list)):
            crb[i] = np.sqrt(np.trace(
                    crb_centered_multivariate_gaussian_basis(
                        results['covariance'], n_samples)
                        )
                    )

        # Save the results in csv format
        df = pd.DataFrame({'n_samples': n_samples_list,
                           'mse_mean': mse_covariance_mean,
                           'mse_std': mse_covariance_std
                           })
        df.to_csv(os.path.join(args.storage_path, 'MSE.csv'),
                  index=False)

        df = pd.DataFrame({'n_samples': n_samples_list,
                           'crb': crb
                           })
        df.to_csv(os.path.join(args.storage_path, 'CRB.csv'),
                  index=False)

    else:
        # We fetch the results from each folder
        for folder in folders:
            # Load results
            with open(os.path.join(folder, 'results.pkl'), 'rb') as f:
                results = pickle.load(f)

            # Compute the lower bound
            n_samples_list = results['n_samples_list']
            crb = np.zeros((len(n_samples_list),))
            print("Computing CRB")
            for i, n_samples in enumerate(tqdm(n_samples_list)):
                crb[i] = np.trace(
                            crb_centered_multivariate_gaussian_basis(
                                results['covariance'], n_samples)
                        )

            # Save the results in csv format
            df = pd.DataFrame({'n_samples': n_samples_list,
                               'mse_mean': results['mse_covariance_mean'],
                               'mse_std': results['mse_covariance_std']
                               })
            df.to_csv(os.path.join(folder, 'MSE.csv'),
                      index=False)

            df = pd.DataFrame({'n_samples': n_samples_list,
                               'crb': crb
                               })
            df.to_csv(os.path.join(folder, 'CRB.csv'),
                      index=False)
