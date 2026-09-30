# Rules for my agent

I am a graduate business student learning Python and SQL for analytics. Treat me as a careful beginner who has never worked as a developer.

## How to help me

- Write the simplest code that works. Prefer plain `for` loops, `if`, lists and dicts. Use a comprehension, a lambda or a class only when I ask for one.
- Explain, without being asked, any line I could not have written myself, in one sentence.
- If your code skips rows, converts values or changes a type, tell me how many rows it affected.
- When my request is ambiguous, ask me one question before you write anything.
- Keep answers short. Leave out the preamble, the emoji headings and the summary of what you just did.

## Notebooks

- My notebooks are marimo files. A name can be defined in only one cell. A cell shows its last expression, so end a chart cell with the chart and never call `plt.show()`.
- I start marimo from the repository folder with `uv run marimo edit`.

## Environment

- This repository is a uv project. Add a package with `uv add <package>` and run anything with `uv run`. Never use `pip`, `conda`, `python -m venv` or `uv pip install`, because none of them records the package in `pyproject.toml`, so the next `uv sync` or another computer will not have it.
