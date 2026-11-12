#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 20:54:41 2023

@author: Martijn
"""
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "Results"

# set plot style: grey grid in the background:
sns.set(style="darkgrid")

##### With number of generations
# Speed
result_s = pd.read_csv(RESULTS / "With number of generations" / "result_mean_speed_y.csv")
# Measure
result_m = pd.read_csv(RESULTS / "With number of generations" / "result_measure.csv")

##### Without number of generations
# Speed
result_s = pd.read_csv(RESULTS / "Without number of generations" / "result_mean_speed_y.csv")
# Measure
result_m = pd.read_csv(RESULTS / "Without number of generations" / "result_measure.csv")

# Merge dataframes
merged_df = pd.merge(result_s, result_m, on=['full_experiment', 'Run', 'Experiment'])

plt.figure(figsize=(8, 6))
fig, ax = plt.subplots()
ax.scatter(merged_df['mean_speed_y'], merged_df['mean_pop_diversity'], color = 'darkblue')
plt.ylabel('ASD')
plt.xlabel('AS')

plt.savefig(RESULTS / "Thesis_speed_against_measure.pdf", format='pdf')
plt.show()
