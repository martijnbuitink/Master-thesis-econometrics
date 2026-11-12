#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 14:13:42 2022

@author: Martijn
"""

import pandas as pd
from pathlib import Path
from sqlalchemy.future import select
import numpy as np

from revolve2.core.config import Config

from revolve2.core.database import open_database_sqlite 
from revolve2.core.database.serializers import DbFloat 
from revolve2.core.optimization.ea.generic_ea._database import (
    DbEAOptimizerGeneration,
    DbEAOptimizerIndividual
)

REVOLVE2_RESULTS = (
    Path(__file__).resolve().parent
    / "revolve2-dd509866ae6fcf2289b334704f8c92bea0b8d2e2"
    / "revolve2-dd509866ae6fcf2289b334704f8c92bea0b8d2e2"
    / "experiments"
    / "default_study"
)

# Where do you want to file to store?
mainpath = "mbuitink"
study_name = "default_study"

# Import args
args = Config()._get_params()

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

parameters = pd.read_csv(REVOLVE2_RESULTS / "parameters.csv")

# How many experiments are there?
nr_experiments = max(parameters['full_experiment'])
print('nr_experiments: ', nr_experiments)



def get_speed(db, exp, full_exp, run):
    # read the optimizer data into a pandas dataframe
    df = pd.read_sql(
        select(
            DbFloat
            ),
        db,)
    result = df[["id", "speed_y"]]
    result = result.assign(full_experiment = full_exp)
    result = result.assign(Run = run)
    result = result.assign(Experiment = exp)

    return(result.values.tolist())


#List to store pop_diversity
result = []

for full_exp in range(1, nr_experiments+1):
#for full_exp in range(1, 3):
    print('At experiment: ', full_exp)
    # How many runs for this experiment?
    exp_rep = parameters.loc[parameters['full_experiment'] == full_exp, 'experiment_repetitions'].iloc[0].item()

    for run in range(1, exp_rep+1):
        # Number of experiment
        exp = parameters.loc[(parameters['full_experiment'] == full_exp) & (parameters['Run'] == run), 'Experiment'].iloc[0].item()
        # Connection to experiment
        db = open_database_sqlite(f'/storage/{mainpath}/{study_name}/{args.experiment_name}/run_{exp}')

        # Get result
        result_exp = get_speed(db, exp = exp, full_exp = full_exp, run = run)
        result.extend(result_exp)

# List to store pop_diversity
result = pd.DataFrame(result,
                      columns = ['id',
                                  'speed_y',
                                  'full_experiment',
                                  'Run',
                                  'Experiment'])

# Write result to right folder
result.to_csv(REVOLVE2_RESULTS / "result_speed_y.csv", index=False)



def get_pop_diversity(db, exp, full_exp, run):
    # read the optimizer data into a pandas dataframe
    df = pd.read_sql(
        select(
            DbEAOptimizerGeneration
            ),
        db,)
    result = df[['generation_index', 'individual_index', 'individual_id', 'pop_diversity']]
    result = result.assign(full_experiment = full_exp)
    result = result.assign(Run = run)
    result = result.assign(Experiment = exp)

    return(result.values.tolist())

# List to store pop_diversity
result = []

for full_exp in range(1, nr_experiments+1):
#for full_exp in range(1, 3):
    print('At experiment: ', full_exp)
    # How many runs for this experiment?
    exp_rep = parameters.loc[parameters['full_experiment'] == full_exp, 'experiment_repetitions'].iloc[0].item()

    for run in range(1, exp_rep+1):
        # Number of experiment
        exp = parameters.loc[(parameters['full_experiment'] == full_exp) & (parameters['Run'] == run), 'Experiment'].iloc[0].item()
        # Connection to experiment
        db = open_database_sqlite(f'/storage/{mainpath}/{study_name}/{args.experiment_name}/run_{exp}')

        # Get result
        result_exp = get_pop_diversity(db, exp = exp, full_exp = full_exp, run = run)
        result.extend(result_exp)

result = pd.DataFrame(result,
                      columns = ['generation_index',
                                 'individual_index',
                                 'individual_id',
                                 'pop_diversity',
                                 'full_experiment',
                                 'Run',
                                 'Experiment'])

# Write result to right folder
result.to_csv(REVOLVE2_RESULTS / "result_pop_diversity.csv", index=False)
