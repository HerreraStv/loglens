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

## Desktop Interface (Level 1)

A minimal Tkinter desktop GUI is approved as a thin frontend over the
same analyzer the CLI uses. It must not reimplement parsing or filtering.

18. Provide a file picker (Browse) to select a log file.
19. Provide a severity selector with `All`, `INFO`, `WARNING`, and
    `ERROR`. `All` calls the analyzer with no filter; `INFO`/`WARNING`/
    `ERROR` reuse the same filtering behavior as the CLI's `--level`.
20. Provide an Analyze action that runs the analysis and displays the
    result in the window.
21. Display the same summary fields as the CLI: Total lines analyzed,
    INFO, WARNING, ERROR, Malformed.
22. If no file is selected, or the selected file cannot be read, show a
    short friendly message in the window instead of crashing or exposing
    a traceback.
23. The GUI must call the existing analyzer (`analyze_file`) directly —
    no separate parser or filtering implementation inside the GUI module.

## Engineering Requirements

- Keep the implementation small and understandable.
- Avoid unnecessary dependencies.
- Separate parsing logic from CLI presentation where useful.
- Handle malformed input without crashing.

## Out of Scope

Do not implement yet:

- database
- AI analysis
- remote log ingestion
- HTTP API
- real-time streaming
- cloud services
- standalone executable packaging (e.g. PyInstaller) or installers
- any GUI functionality beyond the Level 1 desktop interface described
  above (no charts, tables, themes, tabs, or async behavior)