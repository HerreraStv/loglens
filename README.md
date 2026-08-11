# LogLens

LogLens is a small tool that reads through an application's log file and
tells you, at a glance, how healthy things look. You can use it either
from the command line or through a basic desktop window — both work the
same way under the hood.

This repository is also a hands-on learning sandbox for studying
professional AI-assisted software development with Claude Code.

## What problem does it solve?

A log file is a text file an application writes to while it's running,
recording what it did — normal activity, warnings, and outright errors,
all mixed together. These files get long fast, and scrolling through
thousands of lines by hand just to answer "how many things went wrong
today?" is slow and easy to get wrong.

LogLens reads the file for you and counts how many lines fall into each
category, so you get a short summary instead of a wall of text.

## What kind of log file does it read?

LogLens expects one entry per line, roughly in this shape:

    TIMESTAMP LEVEL COMPONENT MESSAGE

For example:

    2026-08-09T16:07:22Z ERROR payments Payment provider connection timeout

The second word — `ERROR` here — is the line's **severity level**, and
it's what LogLens uses to sort each line into a category:

- **INFO** — routine, expected activity (e.g. "server started").
- **WARNING** — something worth noticing, but not necessarily broken (e.g.
  a retry).
- **ERROR** — something went wrong.
- **Malformed** — a line that doesn't match the expected shape above, so
  LogLens can't tell what severity it is. These are counted separately
  rather than silently skipped, so you always know if part of the log is
  unreadable.

## What the output tells you

Running LogLens against a log file prints a short summary like this:

    Total lines analyzed: 14
      INFO:      7
      WARNING:   3
      ERROR:     3
      Malformed: 1

- **Total lines analyzed** is every non-empty line LogLens looked at.
- The four rows underneath break that total down by category.

## Usage

Install the project in editable mode (see [Development](#development) for
what this does):

    python -m pip install -e .

Run it against a log file:

    loglens <path-to-log-file>

### Filtering by severity

To focus on just one severity level, add `--level`:

    loglens <path-to-log-file> --level ERROR

Valid levels are `INFO`, `WARNING`, and `ERROR`, and you can type them in
any case — `--level error` works the same as `--level ERROR`.

Filtering only changes the **severity counters** (INFO/WARNING/ERROR).
Two things stay the same either way:

- **Total lines analyzed always counts every non-empty line in the file**,
  not just the ones matching the filter — it tells you how much of the
  file LogLens actually looked at.
- **Malformed lines are still counted and shown**, even while filtering by
  severity, since a malformed line is a data problem worth knowing about
  regardless of which level you asked for.

For example, filtering the log above with `--level ERROR` prints:

    Total lines analyzed: 14
      INFO:      0
      WARNING:   0
      ERROR:     3
      Malformed: 1

## Desktop interface

If you'd rather not type commands, LogLens also has a very basic desktop
window. It's intentionally simple — a small frontend on top of the same
analyzer the command line uses, not a separate program. Whatever you see
from the CLI, you get from the window too.

After installing the project (see [Usage](#usage) above), launch it with:

    python -m loglens.gui

A small window opens with:

1. A **Browse** button to pick a log file.
2. A **Severity** dropdown: `All`, `INFO`, `WARNING`, or `ERROR` — the
   same filtering described above, just chosen from a list instead of
   typed as `--level`.
3. An **Analyze** button that runs the analysis.
4. A results area showing the same summary the CLI prints (Total lines
   analyzed, INFO, WARNING, ERROR, Malformed).

If you click Analyze before picking a file, or point it at a file that
can't be read, you'll get a short plain-language message in the results
area instead of a crash.

This is a "Level 1" GUI on purpose — plain and functional, not
polished. It exists so you have a no-typing option, not to replace the
command line.

## Development

Install the project in editable mode:

    python -m pip install -e .

This is what creates the `loglens` executable: `pyproject.toml` declares a
`[project.scripts]` entry point (`loglens = "loglens.cli:main"`), and `pip`
turns that into a real executable inside the virtualenv —
`.venv/Scripts/loglens.exe` on Windows, `.venv/bin/loglens` on macOS/Linux.
It's usable as the bare `loglens` command once the venv is activated
(e.g. `.venv/Scripts/Activate.ps1`), or invoked directly by its full path.

Run the tests:

    python -m pytest
