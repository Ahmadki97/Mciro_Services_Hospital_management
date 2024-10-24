from sqlalchemy import String, Integer, Boolean, DateTime, Column, ForeignKey, Time
from sqlalchemy.orm import relationship
from database import Base
import datetime


class Patient(Base):
    __tablename__ = 'Patients'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    username = Column(String(255), unique=True, nullable=False, index=True)
    profile_pic = Column(String(255))
    address = Column(String(255))
    status = Column(Boolean, default=False)
    symptoms = Column(String(500))
    birth = Column(DateTime)
    admit_date = Column(DateTime, onupdate=datetime.datetime.now())
    doctor_id = Column(Integer, ForeignKey("Doctors.id"), nullable=True)
    doctor = relationship("Doctor", back_populates='patients')
    appointments = relationship("Appointment", back_populates="patient")


    def to_dict(self):
        patient = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'profile_pic': self.profile_pic,
            'address': self.address,
            'status': self.status,
           'symptoms': self.symptoms,
            'birth': self.birth,
            'admit_date': self.admit_date,
            'doctor_id': self.doctor_id,
        }
        return patient


class Doctor(Base):
    __tablename__ = 'Doctors'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    username = Column(String(255), unique=True, nullable=False, index=True)
    profile_pic = Column(String(255))
    address = Column(String(255))
    status = Column(Boolean, default=False)
    department = Column(String(255))
    mobile = Column(String(15))
    work_hours = Column(Integer)
    work_starts = Column(Time)
    work_days = Column(String(255))
    patients = relationship(Patient, back_populates='doctor')
    appointments = relationship("Appointment", back_populates="doctor")


    def to_dict(self):
        doctor = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'profile_pic': self.profile_pic,
            'address': self.address,
            'department': self.department,
            'mobile': self.mobile,
            'patients': [patient.to_dict() for patient in self.patients],
            'appointments': [appointment.to_dict() for appointment in self.appointments],
            'work_hours': self.work_hours,
            'work_starts': self.work_starts,
            'work_days': self.work_days,
            'status': self.status,
        }
        return doctor


class Appointment(Base):
    __tablename__ = 'Appointments'
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('Patients.id'), nullable=False)
    doctor_id = Column(Integer, ForeignKey('Doctors.id'), nullable=False)
    time = Column(DateTime, nullable=False)
    description = Column(String, nullable=True)
    patient_report = Column(String)
    status = Column(Boolean, default=False)
    passed = Column(Boolean, default=False)
    patient = relationship(Patient, back_populates='appointments')
    doctor = relationship(Doctor, back_populates='appointments')


    def to_dict(self):
        appointemnt = {
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'time': self.time,
            'description': self.description,
            'patient_report': self.patient_report,
            'status': self.status,
            'passed': self.passed,
            'doctor': self.doctor.to_dict(),
            'patient': self.patient.to_dict(),
        }
        return appointemnt


    