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
    return as_of, last_month_end, last_month_start


@app.cell
def _(last_month_end):
    last_month_end
    return


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
def _(ask):
    ask("SELECT DISTINCT status FROM appointments")
    return


@app.cell
def _(ask):
    ask("DESCRIBE no_show_rate_by_therapist")
    return


@app.cell
def _(ask):
    ask("DESCRIBE patients")
    return


@app.cell
def _(ask):
    ask("DESCRIBE treatments")
    return


@app.cell
def _(ask):
    ask("DESCRIBE referrals")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Each therapist's completed appointments last month, and the revenue from them
    """)
    return


@app.cell
def _(ask, last_month_end, last_month_start, mo):
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

    mo.vstack([
        mo.md(f"### Results for {last_month_start.strftime('%B %Y')}"),
        therapist_revenue
    ])

    return (therapist_revenue,)


@app.cell
def _(therapist_revenue):
    therapist_revenue_total = therapist_revenue["total_revenue"].sum()
    therapist_revenue_total
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
      AND a.start_date < DATE '{last_month_end}'
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 2. The no-show rate for each therapist and for each day of the week
    """)
    return


@app.cell
def _(ask, mo):
    therapist_no_show = ask("""
        SELECT first_name, last_name, overall_no_shows, overall_completed_and_no_shows, overall_no_show_rate_pct
        FROM no_show_rate_by_therapist
        ORDER BY overall_no_show_rate_pct DESC
    """)

    mo.vstack([
        mo.md(f"### No show rate for each therapist, overall and in last week"),
        therapist_no_show
    ])
    return (therapist_no_show,)


@app.cell
def _(ask, mo):
    day_of_week_no_show = ask("""
        SELECT
            strftime(start_date, '%A') AS day_of_week,
            dayofweek(start_date) AS day_num,
            COUNT(*) FILTER (WHERE status = 'no-show') AS no_shows,
            COUNT(*) FILTER (WHERE status IN ('no-show', 'completed')) AS completed_and_no_shows,
            ROUND(
                100.0 * COUNT(*) FILTER (WHERE status = 'no-show')
                / NULLIF(COUNT(*) FILTER (WHERE status IN ('no-show', 'completed')), 0),
                2
            ) AS no_show_rate_pct
        FROM appointments
        GROUP BY day_of_week, day_num
        ORDER BY day_num
    """)

    mo.vstack([
        mo.md(f"### No show rate for each day"),
        day_of_week_no_show
    ])
    return (day_of_week_no_show,)


@app.cell
def _(day_of_week_no_show, therapist_no_show):
    #Checking that overall no show rate within therapists and adding together no show rate for each day generates same overall percentage. 

    therapist_no_shows_sum = therapist_no_show["overall_no_shows"].sum()
    therapist_completed_and_no_shows_sum = therapist_no_show["overall_completed_and_no_shows"].sum()
    therapist_overall_rate = round(100 * therapist_no_shows_sum / therapist_completed_and_no_shows_sum, 2)

    day_no_shows_sum = day_of_week_no_show["no_shows"].sum()
    day_completed_and_no_shows_sum = day_of_week_no_show["completed_and_no_shows"].sum()
    day_overall_rate = round(100 * day_no_shows_sum / day_completed_and_no_shows_sum, 2)

    therapist_overall_rate, day_overall_rate, therapist_overall_rate == day_overall_rate
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 3. Patients whose last completed appointment was more than 90 days ago, with nothing booked, with a phone number
    """)
    return


@app.cell
def _(as_of, ask):
    #Assumption: I included patients on this list who have never booked an appointment

    patients_90_days = ask(f"""
    --Finds the most recently completed appointment for each patient and adds them to a table
    WITH last_completed AS (
        SELECT
            patient_id,
            MAX(start_date) AS last_completed_date
        FROM appointments
        WHERE status = 'completed'
        GROUP BY patient_id
    ),
    --Disregard any patients who have booked appointments 
    has_booked AS (
        SELECT DISTINCT patient_id
        FROM appointments
        WHERE status = 'booked'
    )
    SELECT
        p.patient_id,
        p.first_name,
        p.last_name,
        p.phone,
        lc.last_completed_date
    FROM patients p
    LEFT JOIN last_completed lc ON p.patient_id = lc.patient_id
    LEFT JOIN has_booked hb ON p.patient_id = hb.patient_id
    WHERE (lc.last_completed_date < DATE '{as_of}' - INTERVAL 90 DAY
           OR lc.last_completed_date IS NULL)
      AND hb.patient_id IS NULL
      AND p.phone <> ''
    ORDER BY lc.last_completed_date
    """)

    patients_90_days

    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 4. Revenue, cost and margin for each treatment, including treatments never given
    """)
    return


@app.cell
def _(ask):
    treatment_stats = ask("""
    WITH completed_treatments AS (
        SELECT att.treatment_id, att.price_charged
        FROM appointment_treatments att
        JOIN appointments a ON att.appt_id = a.appt_id
        WHERE a.status = 'completed'
    )
    SELECT
        t.treatment_id,
        t.treatment_name,
        t.price AS list_price,
        t.int_cost,
        COUNT(ct.treatment_id) AS times_given,
        COALESCE(SUM(ct.price_charged), 0) AS total_revenue,
        COUNT(ct.treatment_id) * t.int_cost AS total_cost,
        COALESCE(SUM(ct.price_charged), 0) - COUNT(ct.treatment_id) * t.int_cost AS total_margin,
        ROUND(
            (COALESCE(SUM(ct.price_charged), 0) - COUNT(ct.treatment_id) * t.int_cost)
            / NULLIF(COUNT(ct.treatment_id), 0),
            2
        ) AS margin_per_treatment
    FROM treatments t
    LEFT JOIN completed_treatments ct ON t.treatment_id = ct.treatment_id
    GROUP BY t.treatment_id, t.treatment_name, t.price, t.int_cost
    ORDER BY total_margin DESC
    """)

    treatment_stats
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 5. Patients who were referred and have no appointment at all
    """)
    return


@app.cell
def _(ask):
    patients_referred_no_appt = ask("""
        SELECT DISTINCT p.patient_id, p.first_name, p.last_name
        FROM patients p
        JOIN referrals r ON p.patient_id = r.patient_id
        LEFT JOIN appointments a ON p.patient_id = a.patient_id
        WHERE a.patient_id IS NULL
    """)

    patients_referred_no_appt
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 6. One row per patient with their number of referrals and their number of appointments, each checked against counting it on its own
    """)
    return


@app.cell
def _(ask):
    #count number of rows in table before any "Group By", per prediction question 

    patients_ungrouped = ask("""
    SELECT
        p.patient_id,
        r.referral_id,
        a.appt_id
    FROM patients p
    LEFT JOIN referrals r ON p.patient_id = r.patient_id
    LEFT JOIN appointments a ON p.patient_id = a.patient_id
    ORDER BY p.patient_id
    """)

    patients_ungrouped

    return


@app.cell
def _(ask):
    #Count number of rows created by "UNION ALL"

    all_patient_count = ask("""
    SELECT patient_id, NULL AS referral_id, NULL AS appt_id, 'patient' AS source
    FROM patients

    UNION ALL

    SELECT patient_id, referral_id, NULL AS appt_id, 'referral' AS source
    FROM referrals

    UNION ALL

    SELECT patient_id, NULL AS referral_id, appt_id, 'appointment' AS source
    FROM appointments
    """)

    all_patient_count
    return


@app.cell
def _(ask):
    #Using the same query to combine all three tables

    patient_referrals_appts = ask("""
    SELECT
        p.patient_id,
        COUNT(DISTINCT r.referral_id) AS num_referrals,
        (SELECT COUNT(*) FROM referrals r2 WHERE r2.patient_id = p.patient_id) AS num_referrals_check,
        COUNT(DISTINCT a.appt_id) AS num_appointments,
        (SELECT COUNT(*) FROM appointments a2 WHERE a2.patient_id = p.patient_id) AS num_appointments_check
    FROM patients p
    LEFT JOIN referrals r ON p.patient_id = r.patient_id
    LEFT JOIN appointments a ON p.patient_id = a.patient_id
    GROUP BY p.patient_id
    ORDER BY p.patient_id
    """)
    patient_referrals_appts 

    return (patient_referrals_appts,)


@app.cell
def _(ask):
    # Count referrals and appointments for each patient separately, then add together 
    patient_referrals_appts_sep_count = ask("""WITH ref_counts AS (
        SELECT patient_id, COUNT(*) AS num_referrals
        FROM referrals
        GROUP BY patient_id
    ),
    appt_counts AS (
        SELECT patient_id, COUNT(*) AS num_appointments
        FROM appointments
        GROUP BY patient_id
    )
    SELECT
        p.patient_id,
        p.first_name,
        p.last_name,
        COALESCE(rc.num_referrals, 0) AS num_referrals,
        COALESCE(ac.num_appointments, 0) AS num_appointments
    FROM patients p
    LEFT JOIN ref_counts rc ON p.patient_id = rc.patient_id
    LEFT JOIN appt_counts ac ON p.patient_id = ac.patient_id
    ORDER BY p.patient_id""")

    patient_referrals_appts_sep_count
    return (patient_referrals_appts_sep_count,)


@app.cell
def _(patient_referrals_appts, patient_referrals_appts_sep_count):
    #Check to confirm that total number of referrals and appts calculated with both methods are the same, confirming that join strategy did not cause them to be lost or double counted. These also match the given numbers of appointments and referrals in the data. 
    joined_total_referrals = patient_referrals_appts["num_referrals"].sum()
    joined_total_appointments = patient_referrals_appts["num_appointments"].sum()

    separate_total_referrals = patient_referrals_appts_sep_count["num_referrals"].sum()
    separate_total_appointments = patient_referrals_appts_sep_count["num_appointments"].sum()

    joined_total_referrals, separate_total_referrals, joined_total_appointments, separate_total_appointments, joined_total_referrals == separate_total_referrals, joined_total_appointments == separate_total_appointments
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 7. Every completed appointment checked against the rule that the treatments given at it take no more minutes than its length, and a list of any that break it
    """)
    return


@app.cell
def _(ask):
    completed_treatments_rule_break = ask("""
    WITH treatment_minutes AS (
        SELECT appt_id, SUM(minutes_spent) AS total_minutes
        FROM appointment_treatments
        GROUP BY appt_id
    )
    SELECT
        a.appt_id,
        a.patient_id,
        a.therapist_id,
        a.length AS appt_length,
        tm.total_minutes,
        tm.total_minutes - a.length AS minutes_over
    FROM appointments a
    JOIN treatment_minutes tm ON a.appt_id = tm.appt_id
    WHERE a.status = 'completed'
      AND tm.total_minutes > a.length
    ORDER BY minutes_over DESC
    """)

    completed_treatments_rule_break
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The appt_ids that break the rules match with those that were identified from the terminal code when the data was first generated: "rows that break the minutes-vs-length rule on purpose: appt_id 2285, appt_id 2894"
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 8. Which therapist earns the most revenue per hour of scheduled appointment time?
    """)
    return


@app.cell
def _(ask):
    therapist_revenue_per_hour = ask("""
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
        SUM(a.length) AS total_minutes,
        ROUND(SUM(a.length) / 60.0, 2) AS total_hours,
        COALESCE(SUM(ar.revenue), 0) AS total_revenue,
        ROUND(
            COALESCE(SUM(ar.revenue), 0) / (SUM(a.length) / 60.0),
            2
        ) AS revenue_per_hour
    FROM appointments a
    JOIN therapists t ON a.therapist_id = t.therapist_id
    LEFT JOIN appt_revenue ar ON a.appt_id = ar.appt_id
    WHERE a.status = 'completed'
    GROUP BY t.therapist_id, t.first_name, t.last_name
    ORDER BY revenue_per_hour DESC
    """)

    therapist_revenue_per_hour
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

    The total number of rows before grouping will be about 3,450. I'm predicting this because there will be 150 rows from the referrals table, 3000 rows from the appointments table, and 300 rows from the patients table since that is how many rows those tables have currently. The patient id number for each will be included in the initial join, then those will be reduced to 300 rows to reflect one row per patients.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Results from question 6: there were 3,329 rows generated by left joining the three tables, which was close to my estimate, but I had the incorrect reasoning. I originally assumed that when tables were joined together, there would be a list with all of the original rows from each of the tables, with "Null" for the values in the other tables (ex. for referral ID, null for appointment ID, regardless of whether they had any patients). That number of rows was actually correct for the "UNION ALL" function, which I also ran for the table, for the reasoning I had given originally.

    In actuality, when using the left join function, the number of rows comes from the number of potential combinations of referral IDs and appointment IDs. Instead of being additive, they would multiply per patient ID. For example, if a patient had two appointments and two referral IDs, the left joins would create four total rows (2x2) to show all of those combinations. Without counting in the data, there wouldn't have been a way to determine the exact number of rows since patients with multiple referrals and appointments would create more combinations of rows than if the appointments and referrals were more widely distributed among patient IDs. Theoretically, if there was max of one referral per patient, the total number of rows would be close to 3000 since each row would just include the patient, appointment ID, and referral ID if applicable. There are also some patients without appointments, so those would bring the count to slightly over 3,000 rows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One row of the final result will represent one patient and how many appointments and referals they have, including if they have none of each.
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
