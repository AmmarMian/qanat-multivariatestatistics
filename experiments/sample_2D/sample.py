# ========================================
# FileName: sample.py
# Date: 25 mai 2023 - 10:30
# Author: Ammar Mian
# Email: ammar.mian@univ-smb.fr
# GitHub: https://github.com/ammarmian
# Brief: Sample 2D gaussian distribution
# =========================================

import numpy as np
import argparse
import os

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
            description='Sample 2D gaussian distribution')
    parser.add_argument(
            '--mean', type=str,
            default='0, 0', help='Mean of the gaussian distribution')
    parser.add_argument(
            '--cov', type=str,
            default='1, 0, 0, 1',
            help='Covariance matrix of the gaussian distribution')
    parser.add_argument(
            '--n_samples', type=float, default=1000,
            help='Number of samples to generate')
    parser.add_argument(
            '--seed', type=float, default=0,
            help='Random seed')
    parser.add_argument('--storage_path', type=str, default='data/',
                        help='Path to store the generated samples')

    args = parser.parse_args()

    # Set random seed
    rng = np.random.RandomState(int(args.seed))

    # Generate samples
    mean = [float(x.strip()) for x in args.mean.split(',')]
    cov = [float(x.strip()) for x in args.cov.split(',')]
    cov = np.array(cov).reshape(2, 2)

    samples = rng.multivariate_normal(mean, cov, int(args.n_samples))

    # Save samples and parameters
    if not os.path.exists(os.path.dirname(args.storage_path)):
        os.makedirs(os.path.dirname(args.storage_path))
    np.savetxt(
            os.path.join(args.storage_path, 'samples.csv'),
            samples, delimiter=",")
    parameters = [args.mean, args.cov, int(args.n_samples), int(args.seed)]
    with open(os.path.join(args.storage_path, 'parameters.txt'), 'w') as f:
        for item in parameters:
            f.write("%s\n" % item)
