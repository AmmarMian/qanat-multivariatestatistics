# ========================================
# FileName: compute_montecarlo.py
# Date: 25 mai 2023 - 14:06
# Author: Ammar Mian
# Email: ammar.mian@univ-smb.fr
# GitHub: https://github.com/ammarmian
# Brief: Monte-Carlo simulation of
# a mutivariate normal distribution
# We estiamte the mean and covariance and
# compare it to the theoretical values
# using an MSE criterion.
# =========================================

import numpy as np
from joblib import Parallel, delayed
from sklearn.metrics import mean_squared_error
from sklearn.covariance import EmpiricalCovariance
import argparse
import os
from pathlib import Path
import importlib
import rich
from tqdm import tqdm
import pickle

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from src.utils import matprint

WRITE_PROGRESS_EVERY = 10

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
            description="Monte-Carlo simulation of the estimation of the "
            "parameters of a multivariate normal distribution.\n"
            "We use an MSE criterion to compare the theoretical values of "
            "the mean and covariance to the estimated ones.",
            epilog="Example: python compute_montecarlo.py scenario1.py")
    parser.add_argument('config_file', type=str, help='Path to the config file'
                        ' containing the parameters of the simulation: '
                        'covariance, number of samples list, number of '
                        'trials.')
    parser.add_argument('--trials_range_start', type=int, default=None,
                        help='Range of the total number of trials to run in '
                        'this script. Start of the range.'
                        'This is useful when running the script several times '
                        'on a cluster.')
    parser.add_argument('--trials_range_end', type=int, default=None,
                        help='Range of the total number of trials to run in '
                        'this script. End of the range.'
                        'This is useful when running the script several times '
                        'on a cluster.')
    parser.add_argument('--seed', type=float, default=42, help='Seed for the'
                        ' random number generator.')
    parser.add_argument('--n_jobs', type=int, default=1, help='Number of jobs'
                        'to run in parallel.')
    parser.add_argument('--storage_path', type=str, default='./data/',
                        help='Path to the folder where the results of MSE '
                        'will be stored.')
    args = parser.parse_args()
    seed = int(args.seed)

    # Load the config file
    if not os.path.isfile(args.config_file):
        raise FileNotFoundError("The config file does not exist.")

    sys.path.append(os.path.dirname(args.config_file))
    config = importlib.import_module(Path(args.config_file).stem)

    # Extract the parameters
    mean = config.mean
    covariance = config.covariance
    n_samples_list = config.n_samples_list
    n_trials = config.n_trials
    n_jobs = args.n_jobs

    # Check the trials range
    if args.trials_range_start is not None and \
            args.trials_range_end is not None:
        if args.trials_range_start > args.trials_range_end:
            raise ValueError("The first element of the trials range should be "
                             "smaller than the second one.")
        if args.trials_range_start < 1:
            raise ValueError("The first element of the trials range should be "
                             "greater than 1.")
        if args.trials_range_end < 1:
            raise ValueError("The second element of the trials range should "
                             "be greater than 1.")
        trials_range = [args.trials_range_start, args.trials_range_end]
    else:
        trials_range = [1, n_trials]

    # Pretty print the parameters
    rich.print('[bold]Parameters of the simulation[/bold]')
    rich.print(f'[bold]Mean[/bold]: {mean}')
    rich.print('[bold]Covariance[/bold]:')
    matprint(covariance)
    rich.print(f'[bold]Number of samples[/bold]: {n_samples_list}')
    rich.print(f'[bold]Number of trials[/bold]: {n_trials}')
    rich.print(f'[bold]Number of jobs[/bold]: {n_jobs}')
    rich.print(f'[bold]Trials range[/bold]: {trials_range}')

    # Create a file: progress.txt to track the progress of the simulation
    if not os.path.isdir(args.storage_path):
        os.makedirs(args.storage_path)
    progress_file = os.path.join(args.storage_path, 'progress.txt')
    with open(progress_file, 'w') as f:
        total_trials = trials_range[1] - trials_range[0] + 1
        f.write(f'count_total={total_trials}\n')

    # Function for the Monte-Carlo simulation
    def montecarlo_simulation(mean, covariance,
                              n_samples_list, seed,
                              trial_no):
        rng = np.random.default_rng(seed + trial_no)

        mse_location = np.zeros(len(n_samples_list))
        mse_covariance = np.zeros(len(n_samples_list))
        for i, n_samples in enumerate(n_samples_list):
            # Generate the samples
            samples = rng.multivariate_normal(mean, covariance, n_samples)
            # Estimate the mean and covariance
            empirical_covariance = EmpiricalCovariance().fit(samples)
            # Compute the MSE
            mse_location[i] = \
                mean_squared_error(mean, empirical_covariance.location_)
            mse_covariance[i] = \
                mean_squared_error(covariance,
                                   empirical_covariance.covariance_)

        # Write to progress.txt regularly to track the progress
        # of the simulation
        if (trial_no - trials_range[0] + 1) % WRITE_PROGRESS_EVERY == 0:
            with open(progress_file, 'a') as f:
                f.write(f'{WRITE_PROGRESS_EVERY}\n')

        return mse_location, mse_covariance

    # Run the Monte-Carlo simulation
    results_jobs = Parallel(n_jobs=n_jobs)(
        delayed(montecarlo_simulation)(mean, covariance, n_samples_list,
                                       seed, trial_no)
        for trial_no in tqdm(
            range(trials_range[0], trials_range[1] + 1))
        )

    # Write final progress.txt
    with open(progress_file, 'a') as f:
        f.write('finished')

    # Compute the mean and std of the MSE for location and
    # covariance
    mse_location = np.zeros((total_trials, len(n_samples_list)))
    mse_covariance = np.zeros((total_trials, len(n_samples_list)))
    for trial_no in range(0, trials_range[1] - trials_range[0] + 1):
        mse_location[trial_no, :], mse_covariance[trial_no, :] = \
            results_jobs[trial_no][0], results_jobs[trial_no][1]
    mse_location_mean = np.mean(mse_location, axis=0)
    mse_covariance_mean = np.mean(mse_covariance, axis=0)

    std_location = np.std(mse_location, axis=0)
    std_covariance = np.std(mse_covariance, axis=0)

    # Save the results
    results = {'mse_location_mean': mse_location_mean,
               'mse_covariance_mean': mse_covariance_mean,
               'mse_location_std': std_location,
               'mse_covariance_std': std_covariance,
               'trials_range': trials_range,
               'n_trials': n_trials,
               'n_samples_list': n_samples_list,
               'mean': mean,
               'covariance': covariance,
               'seed': seed}

    results_file = os.path.join(args.storage_path, 'results.pkl')
    with open(results_file, 'wb') as f:
        pickle.dump(results, f)
