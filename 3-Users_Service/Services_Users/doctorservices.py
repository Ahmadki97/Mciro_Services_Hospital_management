from Helper_Users.loghandler import logger
from Models_Users.models import Appointment, Doctor
from Models_Users.schemas import AppointmentSchema, DoctorSchema, PatientSchema
from fastapi import HTTPException , status
from sqlalchemy.orm import Session


def createDoctor(doctor: dict, db: Session):
    try:
        doctor_create = Doctor(**doctor)
        db.add(doctor_create)
        db.commit()
        logger.info(f"createDoctor() Method, Doctor {doctor_create.first_name} {doctor_create.last_name} created successfully..") 
    except Exception as err:
        logger.error(f"Error in createDoctor() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

async def getDoctorById(id: int, db: Session):
    try:
        doctor = db.query(Doctor).filter(Doctor.id == id).first()
        if doctor is None:
            logger.info(f"getDoctorById() Method, Doctor with id {id} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        return doctor
    except Exception as err:
        logger.error(f"Error in getDoctorById() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

async def getDoctorByUsername(username: str, db: Session):
    try:
        doctor = db.query(Doctor).filter(Doctor.username == username).first()
        if doctor is None:
            logger.info(f"getDoctorByUsername() Method, Doctor with username {username} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        return DoctorSchema.model_dump(doctor)
    except Exception as err:
        logger.error(f"Error in getDoctorByUsername() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

async def getDoctorsByDepartment(department: str, db: Session):
    try:
        doctors = db.query(Doctor).filter(Doctor.department == department).all()
        if len(doctors) == 0:
            logger.info(f"getDoctorsByDepartment() Method, No doctors found for department {department}.")
            return []
        else:
            logger.info(f"getDoctorsByDepartment() Method, {len(doctors)} doctors found for department {department}.")
            return [DoctorSchema.model_dump(doctor) for doctor in doctors]
    except Exception as err:
        logger.error(f"Error in getDoctorsByDepartment() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

async def getDoctorPatients(id: int, db: Session):
    try:
        doctor = db.query(Doctor).filter(Doctor.id == id).first()
        if doctor is None:
            logger.info(f"getDoctorPatients() Method, Doctor with id {id} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        patients = doctor.patients
        if len(patients) == 0:
            logger.info(f"getDoctorPatients() Method, No patients found for doctor with id {id}.")
            return []
        else:
            logger.info(f"getDoctorPatients() Method, {len(patients)} patients found for doctor with id {id}.")
            patients = [PatientSchema.model_dump(patients) for patient in patients]
            return patients
    except Exception as err:
        logger.error(f"Error in getDoctorPatients() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

async def getDoctorAppointments(id: int, db: Session):
    try:
        doctor = db.query(Doctor).filter(Doctor.id == id).first()
        if doctor is None:
            logger.info(f"getDoctorAppointments() Method, Doctor with id {id} not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
        appointments = doctor.appointments
        if len(appointments) == 0:
            logger.info(f"getDoctorAppointments() Method, No appointments found for doctor with id {id}.")
            return []
        else:
            logger.info(f"getDoctorAppointments() Method, {len(appointments)} appointments found for doctor with id {id}.")
            appointments = [AppointmentSchema.model_dump(appointment) for appointment in appointments]
            return appointments
    except Exception as err:
        logger.error(f"Error in getDoctorAppointments() Method: {err}.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    
    