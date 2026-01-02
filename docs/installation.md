# Installation

1. Create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install runtime dependencies:

```bash
pip install -r requirements.txt
```

3. Optional: install development/test dependencies (if present):

```bash
pip install -r requirements-dev.txt || true
```

Notes:
- This project was developed and tested on Python 3.10; newer 3.x versions should work.
- The project uses `pandas` and `matplotlib` for data handling and plotting.
