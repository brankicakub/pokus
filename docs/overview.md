# Project Overview

This project reads one or more CSV files and creates line plots saved as PDF and optionally PNG files. It includes:

- A small plotting package (`plotcsv`) (may be in `src/plotcsv`).
- A CLI that can operate interactively (chat-like prompts) or non-interactively with flags.
- A minimal example script (`plot_example.py`) and sample data under `data/`.

Goals:

- Provide a straightforward way to visualize timeseries or numeric CSV data.
- Support autoscaling, simple axis selection, date parsing, and single-PDF output per run.
