# Development

Project layout (important files):

- `src/plotcsv/` — package code (plotter and CLI). If missing, re-create here.
- `plot_example.py` — runnable example script.
- `data/` — sample CSVs.
- `output/` — generated outputs (ignored by git).

Run tests:

```bash
pytest -q
```

Run CLI for development (edit `src/` then run):

```bash
PYTHONPATH=src python -m plotcsv.cli data/sample.csv
```

Formatting:
- Use `black` or your chosen formatter on modified files.

Notes about missing `src/`:
- Earlier commits in the repository history contained `src/plotcsv`. If you need to restore it, identify the commit hash and run:

```bash
git checkout <old-commit-hash> -- src/plotcsv
```

If that fails, the package can be re-created by re-adding `plotter.py` and `cli.py` to `src/plotcsv` and implementing the expected functions described in `docs/usage.md`.
