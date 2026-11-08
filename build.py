import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import polars as pl
    import requests

    return duckdb, mo


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return


@app.cell
def _(mo):
    mo.md(f"""
    **1. The Tables.** One CREATE TABLE for each table in your ERD, with every
    primary key and foreign key declared, and with NOT NULL, CHECK, UNIQUE and
    DEFAULT where the scenario's rules call for them. Chapter D of the SQL
    handbook, §24, has the syntax.
    """)
    return


@app.cell
def _(mo):
    mo.md(f"""
    **2. The Data.** Ask your agent for a script, projects/db/make_data.py, that writes data for every table as CSV files in projects/db/data/, and load them. The data has to obey every rule, with one exception: for each question marked (checks a rule) on your list, break its rule on purpose in exactly two rows, and write down which two in this section. If your tables make the database refuse those rows, your design holds that rule with a constraint: say so here, and show the refusal in that question's answer instead. It has to cover the 12 months up to a date you choose, your as_of date, which Part B uses. You can start from this prompt. Replace each part in angle brackets, brackets included, with your own text:

    Here are the CREATE TABLE statements for my database: <your CREATE TABLE statements>.
    Write a Python script, projects/db/make_data.py, that writes one CSV file
    per table into projects/db/data/.
    - Follow every rule of my scenario: <your scenario's rules>.
    - Break these rules on purpose, each in exactly two rows, and print which rows:
      <the rules your checking questions are about>.
    - Make <your scenario's amounts of data>, covering the 12 months up to <your as_of date>.
    - Include on purpose some rows with nothing attached, such as <one from your scenario>.
    - Use a fixed random seed, so that the script writes the same files every time.
    Copy
    Your scenario says how much data it needs; for your own domain, at least 10 rows in each table that lists things the business keeps and 1,000 rows across the tables that record what happens. Include on purpose some rows with nothing attached, so that the questions about them have an answer. Read the data before you keep it, because an agent's first try usually breaks a rule nobody wrote down: a task assigned before somebody started, a sale of shares nobody held, two appointments at once, a price nobody would charge.
    """)
    return


@app.cell
def _(mo):
    mo.md(f"""
    **3. A Look at the Data.** Read one of your CSV files with polars and chart one column whose shape you can judge, such as appointments by day of the week, orders by hour, or one asset's closing prices. Write one sentence on whether a real business would look like that, and if it would not, what you changed in make_data.py.
    """)
    return


@app.cell
def _(mo):
    mo.md(f"""
    **4. Row Counts.** Every table with its number of rows.
    """)
    return


@app.cell
def _(mo):
    mo.md(f"""
    **5. A Row It Refuses.** Insert one row that breaks one of your rules, and show the message the database gives back. ask() only reads, so open a short write connection of its own for the insert, with duckdb.connect(database) as _con:, the way notebook 6 does, and put it inside try and except, so that the rest of the notebook still runs.
    """)
    return


@app.cell
def _(mo):
    mo.md(f"""
    **6. Answers You Already Knew.** Three queries whose answers you knew before you ran them, because you know what you asked your agent for, with the answer you expected written next to each.
    """)
    return


@app.cell
def _(mo):
    mo.md(f"""
    **7. A View.** One question the business would ask every week, saved with CREATE VIEW in the cell that builds the database, so that anybody can ask for it by name and always get the current rows. Notebook 6 covers views in section 5, after GROUP BY. At least one of your answers in Part B must use it. Chapter D of the SQL handbook, §28.
    """)
    return


if __name__ == "__main__":
    app.run()
