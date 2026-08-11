# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

LogLens is a small Python tool that analyzes application log files and
prints a severity summary (INFO/WARNING/ERROR counts, malformed-line count,
total lines). It has two interfaces — a CLI and a minimal Tkinter desktop
GUI — both thin callers over the same analyzer in `parser.py`. This repo
also serves as a learning sandbox for practicing AI-assisted development —
expect the human to want to review and understand changes, not just
receive a finished diff.

The authoritative requirements are in `SPEC.md`. Read it before implementing
or changing behavior. Do not treat this file as a substitute for it.

## Current state

The core parser, CLI, and a Level 1 desktop GUI are all implemented per
`SPEC.md`. `loglens <path-to-log-file>` reads a log file and prints a
severity summary (INFO/WARNING/ERROR and malformed-line counts, plus total
lines analyzed). An optional `--level` flag (`INFO`, `WARNING`, or `ERROR`,
case-insensitive) filters the summary to a single severity: filtering only
changes the severity counters — the total and malformed counts always
reflect every non-empty line examined. `python -m loglens.gui` opens a
basic window (Browse, a severity dropdown, Analyze, and a results area)
that calls the exact same `analyze_file` function the CLI uses — it does
not have its own parsing or filtering logic.

Parsing and filtering logic belongs in `parser.py` only. Interfaces (CLI,
GUI, or any future one) must call into it rather than reimplementing any
part of it — this has been the pattern since the GUI was added and should
continue.

## Engineering constraints (from SPEC.md)

- Keep the implementation small and understandable.
- Avoid adding dependencies beyond the standard library unless there's a
  strong reason — ask before adding one.
- Separate parsing logic from CLI presentation (e.g., a parser module the
  CLI calls into, not logic embedded directly in `main()`).
- Handle malformed input without crashing; count malformed lines separately
  rather than skipping or erroring on them.
- Missing/unreadable files must fail cleanly: no raw traceback, non-zero
  exit code.

## Out of scope — do not implement without explicit request

Database, AI-based analysis, remote log ingestion, HTTP API, real-time
streaming, cloud services, standalone executable packaging (e.g.
PyInstaller) or installers, and any GUI functionality beyond the Level 1
desktop interface already implemented (no charts, tables, themes, tabs,
or async behavior). If a task seems to call for one of these, stop and
ask rather than assuming scope has expanded.

## Project layout

- `src/loglens/` — package source (src-layout)
  - `parser.py` — the analyzer (`analyze_file`/`analyze_lines`); the only
    place parsing/filtering logic should live
  - `cli.py` — command-line interface, calls into `parser.py`
  - `gui.py` — Tkinter desktop interface, calls into `parser.py` and
    reuses `cli.py`'s `format_summary`
- `tests/` — pytest tests, run with `python -m pytest`
- `samples/application.log` — sample log fixture (includes INFO/WARNING/
  ERROR lines and one deliberately malformed line) for exercising the parser
- `SPEC.md` — v1 requirements, source of truth for behavior

## Workflow

- Install: `python -m pip install -e .`
- Run:
  - `loglens <path-to-log-file>`
  - `loglens <path-to-log-file> --level ERROR` (filter to one severity;
    `INFO`/`WARNING`/`ERROR`, case-insensitive)
  - `python -m loglens.gui` (desktop interface)
- Test: `python -m pytest`
- Every behavior listed in SPEC.md's requirements should have a
  corresponding test — keep this true as the project grows.
