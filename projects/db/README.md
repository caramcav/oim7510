1. The Scenario: Scenario D, Babson PT Clinic 

2. The ERD: 

```mermaid
erDiagram
    THERAPISTS ||--o{ APPOINTMENTS : conducts
    PATIENTS ||--o{ APPOINTMENTS : books
    PATIENTS ||--o{ REFERRALS : has
    APPOINTMENTS ||--|{ APPOINTMENT_TREATMENTS : includes
    TREATMENTS ||--o{ APPOINTMENT_TREATMENTS : used_in

    TREATMENTS {
        int treatment_id PK
        str treatment_name
        int std_min
        float price
        float int_cost
    }

    THERAPISTS {
        int therapist_id PK
        str first_name
        str last_name
        str cred
        str email
        date hire_date
    }

    PATIENTS {
        int patient_id PK
        str first_name
        str last_name
        date DOB
        str phone_num
        str email
        int insurance_id
    }

    APPOINTMENTS {
        int appt_id PK
        int patient_id FK
        int therapist_id FK
        date start_date
        time start_time
        int length
        str status
        float total_price
    }

    APPOINTMENT_TREATMENTS {
        int appt_id FK
        int treatment_id FK
        float price_charged
        int minutes_spent
    }

    REFERRALS {
        int referral_id PK
        int patient_id FK
        str physician_name
        date ref_date
        str reason
    }
```

3. What one row means: 
- One row in "Therapists" is for one therapist that works at the clinic and their associated information
- One row in "Patients" is for one patient that has created an account at the clinic, who may or may not have have had an appointment before
- One row in "Referrals" is for one referral from one physician for one patient. 
- One row in "Appointments" is for one appointment scheduled on a given date with one therapist and one patient. 
- One row in "Appointment Treatments" shows one treatment given within the clinic and which appointment it is associated with. 
- One row in "Treatments" is for one type of treatment offered at the clinic 


4. Design Choices. 
- Which key I chose where the business already had one: I decided to have IDs for the therapists and patients in case multiple individuals shared the same names, their names changed, or their emails changed. I also decided to have IDs for appointments since it'd require a combination of at least 3 primary keys (ex. therapist name, appointment date, appointment time) to differentiate between them. I decided to have referal ids since it'd also take multiple primary keys to differentiate. 
- Which relationships are optional: The relationship between patients and referals are optional since patients do not need a referral- they could walk in instead. The relationships between therapists/patients and appointments are also optional, since they do not neccesarily need to have an appointment scheduled in order to be added to the system. 
- Which of the scenarios rule my table cannot hold: my table can check that two appointments with the same therapist don't have the same start time, but it cannot check whether two appointments with different start times overlap. I will use a query instead to check at the time of booking that the proposed time and duration won't overlap with an existing appointment.
- One thing your agent proposed for the design that you changed or did not take, and why. If you designed it alone, one thing you checked in the ERD your agent drew: I did the majority of the design myself on paper prior to having the agent create it. I confirmed the relationships between the tables were correct after it was created, and found one thing to update. The AI agent had included a zero or more relationship between appointment_treatments and treatments. I updated the relationship to one or more since each appointment requires at least one treatment, otherwise the total price would be $0(which would break the price > $0 rule). 
