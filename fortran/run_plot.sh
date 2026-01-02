#!/usr/bin/env bash
set -euo pipefail
plt=${1:-output/plot.plt}
if ! command -v gnuplot >/dev/null 2>&1; then
  echo "gnuplot not found. Install gnuplot to render plots."
  exit 2
fi
gnuplot "$plt"
echo "Rendered output/plot.pdf and output/plot.png"
