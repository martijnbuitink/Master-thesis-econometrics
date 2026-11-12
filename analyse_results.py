#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 18:50:27 2023

@author: Martijn
"""
import pandas as pd
import numpy as np
from pathlib import Path
from revolve2.core.config import Config

ROOT = Path(__file__).resolve().parent
REVOLVE2_RESULTS = (
    ROOT
    / "revolve2-dd509866ae6fcf2289b334704f8c92bea0b8d2e2"
    / "revolve2-dd509866ae6fcf2289b334704f8c92bea0b8d2e2"
    / "experiments"
    / "default_study"
)
RESULTS = ROOT / "Results" / "With number of generations"

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

# Read data
df_speed_y = pd.read_csv(REVOLVE2_RESULTS / "result_speed_y.csv")
df_pop_diversity = pd.read_csv(REVOLVE2_RESULTS / "result_pop_diversity.csv")

run_speed = df_speed_y["Run"] == 3.0
df_speed_y = df_speed_y[run_speed]

run_div = df_pop_diversity["Run"] == 3.0
df_pop_diversity = df_pop_diversity[run_div]

# Replace -inf and inf by np.NaN
df_speed_y.replace([np.inf, -np.inf], np.NaN, inplace=True)


#########################################################
################### Get mean speed ################### #########################################################

df_result_mean_speed = df_speed_y.groupby(['full_experiment', 'Run','Experiment'])['speed_y'].mean().reset_index(name = 'mean_speed_y')
print(df_result_mean_speed)
# Write result to right folder
df_result_mean_speed.reset_index().set_index(['full_experiment', 'Run','Experiment']).to_csv(REVOLVE2_RESULTS / "result_mean_speed_y.csv", index=False)
df_result_mean_speed.to_csv(RESULTS / "result_mean_speed_y.csv", index=False)


#########################################################
################### Get pop_diversity ################### #########################################################

# Join two dataframes
df_pop_diversity_speed_y = pd.merge(df_pop_diversity, df_speed_y,  how='left', left_on=['individual_id', 'full_experiment', 'Run', 'Experiment'], right_on = ['id', 'full_experiment', 'Run','Experiment'])

# Calculate mean and maximum per generation 
df_mean_speed_y_generation = df_pop_diversity_speed_y.groupby(['generation_index', 'full_experiment', 'Run','Experiment'])['speed_y'].mean().reset_index(name = 'mean_speed_y') 
df_mean_pop_diversity_generation = df_pop_diversity_speed_y.groupby(['generation_index', 'full_experiment', 'Run','Experiment'])['pop_diversity'].mean().reset_index(name = 'mean_pop_diversity')

# Join two dataframes and create measure 
df_measure = pd.merge(df_mean_pop_diversity_generation, df_mean_speed_y_generation,  how='left', left_on=['generation_index', 'full_experiment', 'Run', 'Experiment'], right_on = ['generation_index', 'full_experiment', 'Run','Experiment'])
df_measure['mean_pop_diversity'] = pd.to_numeric(df_measure['mean_pop_diversity'])
df_measure['mean_speed_y'] = pd.to_numeric(df_measure['mean_speed_y'])

measure = []
for i, row in df_measure.iterrows():
    measure.append(row['mean_pop_diversity'] * row['mean_speed_y'])

df_measure['measure'] = measure

# Get average of measure per experiment
df_result_measure = df_measure.groupby(['full_experiment', 'Run','Experiment'])['measure'].mean().reset_index(name = 'mean_pop_diversity')
print(df_result_measure)
df_result_measure = df_result_measure.reset_index()
df_result_measure.to_csv(RESULTS / "result_measure.csv", index=False)
