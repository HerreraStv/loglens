# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

LogLens is a small Python CLI tool that analyzes application log files and
prints a severity summary (INFO/WARNING/ERROR counts, malformed-line count,
total lines). This repo also serves as a learning sandbox for practicing
AI-assisted development — expect the human to want to review and understand
changes, not just receive a finished diff.

The authoritative requirements are in `SPEC.md`. Read it before implementing
or changing behavior. Do not treat this file as a substitute for it.

## Current state

The project is a scaffold only. `src/loglens/cli.py` is a stub — the actual
parser has not been implemented yet. This is intentional, not a bug.

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

GUI, database, AI-based analysis, remote log ingestion, HTTP API,
real-time streaming, cloud services. If a task seems to call for one of
these, stop and ask rather than assuming scope has expanded.

## Project layout

- `src/loglens/` — package source (src-layout)
- `tests/` — pytest tests, run with `python -m pytest`
- `samples/application.log` — sample log fixture (includes INFO/WARNING/
  ERROR lines and one deliberately malformed line) for exercising the parser
- `SPEC.md` — v1 requirements, source of truth for behavior

## Workflow

- Install: `python -m pip install -e .`
- Run (currently a stub — prints a placeholder, takes no arguments):
  `loglens`
- Test: `python -m pytest`
- Once argument parsing and the analyzer are implemented per SPEC.md, this
  section should be updated to document the real invocation
  (`loglens <path-to-log-file>`) and its exit-code behavior.
- Every new behavior in SPEC.md's requirements list should have a
  corresponding test — the current test suite is only a smoke test and
  needs real coverage as the parser is built.
