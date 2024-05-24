from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "mysql://root:24012004Bb*@localhost/proje1"

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()
class KHospital:
    def __init__(self, hospital_id, hospital_name, hospital_address, doctors=None, managers=None, patients=None, for_database=False):
        self._hospital_id = hospital_id
        self._hospital_name = hospital_name
        self._hospital_address = hospital_address
        self._doctors = doctors if doctors is not None else []
        self._managers = managers if managers is not None else []
        self._patients = patients if patients is not None else []

    def save_to_database(self, session):
        # Mevcut Hospital nesnesini veritabanına ekleyin
        session.add(self)

        # Değişiklikleri kaydet
        session.commit()

    @property
    def hospital_id(self):
        return self._hospital_id

    @hospital_id.setter
    def hospital_id(self, value):
        self._hospital_id = value

    @property
    def hospital_name(self):
        return self._hospital_name

    @hospital_name.setter
    def hospital_name(self, value):
        self._hospital_name = value

    @property
    def hospital_address(self):
        return self._hospital_address

    @hospital_address.setter
    def hospital_address(self, value):
        self._hospital_address = value

    @property
    def doctors(self):
        return self._doctors

    @doctors.setter
    def doctors(self, value):
        self._doctors = value

    @property
    def managers(self):
        return self._managers

    @managers.setter
    def managers(self, value):
        self._managers = value

    @property
    def patients(self):
        return self._patients

    @patients.setter
    def patients(self, value):
        self._patients = value

    def add_doctor(self, doctor):
        self._doctors.append(doctor)

    def remove_doctor(self, doctor):
        self._doctors.remove(doctor)

    def add_manager(self, manager):
        self._managers.append(manager)

    def remove_manager(self, manager):
        self._managers.remove(manager)

    def add_patient(self, patient):
        self._patients.append(patient)

    def remove_patient(self, patient):
        self._patients.remove(patient)
