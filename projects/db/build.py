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


    return duckdb, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Babson PT Clinic — Building the Database

    This notebook builds `database.duckdb` from the CSV files in `data/`, which `make_data.py` wrote. It always rebuilds from nothing, so the database matches the `CREATE TABLE` statements and the CSV files every time it runs.
    """)
    return


@app.cell
def _():
    #This section of code defines as_of date. as_of date will always be October 31, 2026, regardless of when the notebook is run. The same as_of date is included in make_data.py file. 

    import datetime

    as_of = datetime.date(2026, 10, 31)
    as_of
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
def _(as_of, database, duckdb, mo):
    #existing database is deleted if needed prior to generating new database. 
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

        _con.execute(f"""
        CREATE VIEW no_show_rate_last_week_by_therapist AS
            SELECT
                therapist_id,
                count(*) FILTER (WHERE status = 'no-show') AS no_shows,
                count(*) FILTER (WHERE status IN ('completed', 'no-show')) AS completed_and_no_shows,
                count(*) FILTER (WHERE status = 'no-show') * 1.0
                    / NULLIF(count(*) FILTER (WHERE status IN ('completed', 'no-show')), 0) AS no_show_rate
            FROM appointments
            WHERE start_date BETWEEN DATE '{as_of}' - INTERVAL 6 DAY AND DATE '{as_of}'
            GROUP BY therapist_id
    """)  

        _data = mo.notebook_dir() / "data"
        _con.execute(f"COPY therapists FROM '{_data / 'therapists.csv'}' (HEADER)")
        _con.execute(f"COPY patients FROM '{_data / 'patients.csv'}' (HEADER)")
        _con.execute(f"COPY treatments FROM '{_data / 'treatments.csv'}' (HEADER)")
        _con.execute(f"COPY referrals FROM '{_data / 'referrals.csv'}' (HEADER)")
        _con.execute(f"COPY appointments FROM '{_data / 'appointments.csv'}' (HEADER)")
        _con.execute(f"COPY appointment_treatments FROM '{_data / 'appointment_treatments.csv'}' (HEADER)")
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

    **The two rows that break a rule on purpose** (for business question 7, *"treatments given at an appointment take no more minutes than its length"*): two `appointment_treatments` rows, picked at random each run of `make_data.py` and printed to the terminal when it runs, carry a `minutes_spent` that pushes the total over their appointment's `length`. My tables do not refuse these rows, because minutes-vs-length is a rule across two tables, not a single-column `CHECK` — so these two rows load successfully and business question 7 has to find them with a query instead.
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
    #Code to confirm that as_of date used in make_data file is consistent with the as_of date in this file

    ask(f"""
        SELECT count(*) AS violations
        FROM appointments
        WHERE (start_date <= DATE '{as_of}' AND status = 'booked')
           OR (start_date > DATE '{as_of}' AND status IN ('completed', 'no-show'))
    """)
    return


@app.cell
def _(as_of, ask):
    #shows number of appointments with different statuses to show that all booked meetings are in the future and appointments in past have either completed or no-show status. 

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
    ## 3. A Look at the Data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Read one of your CSV files with polars and chart one column whose shape you can judge, such as appointments by day of the week, orders by hour, or one asset's closing prices. Write one sentence on whether a real business would look like that, and if it would not, what you changed in make_data.py.
    """)
    return


@app.cell
def _(mo, pl):
    #reads appointments.csv file and adds it to appointments_df dataframe and converts any date-like columns into real dates
    appointments_df = pl.read_csv(
        mo.notebook_dir()/"data"/"appointments.csv",
        try_parse_dates=True,
    )

    #create new dataframe showing days of week. %A chooses specifically full weekday name. 
    appointments_df = appointments_df.with_columns(
        pl.col("start_date").dt.strftime("%A").alias("day_of_week")
    )
    return (appointments_df,)


@app.cell
def _(appointments_df, pl):
    #Specifies day order 
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    #Groups appintments by dates of week
    day_counts = appointments_df.group_by("day_of_week").agg(pl.len().alias("n"))

    #Orders days of week based on day_order listing. 
    day_counts = day_counts.with_columns(
        pl.col("day_of_week").cast(pl.Enum(day_order))
    ).sort("day_of_week")


    #Bar chart that shows number of appointments per day of week
    chart = day_counts.plot.bar(x="day_of_week", y="n")

    chart
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A real business most likely would not have a similar number of appointments on every day, since it's more likely to be closed or have fewer apppointments on the weekend (Saturday and Sunday). This could be fixed in make_data.py by taking into account days of the week during random generation and not allowing Saturday and Sunday dates to be chosen.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I updated make_data.py file to include this constraint of no appointments on weekends. The bar chart reflects this update to have no weekend appointments.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Row Counts

    Every table with its number of rows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Every table with its number of rows.
    """)
    return


@app.cell
def _(ask):
    #wrote SQL query that counts number of rows for each table. 

    ask("""
        SELECT 'therapists' AS table_name, count(*) AS n_rows FROM therapists
        UNION ALL
        SELECT 'patients', count(*) FROM patients
        UNION ALL
        SELECT 'treatments', count(*) FROM treatments
        UNION ALL
        SELECT 'referrals', count(*) FROM referrals
        UNION ALL
        SELECT 'appointments', count(*) FROM appointments
        UNION ALL
        SELECT 'appointment_treatments', count(*) FROM appointment_treatments
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. A Row It Refuses

    A Row It Refuses. Insert one row that breaks one of your rules, and show the message the database gives back. ask() only reads, so open a short write connection of its own for the insert, with duckdb.connect(database) as _con:, the way notebook 6 does, and put it inside try and except, so that the rest of the notebook still runs.
    """)
    return


@app.cell
def _(database, duckdb):
    with duckdb.connect(database) as _con:
        try:
            _con.execute("""
                INSERT INTO therapists (therapist_id, first_name, last_name, cred, email, hire_date)
                VALUES (999, 'Test', 'Therapist', 'MD', 'test.therapist@example.com', '2026-01-01')
            """)
        except duckdb.ConstraintException as _error:
            print(_error)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Answers You Already Knew

    Three queries whose answers you knew before you ran them, because you know what you asked your agent for, with the answer you expected written next to each.
    """)
    return


@app.cell
def _(ask):
    #Query 1: First date of appointments should be 31Nov25

    ask("""
        SELECT min(start_date) AS first_appt_date
        FROM appointments
    """)
    return


@app.cell
def _(ask):
    #Query 2: Total number of appointments was specified as 3,000
    ask("""
        SELECT count(*) AS total_appointments
        FROM appointments
    """)
    return


@app.cell
def _(ask):
    #Query 3: Three options for appointment lengths should be 30, 45 and 60 minutes. 

    ask("""
        SELECT DISTINCT length
        FROM appointments
        ORDER BY length
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. A View

    One question the business would ask every week, saved with CREATE VIEW in the cell that builds the database, so that anybody can ask for it by name and always get the current rows. Notebook 6 covers views in section 5, after GROUP BY. At least one of your answers in Part B must use it. Chapter D of the SQL handbook, §28.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The view I created was a No Show Rate by therapist, which displays the rate both across the entire timeframe of appointments shown in the database and by the past 7 days. The data is originally grouped by therapist ID within the CREATE VIEW code. The data outputted by that Create View is joined with the therapist table so the therapist names can be displayed instead of the therapist ID numbers.
    """)
    return


@app.cell
def _(ask):
    #Table showing no-show rate for each therapist both overall and in the last 7 days. Both rates are calculated within using "Create View" in the code section where the database is generated. 
    ask("""
        SELECT
            t.first_name,
            t.last_name,
            round(v.no_show_rate * 100, 1) AS overall_no_show_rate_pct,
            round(w.no_show_rate * 100, 1) AS last_week_no_show_rate_pct
        FROM therapists t
        JOIN no_show_rate_by_therapist v ON t.therapist_id = v.therapist_id
        LEFT JOIN no_show_rate_last_week_by_therapist w ON t.therapist_id = w.therapist_id
        ORDER BY last_week_no_show_rate_pct DESC
    """)
    return


if __name__ == "__main__":
    app.run()
