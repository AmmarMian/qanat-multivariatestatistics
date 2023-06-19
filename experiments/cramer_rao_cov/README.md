cramer\_rao\_cov
----------------

This experiment aims at providing an example of a Monte-Carlo simulation to compute theoretical performance of statistical estimators. In this case, we consider the estimation of the mean and Covariance of a n-dimensional Gaussian distirbution. We sample the ditribution with a fixed mean and covariance and we do several estimations with increasing number of samples. It also illustrated how you can create python files as configuration for your experiment.

The Cramer-Rao lower-bound for the problem is as well computed in an action `plot`.

## Execution script

The main script is `compute_montecarlo.py` whih is configured thanks to `argparse` as follows:

```console
> python compute_montecarlo.py --help
usage: compute_montecarlo.py [-h] [--trials_range_start TRIALS_RANGE_START] [--trials_range_end TRIALS_RANGE_END] [--seed SEED] [--n_jobs N_JOBS] [--storage_path STORAGE_PATH]
                             config_file

Monte-Carlo simulation of the estimation of the parameters of a multivariate normal distribution. We use an MSE criterion to compare the theoretical values of the mean and covariance to
the estimated ones.

positional arguments:
  config_file           Path to the config file containing the parameters of the simulation: covariance, number of samples list, number of trials.

options:
  -h, --help            show this help message and exit
  --trials_range_start TRIALS_RANGE_START
                        Range of the total number of trials to run in this script. Start of the range.This is useful when running the script several times on a cluster.
  --trials_range_end TRIALS_RANGE_END
                        Range of the total number of trials to run in this script. End of the range.This is useful when running the script several times on a cluster.
  --seed SEED           Seed for the random number generator.
  --n_jobs N_JOBS       Number of jobsto run in parallel.
  --storage_path STORAGE_PATH
                        Path to the folder where the results of MSE will be stored.

Example: python compute_montecarlo.py scenario1.py

```

In this case, the definition of the parameters of the Gaussian distribution and other important values are deported to a config file that is taken as a positional argument to the script. This config file is a python script where the variables are defined. The main script will import those values from the file and execute the simulation. Two examples of such files are provided in `scenarios/`:
* `correlated_low_dimension.py`: A farily low-dimensional distribution with correlated variables (Toeplitz structure)
* `white_high_dimension.py`: A higher-dimensional distribution with non-correlated variables (Identity matrix)

It produces a single file:
* `results.pkl`: A pickled dictionary containing the information on the run of the experiment as well as the values of the MSE with increasing samples

There is also an option to run only a part of the define number of trials to allow to for example run several jobs with the subgroups of trials numbers.

## Action(s)

Two actions are configured for this experiments:
* `plot`: It takes a result storage path and plot the MSE with associated Cramer-Rao lower-bound (computed in the execution of the action)
* `see_config`: Show the config file used for the run of an experiment. Since the repertory is a git repository, it gets back to the version of the file at which point the experiment was run to show exactly the file at that moment.

## Parameters file(s)

No parameter files provided here.
