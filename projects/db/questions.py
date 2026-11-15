import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import polars as pl

    return duckdb, mo


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell
def _():
    #This section of code defines as_of date. as_of date will always be October 31, 2026, regardless of when the notebook is run. The same as_of date is included in make_data.py file. 

    import datetime

    as_of = datetime.date(2026, 10, 31)

    # "Last 30 days" = the 30 days ending on as_of (inclusive of as_of itself)
    last_30_days_end = as_of
    last_30_days_start = as_of - datetime.timedelta(days=29)

    # "Last month" = the last full calendar month before as_of
    last_month_end = as_of.replace(day=1)
    if last_month_end.month == 1:
        last_month_start = last_month_end.replace(year=last_month_end.year - 1, month=12)
    else:
        last_month_start = last_month_end.replace(month=last_month_end.month - 1)

    as_of
    return last_month_end, last_month_start


@app.cell
def _(ask):
    #Adding descriptions of tables to assist in questions 
    ask("SHOW TABLES")
    return


@app.cell
def _(ask):
    ask("DESCRIBE appointments")
    return


@app.cell
def _(ask):
    ask("DESCRIBE appointment_treatments")
    return


@app.cell
def _(ask):
    ask("DESCRIBE therapists")
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Each therapist's completed appointments last month, and the revenue from them
    """)
    return


@app.cell
def _(ask, last_month_end, last_month_start):
    therapist_revenue = ask(f"""
    WITH appt_revenue AS (
        SELECT appt_id, SUM(price_charged) AS revenue
        FROM appointment_treatments
        GROUP BY appt_id
    )
    SELECT
        t.therapist_id,
        t.first_name,
        t.last_name,
        COUNT(a.appt_id) AS completed_appointments,
        COALESCE(SUM(ar.revenue), 0) AS total_revenue
    FROM appointments a
    JOIN therapists t ON a.therapist_id = t.therapist_id
    LEFT JOIN appt_revenue ar ON a.appt_id = ar.appt_id
    WHERE a.status = 'completed'
      AND a.start_date >= DATE '{last_month_start}'
      AND a.start_date <  DATE '{last_month_end}'
    GROUP BY t.therapist_id, t.first_name, t.last_name
    ORDER BY t.therapist_id
    """)

    therapist_revenue

    return (therapist_revenue,)


@app.cell
def _(therapist_revenue):
    therapist_revenue_total = therapist_revenue["total_revenue"].sum()
    therapist_revenue_total
    return


@app.cell
def _():
    return


@app.cell
def _(ask, last_month_end, last_month_start):
    #Check total revenue for all appointments 
    ask(f"""
    SELECT
        SUM(att.price_charged) AS total_revenue_last_30_days
    FROM appointments a
    JOIN appointment_treatments att ON a.appt_id = att.appt_id
    WHERE a.status = 'completed'
      AND a.start_date >= DATE '{last_month_start}'
      AND a.start_date <= DATE '{last_month_end}'
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 2. The no-show rate for each therapist and for each day of the week
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 3. Patients whose last completed appointment was more than 90 days ago, with nothing booked, with a phone number
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 4. Revenue, cost and margin for each treatment, including treatments never given
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 5. Patients who were referred and have no appointment at all
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 6. One row per patient with their number of referrals and their number of appointments, each checked against counting it on its own
    """)
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 7. Every completed appointment checked against the rule that the treatments given at it take no more minutes than its length, and a list of any that break it
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # How I Know These Numbers Are Right
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Reach at least two of your answers a second way

    In this notebook, verify at least two of your answers from Part B a second way: a total against the sum of its parts, a count against counting the same rows another way, or a number against the row counts and the data you generated in Part A.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 2. Working With the Agent

    Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell. If the agent got it right the first time: What did you do to verify that?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For question 1, I added a check to confirm that the revenue per therapist calculated in my first table is the same as the total revenue calculated from adding the price_charged for all appointments within the date range together. Those numbers did not match, so I dug into the code and saw that the date criteria was different within the two queries.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 3. Reading It Back

    The question you picked before answering any, with the prediction you committed then as db: prediction: how many rows you expect its joins to produce before any grouping, and why. Then run the joins alone, count the rows, and write whether your prediction matched and why. Then write, in your own words, what one row of the final result means.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    db: prediction for Question 6.

    The total number of rows before grouping will be about 3,450. I'm predicting this because there will be 150 rows from the referrals table, 3000 rows from the appointments table, and 300 rows from the patients table since that is how many rows those tables have currently. The patient id number for each will be included in the initial join, then those will be reduced to 300 rows to reflect one row per patients. One row of the final result will represent one patient and how many appointments and referals they have, including if they have none of each.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 4. Going Further

    What you tried past the main task, what you found, and where it is.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 5. Time Spent

    About how many hours the whole project took you outside class, as one number. It is not graded.
    """)
    return


if __name__ == "__main__":
    app.run()
