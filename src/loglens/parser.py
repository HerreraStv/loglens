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


def analyze_lines(lines: Iterable[str]) -> LogSummary:
    summary = LogSummary()
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        summary.total += 1
        level = classify_line(line)
        if level == "INFO":
            summary.info += 1
        elif level == "WARNING":
            summary.warning += 1
        elif level == "ERROR":
            summary.error += 1
        else:
            summary.malformed += 1
    return summary


def analyze_file(path: Path | str) -> LogSummary:
    with open(path, encoding="utf-8") as f:
        return analyze_lines(f)
