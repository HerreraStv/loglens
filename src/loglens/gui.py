from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, ttk

from loglens.cli import format_summary
from loglens.parser import analyze_file

LEVELS = ["All", "INFO", "WARNING", "ERROR"]


def run_analysis(path: str, level: str) -> str:
    """Analyze `path` (optionally filtered by `level`) and return summary text, or a friendly message if nothing can be analyzed."""
    if not path:
        return "Please select a log file first."
    try:
        summary = analyze_file(path, level=None if level == "All" else level)
    except OSError as exc:
        return f"Could not read '{path}': {exc.strerror or exc}"
    except UnicodeDecodeError:
        return "LogLens can only analyze UTF-8 text log files."
    return format_summary(summary)


class LogLensApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("LogLens")

        self.path_var = tk.StringVar()
        self.level_var = tk.StringVar(value="All")
        self.result_var = tk.StringVar(value="Results will appear here.")

        file_row = ttk.Frame(root, padding=10)
        file_row.pack(fill="x")
        ttk.Label(file_row, text="Log file:").pack(anchor="w")
        picker_row = ttk.Frame(file_row)
        picker_row.pack(fill="x")
        ttk.Entry(picker_row, textvariable=self.path_var, state="readonly").pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(picker_row, text="Browse", command=self._browse).pack(
            side="left", padx=(5, 0)
        )

        level_row = ttk.Frame(root, padding=10)
        level_row.pack(fill="x")
        ttk.Label(level_row, text="Severity:").pack(anchor="w")
        ttk.Combobox(
            level_row, textvariable=self.level_var, values=LEVELS, state="readonly"
        ).pack(fill="x")

        ttk.Button(root, text="Analyze", command=self._analyze).pack(pady=10)

        ttk.Label(
            root, textvariable=self.result_var, justify="left", padding=10
        ).pack(fill="both", expand=True)

    def _browse(self) -> None:
        path = filedialog.askopenfilename(title="Select a log file")
        if path:
            self.path_var.set(path)

    def _analyze(self) -> None:
        self.result_var.set(run_analysis(self.path_var.get(), self.level_var.get()))


def main() -> None:
    root = tk.Tk()
    LogLensApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
