# Fortran 90: CSV to PDF/PNG Plotter

This folder contains a minimal Fortran 90 implementation that reads a CSV file, asks simple interactive questions to choose columns to plot, and produces a temporary data file and a gnuplot script. Use `gnuplot` to render PDF/PNG output.

Prerequisites
-------------

- `gfortran` (or another Fortran compiler)
- `gnuplot` (for rendering plots to PDF/PNG)

Build and run
-------------

From the repository root run:

```bash
make -C fortran run
```

This will compile the Fortran program, run it against `data/sample.csv`, and then call the included `run_plot.sh` to generate `output/plot.pdf` and `output/plot.png`.

Notes
-----
- The Fortran program writes `output/tmpdata.dat` and `output/plot.plt` which are consumed by `gnuplot`.
- The parser is intentionally simple and expects comma-separated numeric columns; headers are used to select columns interactively.
