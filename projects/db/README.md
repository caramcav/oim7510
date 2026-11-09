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
- One row in "Treatments" is for one type of treatment and the associated information for that type of treatment. 


4. Design Choices. 

