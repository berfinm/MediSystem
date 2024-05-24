from Person import Person
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "mysql://root:24012004Bb*@localhost/proje1"


engine = create_engine(db_url)


Session = sessionmaker(bind=engine)
session = Session()

class KDoctor(Person):
    TYPE = "D"

    def __init__(self, name, surname, tckn, date_of_birth, profession, working_hospital, for_database=False):
        super().__init__(name, surname, tckn, date_of_birth)
        self._profession = profession
        self._working_hospital = working_hospital
        self._doctor_id = self.calculate_id()
        if for_database:
            self.save_to_database(session)

    def calculate_id(self):
        return self.TYPE + self.tckn

    def save_to_database(self, session):
        # Mevcut Doctor nesnesini veritabanına ekleyin
        session.add(self)

        # Değişiklikleri kaydet
        session.commit()

    @property
    def profession(self):
        return self._profession

    @profession.setter
    def profession(self, value):
        self._profession = value

    @property
    def working_hospital(self):
        return self._working_hospital

    @working_hospital.setter
    def working_hospital(self, value):
        self._working_hospital = value

    @property
    def doctor_id(self):
        return self._doctor_id

    @doctor_id.setter
    def doctor_id(self, value):
        self._doctor_id = value
