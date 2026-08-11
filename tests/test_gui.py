from loglens.cli import format_summary
from loglens.gui import run_analysis
from loglens.parser import analyze_file

_SAMPLE_LINES = (
    "2026-01-01T00:00:00Z INFO api hello\n"
    "2026-01-01T00:00:01Z WARNING api careful\n"
    "2026-01-01T00:00:02Z ERROR api boom\n"
    "THIS LINE IS DELIBERATELY MALFORMED\n"
)


def test_run_analysis_no_path_selected():
    result = run_analysis("", "All")
    assert result == "Please select a log file first."


def test_run_analysis_missing_file():
    result = run_analysis("does/not/exist.log", "All")
    assert "does/not/exist.log" in result
    assert "Traceback" not in result


def test_run_analysis_all_matches_unfiltered_analyzer(tmp_path):
    log_file = tmp_path / "sample.log"
    log_file.write_text(_SAMPLE_LINES, encoding="utf-8")

    result = run_analysis(str(log_file), "All")

    assert result == format_summary(analyze_file(log_file))


def test_run_analysis_level_filters_without_changing_total(tmp_path):
    log_file = tmp_path / "sample.log"
    log_file.write_text(_SAMPLE_LINES, encoding="utf-8")

    result = run_analysis(str(log_file), "ERROR")

    assert "Total lines analyzed: 4" in result
    assert "INFO:      0" in result
    assert "WARNING:   0" in result
    assert "ERROR:     1" in result
    assert "Malformed: 1" in result


def test_run_analysis_invalid_utf8_file_returns_friendly_message(tmp_path):
    log_file = tmp_path / "binary.log"
    log_file.write_bytes(b"\xff\xfe\x00\x00not valid utf-8 \x80\x81")

    result = run_analysis(str(log_file), "All")

    assert result == "LogLens can only analyze UTF-8 text log files."
