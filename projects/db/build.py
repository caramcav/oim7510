import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import duckdb
    import polars as pl

    return (duckdb,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Babson PT Clinic — Building the Database

    This notebook builds `database.duckdb` from the CSV files in `data/`, which `make_data.py` wrote. It always rebuilds from nothing, so the database matches the `CREATE TABLE` statements and the CSV files every time it runs.
    """)
    return


@app.cell
def _():
    import datetime

    as_of = datetime.date(2026, 10, 31)
    as_of

    #as_of date will always be October 31, 2026, regardless of when the notebook is run. 
    return as_of, datetime


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return ask, database


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Tables
    """)
    return


@app.cell
def _(database, duckdb, mo):
    if database.exists():
        database.unlink()

    with duckdb.connect(database) as _con:
        _con.execute("""
            CREATE TABLE therapists (
                therapist_id INTEGER PRIMARY KEY,
                first_name   VARCHAR NOT NULL,
                last_name    VARCHAR NOT NULL,
                cred         VARCHAR NOT NULL CHECK (cred IN ('DPT', 'PTA')),
                email        VARCHAR NOT NULL UNIQUE,
                hire_date    DATE NOT NULL
            )
        """)
        _con.execute("""
            CREATE TABLE patients (
                patient_id              INTEGER PRIMARY KEY,
                first_name               VARCHAR NOT NULL,
                last_name                VARCHAR NOT NULL,
                DOB                       DATE NOT NULL,
                phone                     VARCHAR NOT NULL,
                email                     VARCHAR NOT NULL UNIQUE,
                insurance_member_number   VARCHAR
            )
        """)
        _con.execute("""
            CREATE TABLE treatments (
                treatment_id   INTEGER PRIMARY KEY,
                treatment_name VARCHAR NOT NULL UNIQUE,
                std_min        INTEGER NOT NULL CHECK (std_min > 0),
                price          DECIMAL(8, 2) NOT NULL CHECK (price > 0),
                int_cost       DECIMAL(8, 2) NOT NULL CHECK (int_cost >= 0)
            )
        """)
        _con.execute("""
            CREATE TABLE referrals (
                referral_id    INTEGER PRIMARY KEY,
                patient_id     INTEGER NOT NULL REFERENCES patients(patient_id),
                physician_name VARCHAR NOT NULL,
                ref_date       DATE NOT NULL,
                reason         VARCHAR NOT NULL
            )
        """)
        _con.execute("""
            CREATE TABLE appointments (
                appt_id      INTEGER PRIMARY KEY,
                patient_id   INTEGER NOT NULL REFERENCES patients(patient_id),
                therapist_id INTEGER NOT NULL REFERENCES therapists(therapist_id),
                start_date   DATE NOT NULL,
                start_time   TIME NOT NULL,
                length       INTEGER NOT NULL CHECK (length IN (30, 45, 60)),
                status       VARCHAR NOT NULL CHECK (status IN ('booked', 'completed', 'no-show')),
                UNIQUE (therapist_id, start_date, start_time)
            )
        """)
        _con.execute("""
            CREATE TABLE appointment_treatments (
                appt_id       INTEGER NOT NULL REFERENCES appointments(appt_id),
                treatment_id  INTEGER NOT NULL REFERENCES treatments(treatment_id),
                price_charged DECIMAL(8, 2) NOT NULL CHECK (price_charged > 0),
                minutes_spent INTEGER NOT NULL CHECK (minutes_spent > 0),
                PRIMARY KEY (appt_id, treatment_id)
            )
        """)

        _data = mo.notebook_dir() / "data"
        _con.execute(f"COPY therapists FROM '{_data / 'therapists.csv'}' (HEADER)")
        _con.execute(f"COPY patients FROM '{_data / 'patients.csv'}' (HEADER)")
        _con.execute(f"COPY treatments FROM '{_data / 'treatments.csv'}' (HEADER)")
        _con.execute(f"COPY referrals FROM '{_data / 'referrals.csv'}' (HEADER)")
        _con.execute(f"COPY appointments FROM '{_data / 'appointments.csv'}' (HEADER)")
        _con.execute(f"COPY appointment_treatments FROM '{_data / 'appointment_treatments.csv'}' (HEADER)")

        _con.execute("""
            CREATE VIEW no_show_rate_by_therapist AS
                SELECT
                    therapist_id,
                    count(*) FILTER (WHERE status = 'no-show') AS no_shows,
                    count(*) FILTER (WHERE status IN ('completed', 'no-show')) AS completed_and_no_shows,
                    count(*) FILTER (WHERE status = 'no-show') * 1.0
                        / count(*) FILTER (WHERE status IN ('completed', 'no-show')) AS no_show_rate
                FROM appointments
                GROUP BY therapist_id
        """)




    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT count(*) AS violations
        FROM appointments
        WHERE (start_date <= DATE '{as_of}' AND status = 'booked')
           OR (start_date > DATE '{as_of}' AND status IN ('completed', 'no-show'))
    """)
    return


@app.cell
def _(datetime, mo):
    #shows the last time csv file was updated

    import os
    datetime.datetime.fromtimestamp(os.path.getmtime(mo.notebook_dir() / "data" / "appointments.csv"))
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT
            CASE WHEN start_date <= DATE '{as_of}' THEN 'on or before as_of' ELSE 'after as_of' END AS period,
            status,
            count(*) AS n
        FROM appointments
        GROUP BY period, status
        ORDER BY period, status
    """)
    return


@app.cell
def _(ask):
    #Confirms that data generator's function worked to not have any appointments with the same therapist overlap, even if they have different start times. 

    ask(f"""
        SELECT
            a.appt_id AS appt_1,
            b.appt_id AS appt_2,
            a.therapist_id,
            a.start_date,
            a.start_time AS start_1,
            a.length    AS length_1,
            b.start_time AS start_2,
            b.length     AS length_2
        FROM appointments a
        JOIN appointments b
            ON a.therapist_id = b.therapist_id
           AND a.start_date   = b.start_date
           AND a.appt_id < b.appt_id
        WHERE a.start_time < b.start_time + INTERVAL (b.length) MINUTE
          AND b.start_time < a.start_time + INTERVAL (a.length) MINUTE
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. The Data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `make_data.py` writes the CSV files loaded above, with a fixed random seed (`42`) so it writes the same files every time.

    **The two rows that break a rule on purpose** (for business question 7, *"treatments given at an appointment take no more minutes than its length"*): two `appointment_treatments` rows, picked at random each run of `make_data.py` and printed to the terminal when it runs, carry a `minutes_spent` that pushes the total over their appointment's `length`. Our tables do not refuse these rows, because minutes-vs-length is a rule across two tables, not a single-column `CHECK` — so these two rows load successfully and business question 7 has to find them with a query instead.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. A Look at the Data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Appointments spread roughly evenly across weekdays, since `make_data.py` picks a day at random with no weekday weighting — a real clinic would likely book fewer appointments on weekends. If this mattered for the business questions, `make_data.py` could draw `start_date` only from Monday–Friday.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Row Counts
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. A Row It Refuses
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The insert above tries a treatment priced at `$0.00`, which breaks the rule "a price charged is more than zero." The `CHECK (price > 0)` constraint on `treatments` refuses it, and the error message above shows that refusal.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Answers You Already Knew
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. A View
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `no_show_rate_by_therapist`, created above alongside the tables, answers the question a manager would ask every week: how often does each therapist's patients not show up? It stays current because it is a view, not a saved table — every `ask` against it re-reads the latest `appointments` rows.
    """)
    return


if __name__ == "__main__":
    app.run()
