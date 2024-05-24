from Person import Person
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_url = "mysql://root:24012004Bb*@localhost/proje1"

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)
session = Session()

class KPatient(Person):
    TYPE = "P"

    def __init__(self, name, surname, tckn, date_of_birth, gender, tel_no, address, for_database=False):
        super().__init__(name, surname, tckn, date_of_birth)
        self._gender = gender
        self._tel_no = tel_no
        self._address = address
        self._patient_id = self.calculate_id()
        if for_database:
            self.save_to_database()

    def calculate_id(self):
        return self.TYPE + self.tckn

    def save_to_database(self, session):
        # Mevcut Patient nesnesini veritabanına ekleyin
        session.add(self)

        # Değişiklikleri kaydet
        session.commit()

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        self._gender = value

    @property
    def tel_no(self):
        return self._tel_no

    @tel_no.setter
    def tel_no(self, value):
        self._tel_no = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def patient_id(self):
        return self._patient_id

    @patient_id.setter
    def patient_id(self, value):
        self._patient_id = value
