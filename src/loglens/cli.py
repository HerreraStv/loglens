from __future__ import annotations

import argparse
import sys
from pathlib import Path

from loglens.parser import LogSummary, analyze_file


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="loglens",
        description="Analyze an application log file and print a severity summary.",
    )
    parser.add_argument("log_file", type=Path, help="Path to the log file to analyze")
    parser.add_argument(
        "--level",
        type=str.upper,
        choices=["INFO", "WARNING", "ERROR"],
        help="Only count lines at this severity level (plus malformed lines)",
    )
    return parser


def format_summary(summary: LogSummary) -> str:
    return (
        f"Total lines analyzed: {summary.total}\n"
        f"  INFO:      {summary.info}\n"
        f"  WARNING:   {summary.warning}\n"
        f"  ERROR:     {summary.error}\n"
        f"  Malformed: {summary.malformed}"
    )


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)

    try:
        summary = analyze_file(args.log_file, level=args.level)
    except OSError as exc:
        print(f"loglens: could not read '{args.log_file}': {exc.strerror or exc}", file=sys.stderr)
        return 1

    print(format_summary(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
