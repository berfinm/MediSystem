from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from deneme import Hospital, Doctor, Manager, Patient
from faker import Faker
import random


db_url = "mysql://root:24012004Bb*@localhost/proje4"
engine = create_engine(db_url)


Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()


num_hospitals = 5
num_doctors = 10
num_managers = 5
num_patients = 20


for _ in range(num_hospitals):
    hospital = Hospital(
        hospital_name=fake.company(),
        hospital_address=fake.address()
    )
    session.add(hospital)

session.commit()


hospitals = session.query(Hospital).all()


for _ in range(num_doctors):
    doctor = Doctor(
        name=fake.first_name(),
        surname=fake.last_name(),
        tckn=fake.unique.ssn(),
        date_of_birth=fake.date_of_birth(minimum_age=25, maximum_age=70).strftime('%Y-%m-%d'),
        profession=fake.job(),
        hospital=random.choice(hospitals)
    )
    session.add(doctor)

for _ in range(num_managers):
    manager = Manager(
        name=fake.first_name(),
        surname=fake.last_name(),
        tckn=fake.unique.ssn(),
        date_of_birth=fake.date_of_birth(minimum_age=30, maximum_age=70).strftime('%Y-%m-%d'),
        hospital=random.choice(hospitals)
    )
    session.add(manager)


for _ in range(num_patients):
    patient = Patient(
        name=fake.first_name(),
        surname=fake.last_name(),
        tckn=fake.unique.ssn(),
        date_of_birth=fake.date_of_birth(minimum_age=1, maximum_age=100).strftime('%Y-%m-%d'),
        gender=fake.random_element(elements=('Male', 'Female')),
        tel_no=fake.phone_number(),
        address=fake.address(),
    )
    session.add(patient)

session.commit()
session.close()

print("Veri ekleme işlemi tamamlandı.")
