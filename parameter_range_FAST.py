#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 14:13:42 2022

@author: Martijn
"""
from SALib.sample import saltelli
from SALib.analyze import sobol
from SALib.sample import fast_sampler
from SALib.analyze import fast
from SALib.test_functions import Ishigami
import numpy as np
import pandas as pd
from pathlib import Path

REVOLVE2_RESULTS = (
    Path(__file__).resolve().parent
    / "revolve2-dd509866ae6fcf2289b334704f8c92bea0b8d2e2"
    / "revolve2-dd509866ae6fcf2289b334704f8c92bea0b8d2e2"
    / "experiments"
    / "default_study"
)

# Where do you want to file to store?
mainpath = "mbuitink"

# How many evaluations? n*nr_variables
# Must be larger than N > 4M^2 is required. M=4 by default.
nr_runs = 65

# Define problem
# Bounds are 0.5 above and below bound (later rounded to integers) 
problem = {'num_vars': 5,
           'names': ['population_size',
                     'offspring_size',
                     'num_generations',
                     'parent_selection',
                     'survivor_selection'],
           'bounds': [[49.5,200.5],
                      [49.5,100.5],
                      [49.5,200.5],
                      [1.5, 4.5],
                      [1.5, 4.5]],
           'dists': ['unif',
                     'unif',
                     'unif',
                     'unif',
                     'unif']
    }

# Find all combinations of parameters that need to be checked 
# Parameters are rounded to integers 
parameters = fast_sampler.sample(problem, nr_runs) 
parameters = np.round(parameters,0).astype(int)

# Write the result to a dataframe
result = pd.DataFrame(parameters,
                      columns=['population_size',
                               'offspring_size',
                               'num_generations',
                               'parent_selection',
                               'survivor_selection'])

# Add number of runs per experiment
result['experiment_repetitions'] = 3

# Assing experiment number
result['full_experiment'] = np.arange(1,len(result)+1)

# Each run is a different experiment
runs_max = result['experiment_repetitions'].max()
runs_min = result['experiment_repetitions'].min()

runs = []
for i in range(runs_min, runs_max+1):
    for j in range(1, i+1):
        runs.append([j,i])

runs = pd.DataFrame(runs,
                    columns=['Run',
                             'experiment_repetitions'])

result = pd.merge(
    result, runs, how="left", on=['experiment_repetitions']
    )

print(result)

# Assign experiment number
result['Experiment'] = np.arange(1,len(result)+1)

# Write result to right folder
result.to_csv(REVOLVE2_RESULTS / "parameters.csv", index=False)

