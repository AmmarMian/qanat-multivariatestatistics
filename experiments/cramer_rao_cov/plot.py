# ========================================
# FileName: plot.py
# Date: 25 mai 2023 - 10:36
# Author: Ammar Mian
# Email: ammar.mian@univ-smb.fr
# GitHub: https://github.com/ammarmian
# Brief: Plot MSE curve and lower bound
# as a function of the number of samples.
# =========================================

import argparse
import os
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import tikzplotlib
import rich
import sys
from tqdm import tqdm
file_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(file_dir, '../..'))
from src.utils import (
        tikzplotlib_fix_ncols
)
from src.cramer_rao import (
        crb_centered_multivariate_gaussian_basis,
)

sns.set_style('darkgrid')

# Activate LaTeX text rendering
# if available on your system
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


def generate_figure(mse_covariance_mean,
                    mse_covariance_std,
                    crb,
                    n_samples_list,
                    folder,
                    save=False):

    fig_cov, ax_cov = plt.subplots(1, 1, figsize=(6, 4))
    ax_cov.plot(n_samples_list, mse_covariance_mean, label='Covariance',
                marker='o', markersize=5, linestyle='')

    # Fill between the standard deviation
    ax_cov.fill_between(n_samples_list,
                        mse_covariance_mean - mse_covariance_std,
                        mse_covariance_mean + mse_covariance_std,
                        color='b', alpha=0.2,
                        label='Standard deviation')

    # Plot the lower bound
    ax_cov.plot(n_samples_list, crb, label='Lower bound',
                marker='', c='k', linestyle='-')

    ax_cov.set_xlabel('Number of samples')
    ax_cov.set_ylabel('MSE')
    ax_cov.set_title(
            'MSE as a function of the number of samples: covariance\n'
            'Folder: {}'.format(folder))
    # log-log plot
    ax_cov.set_xscale('log')

    if save:
        plt.savefig(os.path.join(folder, 'MSE_covariance.pdf'),
                    bbox_inches='tight')
        tikzplotlib_fix_ncols(fig_cov)
        tikzplotlib.save(os.path.join(folder, 'MSE_covariance.tex'))
        print('Saved covariance plot in {}'.format(folder))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--storage_path', type=str,
                        default='data/',
                        help='Path to the data folder where '
                        'results.pkl is located.')
    parser.add_argument('--aggregate', action='store_true', default=False,
                        help='Aggregate results from different folders')
    parser.add_argument('--save', action='store_true', default=False,
                        help='Save the plot as pdf and LaTeX code')
    args = parser.parse_args()

    rich.print(
            '[bold green]Plotting MSE as a function of the number of samples')
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

        # Plotting
        generate_figure(mse_covariance_mean,
                        mse_covariance_std,
                        crb,
                        n_samples_list,
                        args.storage_path,
                        args.save)

    else:
        # We plot the results from each folder
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

            # Plotting
            generate_figure(results['mse_covariance_mean'],
                            results['mse_covariance_std'],
                            crb,
                            results['n_samples_list'],
                            folder,
                            args.save)

    plt.show()
