# LogLens — Claude Code Learning Sandbox

# LogLens

LogLens is a small Python command-line tool for analyzing application log files.

This repository is also a hands-on learning sandbox for studying professional AI-assisted software development with Claude Code.

## Current Status

The project scaffold is complete.

Version 1 of the log analyzer is implemented: it accepts a log file path, reads it safely, and reports counts of INFO, WARNING, ERROR, and malformed lines along with the total lines analyzed. See `SPEC.md` for the requirements.

## Development

Install the project in editable mode:

    python -m pip install -e .

This is what creates the `loglens` executable: `pyproject.toml` declares a
`[project.scripts]` entry point (`loglens = "loglens.cli:main"`), and `pip`
turns that into a real executable inside the virtualenv —
`.venv/Scripts/loglens.exe` on Windows, `.venv/bin/loglens` on macOS/Linux.

Run the CLI (works as the bare `loglens` command once the venv is
activated, e.g. `.venv/Scripts/Activate.ps1`; otherwise invoke it by its
full path):

    loglens <path-to-log-file>

Run the tests:

    python -m pytest