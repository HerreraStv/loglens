from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

_LEVELS = {"INFO", "WARNING", "ERROR"}


@dataclass
class LogSummary:
    total: int = 0
    info: int = 0
    warning: int = 0
    error: int = 0
    malformed: int = 0


def classify_line(line: str) -> str | None:
    """Return the severity level of a log line, or None if unrecognized.

    Expects the level as the second whitespace-separated token
    (`TIMESTAMP LEVEL COMPONENT MESSAGE`), matching the sample log format.
    """
    tokens = line.split()
    if len(tokens) >= 2 and tokens[1] in _LEVELS:
        return tokens[1]
    return None


def analyze_lines(lines: Iterable[str], level: str | None = None) -> LogSummary:
    """`total`/`malformed` count every non-blank line; `level` only gates the severity counters."""
    summary = LogSummary()
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        summary.total += 1
        detected = classify_line(line)
        if detected is None:
            summary.malformed += 1
        elif level is None or detected == level:
            if detected == "INFO":
                summary.info += 1
            elif detected == "WARNING":
                summary.warning += 1
            elif detected == "ERROR":
                summary.error += 1
    return summary


def analyze_file(path: Path | str, level: str | None = None) -> LogSummary:
    with open(path, encoding="utf-8") as f:
        return analyze_lines(f, level=level)
