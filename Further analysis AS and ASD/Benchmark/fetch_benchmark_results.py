#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 13:32:17 2026
 
@author: Martijn
"""
# Analysis for benchmark results
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REVOLVE2_RESULTS = (
    ROOT
    / "revolve2-dd509866ae6fcf2289b334704f8c92bea0b8d2e2"
    / "revolve2-dd509866ae6fcf2289b334704f8c92bea0b8d2e2"
    / "experiments"
    / "default_study"
)
RESULTS = ROOT / "Results"
 
# Read csv files for speed, diversity and parameters
speed = pd.read_csv(REVOLVE2_RESULTS / "result_speed_y_without_nr_generations.csv")
diversity = pd.read_csv(REVOLVE2_RESULTS / "result_pop_diversity_without_nr_generations.csv")
parameters = pd.read_csv(REVOLVE2_RESULTS / "parameters_without_num_generations.csv")
 
# Read csv file for ASD results
asd_results = pd.read_csv(RESULTS / "Without number of generations" / "result_measure.csv")
 
# Merge speed and diversity data, then merge with parameters for analysis
speed_diversity = speed.merge(diversity, left_on=["full_experiment", "id"], right_on=["full_experiment", "individual_id"], how="left", suffixes=('_speed', '_diversity'))
analysis = speed_diversity.merge(parameters.drop(columns="Run"), on=["full_experiment"], how="left")
 
# Find the five experiments with the highest ASD
top_asd = (
    asd_results.sort_values("mean_pop_diversity", ascending=False)
    .drop_duplicates(subset="full_experiment")
    .head(5)
    .copy()
)
top_asd["asd_rank"] = range(1, len(top_asd) + 1)
print(top_asd)
 
top_asd_analysis_rows = analysis.merge(
    top_asd[["full_experiment", "mean_pop_diversity", "asd_rank"]],
    on="full_experiment",
    how="inner",
).sort_values("asd_rank")
 
# Find the five closest parameter rows to the target settings.
# parent_selection and survivor_selection should match exactly, so we can filter those first
target_settings = {
    "population_size": 100,
    "offspring_size": 100,
    "parent_selection": 2,
    "survivor_selection": 2
}
 
filtered_parameters = parameters[
    (parameters["parent_selection"] == target_settings["parent_selection"]) &
    (parameters["survivor_selection"] == target_settings["survivor_selection"])
]
 
setting_distances = (
    (filtered_parameters[list(target_settings)] - pd.Series(target_settings)) ** 2
).sum(axis=1)
closest_rows = (
    filtered_parameters.assign(setting_distance=setting_distances)
    .sort_values("setting_distance")
    .drop_duplicates(subset="full_experiment")
    .head(5)
    .copy()
)
closest_rows["setting_rank"] = range(1, len(closest_rows) + 1)
print(closest_rows)
 
closest_analysis_rows = analysis.merge(
    closest_rows[["full_experiment", "setting_distance", "setting_rank"]],
    on="full_experiment",
    how="inner",
).sort_values("setting_rank")
 
# Write the analysis rows for each selected experiment to separate CSV files.
top_asd_analysis_rows.to_csv(RESULTS / "Best settings ASD" / "max_ASD_top5_rows.csv", index=False)
closest_analysis_rows.to_csv(RESULTS / "Best settings ASD" / "default_settings_top5_rows.csv", index=False)
