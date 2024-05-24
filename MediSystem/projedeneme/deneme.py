from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

db_url = "mysql://root:24012004Bb*@localhost/proje4"


engine = create_engine(db_url)


Base = declarative_base()


Session = sessionmaker(bind=engine)
session = Session()

class Hospital(Base):
    __tablename__ = 'hospitals'
    hospital_id = Column(Integer, primary_key=True)
    hospital_name = Column(String(100))
    hospital_address = Column(String(255))

    doctors = relationship("Doctor", back_populates="hospital")
    managers = relationship("Manager", back_populates="hospital")
    patients = relationship("Patient", back_populates="hospital")
class Patient(Base):
    __tablename__ = 'patients'
    patient_id = Column(Integer, primary_key=True, autoincrement=True)
    hospital_id = Column(Integer, ForeignKey('hospitals.hospital_id'))
    name = Column(String(50))
    surname = Column(String(50))
    tckn = Column(String(12))
    date_of_birth = Column(String(50))
    gender = Column(String(10))
    tel_no = Column(String(50))
    address = Column(String(100))
    TYPE = "P"

    hospital = relationship("Hospital", back_populates="patients")



class Doctor(Base):
    __tablename__ = 'doctors'
    doctor_id = Column(Integer, primary_key=True, autoincrement=True)
    hospital_id = Column(Integer, ForeignKey('hospitals.hospital_id'))
    name = Column(String(50))
    surname = Column(String(50))
    tckn = Column(String(12))
    date_of_birth = Column(String(50))
    profession = Column(String(50))

    hospital = relationship("Hospital", back_populates="doctors")
    TYPE = "D"

class Manager(Base):
    __tablename__ = 'managers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hospital_id = Column(Integer, ForeignKey('hospitals.hospital_id'))
    name = Column(String(50))
    surname = Column(String(50))
    tckn = Column(String(12))
    date_of_birth = Column(String(50))

    hospital = relationship("Hospital", back_populates="managers")


class Appointment(Base):
    __tablename__ = 'appointments'
    appointment_id = Column(Integer, primary_key=True)
    appointment_date = Column(String(50))
    appointment_time = Column(String(50))
    #hospital = relationship("Hospital", back_populates="appointments")
    #doctors = relationship("Doctor", back_populates="appointments")
    #patients = relationship("Patient", back_populates="appointments")

Base.metadata.create_all(engine)
