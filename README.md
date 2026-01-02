# CSV to PDF/PNG Plotter

Small Python project that reads CSV files and creates line plots (PDF and PNG).

Usage
-----

- Create and activate a virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- Example run (simple script):

```bash
python plot_example.py
# writes output/example.png
```

- CLI (project package; `src/` layout expected):

```bash
PYTHONPATH=src python -m plotcsv.cli data/sample.csv
```

Git
---

This repository currently has a single clean `main` commit. To push to your GitHub repo, add a remote and push:

```bash
git remote add origin <URL>
git push -u origin main
```


Documentation
-------------

More detailed documentation is available in the `docs/` folder: see [docs/overview.md](docs/overview.md).

Notes
-----
- `output/` and `.venv/` are ignored by `.gitignore`.
- If `src/` is missing, the package (`plotcsv`) may need restoring from earlier commits or re-creation.

