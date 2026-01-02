import os
from typing import List, Optional, Tuple

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def plot_csv_to_pdf(
    csv_path: str,
    output_pdf: str,
    parse_dates: bool = False,
    x_col: Optional[str] = None,
    y_cols: Optional[List[str]] = None,
    title: Optional[str] = None,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    x_range: Optional[Tuple[float, float]] = None,
    y_range: Optional[Tuple[float, float]] = None,
    create_png: bool = False,
    png_path: Optional[str] = None,
    png_dpi: int = 150,
):
    df = pd.read_csv(csv_path)

    if parse_dates:
        # assume first column is date-like if parse_dates is True
        df = pd.read_csv(csv_path, parse_dates=[0])
        x = df.iloc[:, 0]
        df_plot = df.iloc[:, 1:]
    else:
        df_plot = df.select_dtypes(include=["number"]).copy()
        if x_col and x_col in df.columns:
            x = df[x_col]
        else:
            x = df_plot.index

    if y_cols:
        # limit to requested columns if present
        y = [c for c in y_cols if c in df_plot.columns]
    else:
        y = list(df_plot.columns)

    if len(y) == 0:
        raise ValueError("No numeric columns found to plot.")

    fig, ax = plt.subplots(figsize=(8, 4.5))
    for col in y:
        ax.plot(x, df_plot[col], label=col)

    if title:
        ax.set_title(title)
    if x_label:
        ax.set_xlabel(x_label)
    if y_label:
        ax.set_ylabel(y_label)

    if x_range:
        ax.set_xlim(x_range)
    if y_range:
        ax.set_ylim(y_range)

    ax.grid(True)
    if len(y) > 1:
        ax.legend()

    pdf_dir = os.path.dirname(output_pdf) or "."
    os.makedirs(pdf_dir, exist_ok=True)
    with PdfPages(output_pdf) as pdf:
        pdf.savefig(fig, bbox_inches="tight")

    if create_png:
        # determine png path
        if png_path:
            png_out = png_path
        else:
            base, _ = os.path.splitext(output_pdf)
            png_out = f"{base}.png"
        png_dir = os.path.dirname(png_out) or "."
        os.makedirs(png_dir, exist_ok=True)
        fig.savefig(png_out, dpi=png_dpi, bbox_inches="tight")

    plt.close(fig)
