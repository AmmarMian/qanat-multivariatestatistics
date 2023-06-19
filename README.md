<a name="readme-top"></a>
# Qanat Examples: Multivariate Statistics

This repository is an example project for [Qanat](https://ammarmian.github.io/qanat/), a command-line based exeperiment tracking tool. The focus here is on experiemnts to illustrate various results on multivariate statistics theory. It also illustrate how you can setup Qanat project for heavy Monte-Carlo based experiments' tracking.


<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#readme-top">About The Project</a>
    </li>
    <li><a href="#documentation">Documentation</a></li>
    <li>
      <a href="#installation">Installation</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#settinguptheproject">Setting up the project</a></li>
      </ul>
    </li>
    <li><a href="#authors">Authors</a></li>
  </ol>
</details>


## Documentation

Documentation fro Qanat available at https://ammarmian.github.io/qanat/.
**Still in progress**.

## Installation

### Prerequisites

* python >= 3.6
* htcondor (for HTcondor runner)
* an emoji friendly terminal
* [Qanat](https://github.com/AmmarMian/qanat)
* pydoit

### Setting up the projects

You can fetch this example thanks to:

```bash
git clone https://github.com/AmmarMian/qanat-multivariatestatistics
cd qanat-multivariatestatistics
```

Then to setup the project, do:

```bash
doit initialize_example
```

which will initialize the qanat repertory and add relevant experiments and datasets.


## Available experiments

* sample\_2D: Visualisation of two-dimensional real-valued Gaussian sampling. Located in experiments/sample\_2D
* cramer\_rao_\cov: Estimation of the mean and covariance of a real\_valued n-dimensional Gaussian distribution with a visualisation of the Cramer-Rao lower-bound. Located in experiments/cramer\_rao\_cov


## Authors

Ammar Mian, Associate professor at LISTIC, Université Savoie Mont-Blanc
  * :envelope: mail: ammar.mian@univ-smb.fr
  * :house: web: https://ammarmian.github.io

