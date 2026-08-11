from pathlib import Path

import pytest

from loglens.parser import LogSummary, analyze_file, analyze_lines

SAMPLE_LOG = Path(__file__).resolve().parents[1] / "samples" / "application.log"


def test_analyze_lines_counts_by_level():
    lines = [
        "2026-01-01T00:00:00Z INFO api hello",
        "2026-01-01T00:00:01Z WARNING api careful",
        "2026-01-01T00:00:02Z ERROR api boom",
        "2026-01-01T00:00:03Z INFO api world",
    ]
    summary = analyze_lines(lines)
    assert summary == LogSummary(total=4, info=2, warning=1, error=1, malformed=0)


def test_analyze_lines_counts_malformed_lines():
    lines = [
        "2026-01-01T00:00:00Z INFO api hello",
        "THIS LINE IS DELIBERATELY MALFORMED",
    ]
    summary = analyze_lines(lines)
    assert summary.total == 2
    assert summary.info == 1
    assert summary.malformed == 1


def test_analyze_lines_skips_blank_lines():
    summary = analyze_lines(["", "   ", "\n"])
    assert summary.total == 0


def test_analyze_file_reads_from_disk(tmp_path):
    log_file = tmp_path / "sample.log"
    log_file.write_text(
        "2026-01-01T00:00:00Z INFO api hello\n"
        "2026-01-01T00:00:01Z ERROR api boom\n",
        encoding="utf-8",
    )
    summary = analyze_file(log_file)
    assert summary.total == 2
    assert summary.info == 1
    assert summary.error == 1


def test_analyze_file_missing_file_raises_oserror():
    with pytest.raises(OSError):
        analyze_file("does/not/exist.log")


def test_analyze_file_sample_log():
    summary = analyze_file(SAMPLE_LOG)
    assert summary.total == 14
    assert summary.info == 7
    assert summary.warning == 3
    assert summary.error == 3
    assert summary.malformed == 1
