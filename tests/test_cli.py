from loglens.cli import main


def test_main_returns_zero_and_prints_summary(tmp_path, capsys):
    log_file = tmp_path / "sample.log"
    log_file.write_text(
        "2026-01-01T00:00:00Z INFO api hello\n"
        "2026-01-01T00:00:01Z WARNING api careful\n"
        "2026-01-01T00:00:02Z ERROR api boom\n"
        "THIS LINE IS DELIBERATELY MALFORMED\n",
        encoding="utf-8",
    )

    exit_code = main([str(log_file)])

    assert exit_code == 0
    out = capsys.readouterr().out
    assert "Total lines analyzed: 4" in out
    assert "INFO" in out
    assert "WARNING" in out
    assert "ERROR" in out
    assert "Malformed" in out


def test_main_missing_file_returns_nonzero_without_traceback(capsys):
    exit_code = main(["does/not/exist.log"])

    assert exit_code == 1
    err = capsys.readouterr().err
    assert "exist.log" in err
    assert "Traceback" not in err
