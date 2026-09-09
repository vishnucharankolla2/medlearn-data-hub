import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()
np.random.seed(42)
random.seed(42)

def generate_patients():
    data = []
    for i in range(1, 101):
        patient_id = i if random.random() > 0.05 else None
        gender_choices = ['M', 'F', 'Male', 'Female', '1', '2', 'X', 'UNKNOWN']
        gender = random.choice(gender_choices)
        
        if random.random() < 0.05:
            birthdate = fake.date_between(start_date="today", end_date="+2y")
        else:
            birthdate = fake.date_between(start_date="-80y", end_date="-18y")
        
        data.append({
            "patient_id": patient_id,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "gender": gender,
            "birth_date": birthdate,
            "zip_code": fake.zipcode() if random.random() > 0.1 else None,
            "phone": fake.phone_number()
        })
    return pd.DataFrame(data)

def generate_visits():
    data = []
    patient_ids = list(range(1, 101))
    hospital_names = ['St. Marys Hospital', 'St. Mary\'s Hospital', 'General Hospital', 'Gen. Hosp.', 'Mayo Clinic', 'MAYO CLINIC']
    
    for _ in range(200):
        p_id = random.choice(patient_ids) if random.random() > 0.08 else None
        hospital = random.choice(hospital_names)
        admit = fake.date_time_between(start_date="-2y", end_date="now")
        if random.random() < 0.07:
            discharge = admit - timedelta(days=random.randint(1, 10))
        else:
            discharge = admit + timedelta(days=random.randint(1, 15))
            
        data.append({
            "visit_id": fake.uuid4(),
            "patient_id": p_id,
            "hospital": hospital,
            "admission_date": admit.strftime("%Y-%m-%d %H:%M:%S"),
            "discharge_date": discharge.strftime("%Y-%m-%d %H:%M:%S"),
            "department": random.choice(['ER', 'Cardio', 'Neuro', 'Ortho', ''])
        })
    return pd.DataFrame(data)

def generate_labs():
    data = []
    patient_ids = list(range(1, 101))
    lab_tests = ['Hemoglobin', 'Glucose', 'Cholesterol', 'Potassium']
    
    for _ in range(500):
        p_id = random.choice(patient_ids)
        test = random.choice(lab_tests)
        if random.random() < 0.03:
            value = random.randint(1000, 9999)
        else:
            value = round(random.uniform(4.0, 150.0), 2)
        unit = random.choice(['mg/dL', 'mmol/L', 'g/L', ''])
        
        data.append({
            "lab_id": fake.uuid4(),
            "patient_id": p_id,
            "test_name": test,
            "value": value,
            "unit": unit,
            "lab_date": fake.date_between(start_date="-1y", end_date="today")
        })
    return pd.DataFrame(data)

if __name__ == "__main__":
    patients_df = generate_patients()
    visits_df = generate_visits()
    labs_df = generate_labs()
    
    patients_df.to_csv("data/patients_raw.csv", index=False)
    visits_df.to_csv("data/visits_raw.csv", index=False)
    labs_df.to_csv("data/labs_raw.csv", index=False)
    
    print("✅ Dirty data generated successfully!")
    print(f"Patients: {len(patients_df)} records (Check for null IDs!)")
    print(f"Visits: {len(visits_df)} records (Check for orphan patients!)")
    print(f"Labs: {len(labs_df)} records (Check for outliers!)")
