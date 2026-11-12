# Master Thesis: Econometric Analysis

This repository contains the experiment code, a copy of the Revolve2 source files, and the analysis of the experiment results.

## Folders and Scripts

- `parameter_range_FAST.py`: generates the eFAST parameter combinations.
- `sensitivity_analysis_FAST.py`: extracts speed and population-diversity results from the experiment databases.
- `analyse_results.py`: combines the raw results and creates summaries for the analysis with generations.
- `analyse_fourier.py` and `analyse_fourier_gen.py`: run the Fourier sensitivity analyses.
- `Further analysis AS and ASD/`: AS/ASD comparison, benchmark analysis, and effect plots.
- `revolve2-dd509866ae6fcf2289b334704f8c92bea0b8d2e2/revolve2-dd509866ae6fcf2289b334704f8c92bea0b8d2e2/experiments/default_study/`: copied Revolve2 experiment code and the intended location for parameter and raw-result files.
- `Results/`: processed CSV results.

## Result Locations

The local analysis scripts build paths from their own file locations, so they can be run from any working directory.

- Generation-based summaries are stored in `Results/With number of generations/`.
- First-generation Fourier inputs are in `Results/First generations/`.
- The separate analysis without generation counts uses `Results/Without number of generations/`.
- `parameter_range_FAST.py` writes `parameters.csv` beside the copied Revolve2 experiment files.
- `sensitivity_analysis_FAST.py` writes the raw `result_speed_y.csv` and `result_pop_diversity.csv` files to that same `default_study` folder.
- Fourier plots and the AS/ASD comparison plot are saved directly in `Results/`.

## Workflow

1. Run `parameter_range_FAST.py` to generate the experiment parameters.
2. Run the Revolve2 experiments in the environment containing the experiment databases.
3. Run `sensitivity_analysis_FAST.py` to extract the raw speed and diversity results from the databases.
4. Run `analyse_results.py` to create the generation-based summaries in `Results/With number of generations/`.
5. Run `analyse_fourier.py` or `analyse_fourier_gen.py` for the sensitivity analysis.

The included Revolve2 runner and database code come from a separate Linux environment. Their database paths (`/storage/...`) are environment-specific. The databases and raw CSV files are not included in this repository; place or generate the required CSV files in the locations described above.

## Modified Revolve2 Files

These are the Revolve2 files adapted for the thesis experiments:

- [optimize.py](revolve2-dd509866ae6fcf2289b334704f8c92bea0b8d2e2/revolve2-dd509866ae6fcf2289b334704f8c92bea0b8d2e2/experiments/default_study/optimize.py)
- [optimizer.py](revolve2-dd509866ae6fcf2289b334704f8c92bea0b8d2e2/revolve2-dd509866ae6fcf2289b334704f8c92bea0b8d2e2/experiments/default_study/optimizer.py)
- [run-experiments-Martijn.sh](revolve2-dd509866ae6fcf2289b334704f8c92bea0b8d2e2/revolve2-dd509866ae6fcf2289b334704f8c92bea0b8d2e2/experiments/default_study/run-experiments-Martijn.sh)
- [setup-experiments-Martijn.sh](revolve2-dd509866ae6fcf2289b334704f8c92bea0b8d2e2/revolve2-dd509866ae6fcf2289b334704f8c92bea0b8d2e2/experiments/default_study/setup-experiments-Martijn.sh)
- [config.py](revolve2-dd509866ae6fcf2289b334704f8c92bea0b8d2e2/revolve2-dd509866ae6fcf2289b334704f8c92bea0b8d2e2/core/revolve2/core/config.py)

## Analysis Without Generation

This is a separate analysis and requires manually updating the input paths and selecting the appropriate data in the relevant scripts. Not every step has a separate no-generation version. `impact.py` contains input blocks for both analyses; the last block determines the active input. The benchmark script expects `result_speed_y_without_nr_generations.csv` and `result_pop_diversity_without_nr_generations.csv` beside the copied Revolve2 files in `default_study`.

## Further Analysis

- `Further analysis AS and ASD/impact.py`: compares AS with ASD.
- `Further analysis AS and ASD/Benchmark/fetch_benchmark_results.py`: selects the five highest-ASD results and the settings closest to the defaults.
- `Further analysis AS and ASD/Benchmark/Benchmark_results.ipynb`: creates benchmark plots.
- `Further analysis AS and ASD/Effect/heathplot.ipynb`: effect plots and parameter-space visualizations.