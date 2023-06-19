Sample 2D
----------

This experiment aims at sampling 2-dimensional real-valued Gaussian data in order to visualize the estimation of its mean and covariance.

## Execution script

The main script is `sample.py` whih is configured thanks to `argparse` as follows:

```console
> python sample.py --help
usage: sample.py [-h] [--mean MEAN] [--cov COV] [--n_samples N_SAMPLES] [--seed SEED] [--storage_path STORAGE_PATH]

Sample 2D gaussian distribution

options:
  -h, --help            show this help message and exit
  --mean MEAN           Mean of the gaussian distribution
  --cov COV             Covariance matrix of the gaussian distribution
  --n_samples N_SAMPLES
                        Number of samples to generate
  --seed SEED           Random seed
  --storage_path STORAGE_PATH
                        Path to store the generated samples
```

You can parametrize the mean, covariance, number of generated samples as well as the seed of the random number generator.

It produces two files:
* `samples.csv`: The generated samples
* `parameters.txt`: The parameters used for easier parsing for the action `plot`


## Action(s)

One action is configured for this experiments:
* `plot`: It takes a result storage path and depending on the number of groups of parameters used to run the experiment, will show the only or all of the samples in a 2D plot. The true and estimated covariances will also be visualized with crosses and an ellipsoids. To run this action on a run: `qanat experiment action sample_2D plot <RUN_ID>`

## Parameters file(s)

A single parameter file description is provided:
* `parameter_files/increasing_nsamples.yaml` which defines a mean and a covariance, and do a range on the number of samples. This can allow to showcase the better estimation of the mean and covariance when increasing the number of samples. To run this setup: `qanat experiment run sample_2D -f parameter_files/increasing_nsamples.yaml`.
