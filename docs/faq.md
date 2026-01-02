# FAQ

Q: I get "ModuleNotFoundError: No module named 'plotcsv'" — what do I do?

A: Ensure the `src/plotcsv` package exists and run with `PYTHONPATH=src` (or install the package). If `src/` is missing, restore it from a prior commit or re-create the package files.

Q: How do I push to my GitHub repository?

A: Add a remote and push:

```bash
git remote add origin <URL>
git push -u origin main --force
```

Q: How can I change plot styles or add more plot types?

A: Edit the plotting code in `src/plotcsv/plotter.py` (or create new modules) and add CLI options in `src/plotcsv/cli.py`. Use `matplotlib` styles for customization.
