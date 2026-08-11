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


def test_analyze_lines_level_none_matches_unfiltered_behavior():
    lines = [
        "2026-01-01T00:00:00Z INFO api hello",
        "2026-01-01T00:00:01Z WARNING api careful",
        "2026-01-01T00:00:02Z ERROR api boom",
        "THIS LINE IS DELIBERATELY MALFORMED",
    ]
    assert analyze_lines(lines, level=None) == analyze_lines(lines)


def test_analyze_lines_filter_excludes_other_levels_but_keeps_malformed():
    lines = [
        "2026-01-01T00:00:00Z INFO api hello",
        "2026-01-01T00:00:01Z WARNING api careful",
        "2026-01-01T00:00:02Z ERROR api boom",
        "2026-01-01T00:00:03Z ERROR api boom again",
        "THIS LINE IS DELIBERATELY MALFORMED",
    ]
    summary = analyze_lines(lines, level="ERROR")
    assert summary == LogSummary(total=5, info=0, warning=0, error=2, malformed=1)


def test_analyze_lines_filter_with_no_malformed_lines():
    lines = [
        "2026-01-01T00:00:00Z INFO api hello",
        "2026-01-01T00:00:01Z WARNING api careful",
    ]
    summary = analyze_lines(lines, level="INFO")
    assert summary == LogSummary(total=2, info=1, warning=0, error=0, malformed=0)


def test_analyze_lines_filter_does_not_change_total():
    lines = [
        "2026-01-01T00:00:00Z INFO api hello",
        "2026-01-01T00:00:01Z WARNING api careful",
        "2026-01-01T00:00:02Z ERROR api boom",
        "THIS LINE IS DELIBERATELY MALFORMED",
    ]
    unfiltered_total = analyze_lines(lines).total
    for level in ("INFO", "WARNING", "ERROR"):
        assert analyze_lines(lines, level=level).total == unfiltered_total


def test_analyze_file_filters_by_level():
    summary = analyze_file(SAMPLE_LOG, level="ERROR")
    assert summary.total == 14
    assert summary.info == 0
    assert summary.warning == 0
    assert summary.error == 3
    assert summary.malformed == 1
