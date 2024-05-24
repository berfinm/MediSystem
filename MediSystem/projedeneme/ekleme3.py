from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from deneme import Hospital, Manager
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


hospitals = session.query(Hospital).all()


for _ in range(num_managers):

    random_hospital = random.choice(hospitals)
    manager = Manager(
        name=fake.first_name(),
        surname=fake.last_name(),
        tckn=fake.unique.ssn(),
        date_of_birth=fake.date_of_birth(minimum_age=30, maximum_age=70).strftime('%Y-%m-%d'),
        hospital=random_hospital
    )
    session.add(manager)

session.commit()  
session.close()

print("Veri ekleme işlemi tamamlandı.")
