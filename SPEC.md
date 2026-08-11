# LogLens — Version 1 Specification

## Purpose

LogLens is a small command-line application that analyzes application log files and produces a simple severity summary.

## Version 1 Requirements

LogLens must:

1. Accept the path to a log file from the command line.
2. Read the file safely.
3. Count lines containing INFO.
4. Count lines containing WARNING.
5. Count lines containing ERROR.
6. Count malformed or unrecognized lines separately.
7. Display the total number of lines analyzed.
8. Display a readable summary.
9. Handle a missing file without an unhandled traceback.
10. Return a non-zero exit code when the file cannot be analyzed.
11. Include automated tests for important behavior.

## Severity Filtering (`--level`)

LogLens must support an optional `--level` flag that narrows the summary
to a single severity:

12. Accept `INFO`, `WARNING`, or `ERROR` as valid values for `--level`.
13. Accept level input case-insensitively (`--level error` is equivalent
    to `--level ERROR`).
14. Filtering changes only the severity counters: lines belonging to a
    valid level other than the one requested are excluded from the
    INFO/WARNING/ERROR counts.
15. "Total lines analyzed" always counts every non-empty line LogLens
    examined, whether or not `--level` is set — filtering never reduces
    this count.
16. Malformed-line counting is unaffected by filtering: malformed lines
    are always counted and reported, regardless of `--level`.
17. Reject invalid `--level` values cleanly — non-zero exit code, no
    unhandled traceback.

## Engineering Requirements

- Keep the implementation small and understandable.
- Avoid unnecessary dependencies.
- Separate parsing logic from CLI presentation where useful.
- Handle malformed input without crashing.

## Out of Scope

Do not implement yet:

- GUI
- database
- AI analysis
- remote log ingestion
- HTTP API
- real-time streaming
- cloud services