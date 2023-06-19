# ========================================
# FileName: plot.py
# Date: 25 mai 2023 - 10:36
# Author: Ammar Mian
# Email: ammar.mian@univ-smb.fr
# GitHub: https://github.com/ammarmian
# Brief: Plot 2D Gaussian distribution
# with mean and covariance matrix ellipsoid
# =========================================

import argparse
import yaml
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import tikzplotlib

import sys
file_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(file_dir, '../..'))
from src.utils import (
        format_covariance_latex,
        tikzplotlib_fix_ncols)


# Activate LaTeX text rendering
# if available on your system
plt.rc('text', usetex=True)
plt.rc('font', family='serif')


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--storage_path', type=str,
                        default='data/',
                        help='Path to the data folder where samples.csv, '
                        'and parameters.txt are located')
    parser.add_argument('--save', action='store_true', default=False,
                        help='Save the plot as pdf and LaTeX code')
    args = parser.parse_args()

    # Check if subfolders with name "group_" exist
    # Which means that several parameters have been
    # estimated and stored in different folders
    if os.path.isdir(os.path.join(args.storage_path, 'group_0')):
        folders = [os.path.join(args.storage_path, f) for f in
                   os.listdir(args.storage_path) if 'group_' in f
                   and os.path.isdir(os.path.join(args.storage_path, f))]
    else:
        folders = [args.storage_path]

    for folder in folders:
        # Load samples
        samples = np.loadtxt(
                os.path.join(folder, 'samples.csv'),
                delimiter=',')

        # Load parameters
        with open(os.path.join(folder, 'parameters.txt'), 'r') as f:
            lines = f.readlines()
            # Mean is first line format: [x1, x2]
            line = lines[0].replace('[', '').replace(']', '')
            mean = np.array([float(x) for x in line.split(',')])
            # Covariance matrix is second line
            line = lines[1].replace('[', '').replace(']', '')
            cov = np.array([float(x) for x in line.split(',')]).reshape(2, 2)
            # Number of samples is third line
            n_samples = int(lines[2])
            # Random seed is fourth line
            seed = int(lines[3])

        # Estimate mean and covariance matrix
        mean_est = np.mean(samples, axis=0)
        cov_est = np.cov(samples.T)
        # Compute eigenvalues and eigenvectors
        eig_val_est, eig_vec_est = np.linalg.eig(cov_est)
        # Compute angle of rotation
        angle_est = np.arctan2(
                eig_vec_est[1, 0],
                eig_vec_est[0, 0]) * 180 / np.pi

        # Compute eigenvalues and eigenvectors for the true covariance matrix
        eig_val, eig_vec = np.linalg.eig(cov)
        # Compute angle of rotationhttps://github.com/AmmarMian/qanat
        angle = np.arctan2(eig_vec[1, 0], eig_vec[0, 0]) * 180 / np.pi

        # Plotting
        fig, ax = plt.subplots(1, 1, figsize=(8, 7))
        ax.scatter(samples[:, 0], samples[:, 1], s=10, c='pink', alpha=0.5,
                   label='Samples')
        ax.scatter(mean[0], mean[1], s=100, c='r', marker='x',
                   label='True mean')
        ax.scatter(mean_est[0], mean_est[1], s=100, c='b', marker='x',
                   label='Estimated mean')

        # Plot covariance matrix ellipsoid
        ell = Ellipse(xy=(mean[0], mean[1]),
                      width=2 * np.sqrt(eig_val[0]),
                      height=2 * np.sqrt(eig_val[1]),
                      angle=angle,
                      color='r',
                      label='True covariance matrix')
        ell.set_facecolor('none')
        ax.add_artist(ell)

        # Plot estimated covariance matrix ellipsoid
        ell_est = Ellipse(xy=(mean_est[0], mean_est[1]),
                          width=2 * np.sqrt(eig_val_est[0]),
                          height=2 * np.sqrt(eig_val_est[1]),
                          angle=angle_est,
                          color='b',
                          label='Estimated covariance matrix')
        ell_est.set_facecolor('none')
        ax.add_artist(ell_est)

        ax.legend()
        ax.set_xlabel(r'$x_1$')
        ax.set_ylabel(r'$x_2$')
        title = r'$\mu = [{:.2f}, {:.2f}]$'.format(mean[0], mean[1]) + ', '
        title += r'$\Sigma = {}$'.format(format_covariance_latex(cov)) + '\n'
        title += r'Number of samples: {}'.format(n_samples) + '\n'
        title += r'Seed: {}'.format(seed)
        ax.set_title(title, ha='left', fontsize=12, loc='left')

        if args.save:
            plt.savefig(os.path.join(folder, 'plot.pdf'), bbox_inches='tight')
            tikzplotlib_fix_ncols(fig)
            tikzplotlib.save(os.path.join(folder, 'plot.tex'))
            print('Saved plot in {}'.format(folder))

    plt.show()
