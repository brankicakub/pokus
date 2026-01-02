import argparse
import os
from pathlib import Path
from typing import List, Optional, Tuple

from rich.prompt import Prompt, Confirm

from .plotter import plot_csv_to_pdf


def _split_list_arg(s: Optional[str]) -> Optional[List[str]]:
    if not s:
        return None
    items = [p.strip() for p in s.split(",") if p.strip()]
    return items or None


def _parse_range(s: Optional[str]) -> Optional[Tuple[float, float]]:
    if not s:
        return None
    parts = [p.strip() for p in s.split(",")]
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("Range must be two comma-separated numbers, e.g. 0,10")
    try:
        a, b = float(parts[0]), float(parts[1])
    except ValueError:
        raise argparse.ArgumentTypeError("Range values must be numeric")
    return (a, b)


def ask_options_for_file(path: str, defaults: dict = None):
    defaults = defaults or {}
    print(f"Configuring plot for {path}")
    parse_dates = defaults.get("parse_dates")
    if parse_dates is None:
        parse_dates = Confirm.ask("Parse first column as dates?", default=True)

    x_col = defaults.get("x_col")
    if x_col is None:
        x_col = Prompt.ask("X column (leave empty to use index or first column)", default="")
        if isinstance(x_col, str) and x_col.strip().lower() in {"y", "n", "yes", "no"}:
            x_col = ""

    y_cols_raw = defaults.get("y_cols_raw")
    if y_cols_raw is None:
        y_cols_raw = Prompt.ask(
            "Comma-separated Y columns (leave empty to use all numeric columns)", default=""
        )
        if isinstance(y_cols_raw, str) and y_cols_raw.strip().lower() in {"y", "n", "yes", "no"}:
            y_cols_raw = ""

    y_cols = _split_list_arg(y_cols_raw)

    title = defaults.get("title")
    if title is None:
        title = Prompt.ask("Plot title", default=Path(path).stem)

    x_label = defaults.get("x_label")
    if x_label is None:
        x_label = Prompt.ask("X label", default=(x_col or ""))

    y_label = defaults.get("y_label")
    if y_label is None:
        y_label = Prompt.ask("Y label", default="")

    return dict(
        parse_dates=bool(parse_dates),
        x_col=x_col or None,
        y_cols=y_cols,
        title=title,
        x_label=x_label or None,
        y_label=y_label or None,
    )


def cli(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(description="CSV to PDF plotter (line plots)")
    parser.add_argument("csv_files", nargs="+", help="One or more CSV files to plot")
    parser.add_argument("-o", "--out", help="Output PDF file or directory (one per CSV when omitted)")
    parser.add_argument("--parse-dates", action="store_true", help="Parse first column as dates")
    parser.add_argument("--no-parse-dates", dest="parse_dates", action="store_false", help="Don't parse dates")
    parser.set_defaults(parse_dates=None)
    parser.add_argument("--x-col", help="Column name to use for X axis")
    parser.add_argument("--y-cols", help="Comma-separated Y column names to plot")
    parser.add_argument("--title", help="Plot title")
    parser.add_argument("--x-label", help="X axis label")
    parser.add_argument("--y-label", help="Y axis label")
    parser.add_argument("--x-range", type=_parse_range, help="X axis range as 'min,max'")
    parser.add_argument("--y-range", type=_parse_range, help="Y axis range as 'min,max'")
    parser.add_argument("--png", action="store_true", help="Also produce PNG output alongside PDF")
    parser.add_argument("--png-out", help="PNG output file or directory")
    parser.add_argument("--png-dpi", type=int, default=150, help="PNG DPI (default 150)")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip interactive prompts and use defaults/flags")

    args = parser.parse_args(argv)

    y_cols_list = _split_list_arg(args.y_cols)

    for idx, csv_path in enumerate(args.csv_files):
        defaults = {
            "parse_dates": args.parse_dates if args.parse_dates is not None else None,
            "x_col": args.x_col,
            "y_cols_raw": args.y_cols,
            "title": args.title,
            "x_label": args.x_label,
            "y_label": args.y_label,
        }

        if args.yes:
            # non-interactive: build opts directly
            opts = dict(
                parse_dates=bool(args.parse_dates) if args.parse_dates is not None else True,
                x_col=args.x_col or None,
                y_cols=y_cols_list,
                title=args.title or Path(csv_path).stem,
                x_label=args.x_label or (args.x_col or None),
                y_label=args.y_label or None,
            )
        else:
            opts = ask_options_for_file(csv_path, defaults=defaults)

        # determine output path
        if args.out:
            out_path = Path(args.out)
            if out_path.is_dir() or (len(args.csv_files) > 1 and not str(out_path).endswith('.pdf')):
                out = str(out_path / f"{Path(csv_path).stem}.pdf")
            elif len(args.csv_files) > 1:
                # multiple files but single filename given - append index
                stem = out_path.stem
                out = str(out_path.with_name(f"{stem}-{idx+1}.pdf"))
            else:
                out = str(out_path)
        else:
            out = f"output/{Path(csv_path).stem}.pdf"

        # determine png path (if requested)
        png_out = None
        if args.png:
            if args.png_out:
                p = Path(args.png_out)
                if p.is_dir() or (len(args.csv_files) > 1 and not str(p).endswith('.png')):
                    png_out = str(p / f"{Path(csv_path).stem}.png")
                elif len(args.csv_files) > 1:
                    stem = p.stem
                    png_out = str(p.with_name(f"{stem}-{idx+1}.png"))
                else:
                    png_out = str(p)
            else:
                png_out = None

        print(f"Generating {out}...")
        try:
            plot_csv_to_pdf(
                csv_path,
                out,
                x_range=args.x_range,
                y_range=args.y_range,
                create_png=args.png,
                png_path=png_out,
                png_dpi=args.png_dpi,
                **opts,
            )
        except Exception as e:
            print(f"Error while plotting {csv_path}: {e}")
        else:
            print("Done.")


if __name__ == "__main__":
    cli()
