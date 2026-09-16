# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Set up your machine and push a notebook.

Session 1 of OIM7510 and OIM6301, second half.

Nothing here reads a data file, so nothing here depends on your network.

AUTHORING NOTES.

Every markdown cell carries `hide_code=True`, so a student sees the rendered
prose without the `mo.md` wrapper around it. Keep it on any cell that is only
markdown, and leave it off any cell whose code a student should read.

The four experiments ask a student to edit, delete and reorder cells, which
`--mode run` cannot do. This is written for `marimo edit` on the student's own
machine, which is what session 1 spends an hour setting up. A published copy has
to be exported `--mode edit`, and whether an edited cell re-executes there is
still unsettled: `.claude/rules/marimo-notebooks.md`.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="pandas")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    print('hi')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Set Up Your Machine and Push a Notebook
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ▶️ A Name Holding Several Things

    A name holds a value. `=` puts the value there. It means *put this in that*.

    The five numbers below are the freight charged on orders `10248` through
    `10252`. Order `10248` is the one from the slides.
    """)
    return


@app.cell
def _():
    freight = [16.75, 22.25, 18.00, 20.25, 36.25]
    freight
    return (freight,)


@app.cell
def _(freight):
    print(f"Number of freight charges: {len(freight)}")
    return


@app.cell
def _(freight):
    print(f"Max freight charge: {max(freight)}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ✏️ Your Turn: Three Cells

    Add three cells below with the **+** button. One line in each.

    1. The freight on the **first** order: `freight[0]`
    2. **How many** orders there are: `len(freight)`
    3. The **total**: `total = sum(freight)`, then `total` on the next line

    Keep them in separate cells. The next section needs them separate.

    *Python counts from zero, so `freight[0]` is the first one.*
    """)
    return


@app.cell
def _(freight):
    freight[0]
    return


@app.cell
def _(freight):
    len(freight)
    return


@app.cell
def _(freight):
    total = sum(freight)
    total
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🙋 Guess First: Four Questions

    Write all four answers down before you run anything.

    1. Cell A says `x = 5`. Cell B says `print(x)`. You change A to `x = 50`.
       **What does B print?**
    2. Cell A says `orders = 3`. Cell B says `orders * 12`. You **delete cell A**.
       **What happens to B?**
    3. Two different cells both say `total = ...`. **What happens?**
    4. You put `print(total)` **above** the cell that says `total = 5`.
       **Does it run?**

    Four experiments follow. Do them in order, and undo each one before the next.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    1. x will print 50
    2. B will print 0 since there is no value associated with cell A
    3. total is printed out twice
    4. no, it doesn't run since total is not defined
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Experiment 1

    Change `16.75` to `999.99` in the freight cell. Run only that cell.

    Watch your three cells.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Experiment 2

    Delete the freight cell. Watch your three cells.

    Then bring it back: undo, or type the line again.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Experiment 3

    Add a cell anywhere and put `total = 1` in it.

    Delete it again once you have seen what happens.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Experiment 4

    Drag the cell holding `total = sum(freight)` **below** the cell that shows
    `total`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ▶️ What Happened

    1. **Everything that used the number recomputed by itself.** You ran one cell.
    2. **The cells using the deleted name went blank.** None of them kept showing a
       value whose source is gone.
    3. **An error, straight away.** A name is defined in exactly one cell, so there
       is no way to be looking at a `total` that some other cell changed.
    4. **It ran.** This notebook works out what depends on what and runs in that
       order. Where a cell sits on the page is a layout choice.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # ✏️ Your Turn: Push It

    1. Change one number in the freight list. Watch your three cells update.
    2. Save the file **inside your repository, in the `notebooks/` folder**.
    3. In **GitHub Desktop**: write a commit message, click **Commit to main**,
       then **Push origin**.
    4. Open **github.com**, go to your repository, and click on the notebook.

    *Nothing there? Check that GitHub Desktop is showing the right repository at
    the top left, and that the file you saved is inside that repository's folder.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 🚀 This Week: Ask For Something You Cannot Write Yet

    You have five freight charges and three lines of Python. Get a fourth line you could not have written.

    1. **Pick something you want to know about `freight`** that the cells above do not show: the average, the largest, how many are above 22.
    2. **Ask your agent for it.** Show it the list and state what you want back.
    3. **Paste what it gives you into a new cell and run it.** If it errors, keep the error.
    4. **Add a markdown cell underneath.** What does the line do, in your words, and **which part of it are you unsure about?**
    5. **Commit and push.**

    Week one is too early to account for a line you did not write. Name the part you cannot.

    *New to markdown? The [Markdown guide](https://oim7510.github.io/guides/markdown/) is a ten-minute read, and we cover it properly next session.*
    """)
    return


@app.cell
def _(freight):
    print(f"Max freight charge: {max(freight)}")

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The code in the cell above determines the maximum value that's part of the "freight" set of numbers. It also prints "New freight charge" before the output of the max calculation. I am not sure the function of the f" in the beginning of the code.
    """)
    return


if __name__ == "__main__":
    app.run()
