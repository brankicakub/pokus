# Usage

Basic example (minimal script):

```bash
python plot_example.py
# creates output/example.png
```

CLI usage (package-based):

```bash
PYTHONPATH=src python -m plotcsv.cli data/sample.csv
```

Interactive mode:
- The CLI will ask simple questions about which columns to use for X/Y, whether to parse dates, and export options. Answer the prompts or pass `-y`/`--yes` to accept defaults.

Non-interactive flags (examples):

- `--x-col` and `--y-col` to set column names.
- `--parse-dates` to attempt parsing the X column as dates.
- `--output` to specify the output filename (PDF). Add `--png` to also emit PNG files.

Output:
- By default one plot (per CSV file) is created and written into a single PDF (and optionally PNGs in `output/`).

When `src/` is missing:
- The CLI expects the package under `src/plotcsv`. If you see import errors, restore `src/` from earlier commits or re-create the package files in `src/plotcsv`.
