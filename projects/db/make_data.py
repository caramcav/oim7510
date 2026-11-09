"""Write one CSV file per table for the Babson PT Clinic database.

Run with: uv run python projects/db/make_data.py
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

from faker import Faker

SEED = 42
random.seed(SEED)
fake = Faker()
Faker.seed(SEED)

AS_OF = date(2026, 12, 31)
HISTORY_START = AS_OF - timedelta(days=365)
FUTURE_END = AS_OF + timedelta(days=21)

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

N_THERAPISTS = 6
N_PATIENTS = 300
N_REFERRALS = 150
N_APPOINTMENTS = 3000

CREDENTIALS = ["DPT", "PTA"]
LENGTHS = [30, 45, 60]
REFERRAL_REASONS = [
    "post-surgical rehab",
    "chronic back pain",
    "sports injury",
    "balance and fall risk",
    "post-stroke recovery",
    "work injury",
]

# name, standard minutes, price, internal cost
TREATMENT_ROWS = [
    ("Manual Therapy", 30, 65.00, 20.00),
    ("Therapeutic Exercise", 30, 55.00, 15.00),
    ("Ultrasound Therapy", 15, 40.00, 8.00),
    ("Electrical Stimulation", 15, 35.00, 7.00),
    ("Gait Training", 30, 60.00, 18.00),
    ("Joint Mobilization", 30, 70.00, 22.00),
    ("Post-Surgical Rehab", 45, 90.00, 30.00),
    ("Balance Training", 30, 50.00, 14.00),
]

# 20 patients who never get a referral or an appointment, for business question 3 / going further
WALK_IN_NO_HISTORY_IDS = []
for patient_id in range(281, 301):
    WALK_IN_NO_HISTORY_IDS.append(patient_id)

# half-hour appointment slots from 8:00 AM to 4:30 PM
SLOT_MINUTES = []
minutes = 8 * 60
while minutes <= 16 * 60 + 30:
    SLOT_MINUTES.append(minutes)
    minutes = minutes + 30


def minutes_to_time_string(minutes_since_midnight):
    hour = minutes_since_midnight // 60
    minute = minutes_since_midnight % 60
    return f"{hour:02d}:{minute:02d}:00"


def write_csv(filename, fieldnames, rows):
    path = DATA_DIR / filename
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"wrote {len(rows)} rows to data/{filename}")


def make_therapists():
    rows = []
    for therapist_id in range(1, N_THERAPISTS + 1):
        hire_date = fake.date_between(start_date=date(2015, 1, 1), end_date=HISTORY_START)
        rows.append(
            {
                "therapist_id": therapist_id,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "cred": random.choice(CREDENTIALS),
                "email": fake.unique.email(),
                "hire_date": hire_date.isoformat(),
            }
        )
    return rows


def make_treatments():
    rows = []
    treatment_id = 1
    for name, std_min, price, int_cost in TREATMENT_ROWS:
        rows.append(
            {
                "treatment_id": treatment_id,
                "treatment_name": name,
                "std_min": std_min,
                "price": price,
                "int_cost": int_cost,
            }
        )
        treatment_id = treatment_id + 1
    return rows


def make_patients():
    rows = []
    for patient_id in range(1, N_PATIENTS + 1):
        dob = fake.date_of_birth(minimum_age=8, maximum_age=90)
        self_pay = random.random() < 0.2
        if self_pay:
            insurance_member_number = ""
        else:
            insurance_member_number = f"INS{100000 + patient_id}"
        rows.append(
            {
                "patient_id": patient_id,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "DOB": dob.isoformat(),
                "phone": fake.phone_number(),
                "email": fake.unique.email(),
                "insurance_member_number": insurance_member_number,
            }
        )
    return rows


def make_referrals():
    # active patients can be referred; walk-ins never are
    active_patient_ids = []
    for patient_id in range(1, N_PATIENTS + 1):
        if patient_id not in WALK_IN_NO_HISTORY_IDS:
            active_patient_ids.append(patient_id)

    # 15 patients get a referral but will never get an appointment (business question 5)
    referred_no_appt_ids = random.sample(active_patient_ids, 15)

    rows = []
    referral_id = 1
    for patient_id in referred_no_appt_ids:
        ref_date = fake.date_between(start_date=HISTORY_START, end_date=AS_OF)
        rows.append(
            {
                "referral_id": referral_id,
                "patient_id": patient_id,
                "physician_name": "Dr. " + fake.last_name(),
                "ref_date": ref_date.isoformat(),
                "reason": random.choice(REFERRAL_REASONS),
            }
        )
        referral_id = referral_id + 1

    while referral_id <= N_REFERRALS:
        patient_id = random.choice(active_patient_ids)
        ref_date = fake.date_between(start_date=HISTORY_START, end_date=AS_OF)
        rows.append(
            {
                "referral_id": referral_id,
                "patient_id": patient_id,
                "physician_name": "Dr. " + fake.last_name(),
                "ref_date": ref_date.isoformat(),
                "reason": random.choice(REFERRAL_REASONS),
            }
        )
        referral_id = referral_id + 1

    return rows, referred_no_appt_ids


def make_appointments(referred_no_appt_ids):
    # patients eligible for appointments: everyone except walk-ins and referral-only patients
    appointment_patient_ids = []
    for patient_id in range(1, N_PATIENTS + 1):
        if patient_id in WALK_IN_NO_HISTORY_IDS:
            continue
        if patient_id in referred_no_appt_ids:
            continue
        appointment_patient_ids.append(patient_id)

    taken_slots = set()  # (therapist_id, start_date, start_time) already booked
    rows = []
    appt_id = 1
    total_days = (FUTURE_END - HISTORY_START).days

    while appt_id <= N_APPOINTMENTS:
        therapist_id = random.randint(1, N_THERAPISTS)
        offset_days = random.randint(0, total_days)
        start_date = HISTORY_START + timedelta(days=offset_days)
        start_time = minutes_to_time_string(random.choice(SLOT_MINUTES))

        slot_key = (therapist_id, start_date, start_time)
        if slot_key in taken_slots:
            continue
        taken_slots.add(slot_key)

        if start_date > AS_OF:
            status = "booked"
        elif random.random() < 0.15:
            status = "no-show"
        else:
            status = "completed"

        rows.append(
            {
                "appt_id": appt_id,
                "patient_id": random.choice(appointment_patient_ids),
                "therapist_id": therapist_id,
                "start_date": start_date.isoformat(),
                "start_time": start_time,
                "length": random.choice(LENGTHS),
                "status": status,
            }
        )
        appt_id = appt_id + 1

    return rows


def make_appointment_treatments(appointments, treatments):
    rows = []
    completed_appt_ids_in_order = []

    for appt in appointments:
        if appt["status"] != "completed":
            continue
        completed_appt_ids_in_order.append(appt["appt_id"])

        how_many = random.choice([1, 2, 3])
        candidates = treatments.copy()
        random.shuffle(candidates)

        remaining_minutes = appt["length"]
        added = 0
        for treatment in candidates:
            if added >= how_many:
                break
            if treatment["std_min"] <= remaining_minutes:
                rows.append(
                    {
                        "appt_id": appt["appt_id"],
                        "treatment_id": treatment["treatment_id"],
                        "price_charged": treatment["price"],
                        "minutes_spent": treatment["std_min"],
                    }
                )
                remaining_minutes = remaining_minutes - treatment["std_min"]
                added = added + 1

    # break the "minutes spent <= appointment length" rule on purpose, in exactly two rows
    broken_appt_ids = random.sample(completed_appt_ids_in_order, 2)
    appt_lookup = {}
    for appt in appointments:
        appt_lookup[appt["appt_id"]] = appt

    used_treatment_ids = {}
    for row in rows:
        used_treatment_ids.setdefault(row["appt_id"], set()).add(row["treatment_id"])

    for appt_id in broken_appt_ids:
        appt = appt_lookup[appt_id]
        already_used = used_treatment_ids.get(appt_id, set())
        for treatment in treatments:
            if treatment["treatment_id"] not in already_used:
                rows.append(
                    {
                        "appt_id": appt_id,
                        "treatment_id": treatment["treatment_id"],
                        "price_charged": treatment["price"],
                        "minutes_spent": appt["length"] + treatment["std_min"],
                    }
                )
                break

    print(f"rows that break the minutes-vs-length rule on purpose: appt_id {broken_appt_ids[0]}, appt_id {broken_appt_ids[1]}")
    return rows


def main():
    therapists = make_therapists()
    treatments = make_treatments()
    patients = make_patients()
    referrals, referred_no_appt_ids = make_referrals()
    appointments = make_appointments(referred_no_appt_ids)
    appointment_treatments = make_appointment_treatments(appointments, treatments)

    write_csv("therapists.csv", ["therapist_id", "first_name", "last_name", "cred", "email", "hire_date"], therapists)
    write_csv("treatments.csv", ["treatment_id", "treatment_name", "std_min", "price", "int_cost"], treatments)
    write_csv("patients.csv", ["patient_id", "first_name", "last_name", "DOB", "phone", "email", "insurance_member_number"], patients)
    write_csv("referrals.csv", ["referral_id", "patient_id", "physician_name", "ref_date", "reason"], referrals)
    write_csv("appointments.csv", ["appt_id", "patient_id", "therapist_id", "start_date", "start_time", "length", "status"], appointments)
    write_csv("appointment_treatments.csv", ["appt_id", "treatment_id", "price_charged", "minutes_spent"], appointment_treatments)

    print(f"{len(WALK_IN_NO_HISTORY_IDS)} patients have no referral and no appointment")
    print(f"{len(referred_no_appt_ids)} patients have a referral but no appointment")


if __name__ == "__main__":
    main()
