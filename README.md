# MyT_assignment
MyTomorrows take home assignment

The purpose of this assessment is to redesign a given data model which tracks the flow of medical procedures.

The Initial E/R Diagram of the system was this one:

![Old Data Model](.images/old_diagram.png)

# 1.1 Proposed New Data Model

## Main Entities:

Person: Base table to store common attributes of Contact and Patient.
    Fields: person_id (UUID), firstname, lastname, email.

Contact: Inherits from Person and adds specific fields for leads/doctors.
    Fields: contact_id (UUID), contact_type (option_set), job_title, hospital_id (FK to Hospital), medical_license_number.

Patient: Inherits from Person and links to the Contact that converted it.
    Fields: patient_id (UUID), contact_record_id (FK to Contact), physician_id (FK to Contact), initial_consult_date, eap_enrollment_date, etc.

MedicalCondition: Single table for medical conditions (eliminates redundancy).
    Fields: condition_id (UUID), name, abbreviation.

Referral: Table to manage EAP/CT referrals (supports multiple).
    Fields: referral_id (UUID), patient_id (FK), type (EAP/CT), referral_date, outcome.

Appointment: Records all appointments (prevents data loss).
    Fields: appointment_id (UUID), patient_id (FK), booking_date, reminder_date, notes.

## Relationships:

Patient.contact_record_id → Contact.contact_id (a patient originates from a contact).

Contact.contact_type uses an option_set (patient-lead, physician, pharmacist).

Patient.medical_condition_id → MedicalCondition.condition_id (single lookup).

## Advantages:

Eliminates redundancy of medical_condition by using a single table.

Separates roles (Contact/Patient) using inheritance and avoids confusing fields.

Supports multiple referrals (EAP/CT) and appointments without data loss.

# 1.2 Migration to the New Model

## 1.2.1 Existing Data Analysis:

Map redundant fields (e.g., Contact.medical_condition → MedicalCondition).

Identify orphaned or inconsistent records.

## 1.2.3 Migration Scripts:

Create new tables (Person, MedicalCondition, Referral, etc.).

## 1.2.4 Migrate data:

Insert MedicalCondition from option_set medical condition.

Split Contact and Patient into Person + inherited tables.

Update foreign keys (e.g., Patient.physician → Contact.contact_id).

## 1.2.5: Real-Time Synchronization:

Use triggers or application logic to keep Person updated when Contact or Patient changes.

## 1.2.6 Validation:

Verify relationship integrity and migrated data.

Regression testing for critical flows (e.g., Contact → Patient conversion).

# 2 API creation

Made an API with CRUD operations for the patient model.

