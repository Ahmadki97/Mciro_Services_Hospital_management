from Helper_Users.loghandler import logger
from fastapi import status, HTTPException
from Models_Users.models import Patient
from Models_Users.schemas import PatientSchema, AppointmentSchema
from sqlalchemy.orm import Session




def createPatient(patient: dict, db: Session):
    try:
        patient = Patient(**patient)
        db.add(patient)
        db.commit()
        logger.info(f"createPatient() Method, Patient with id {patient.id} Created successfully.") 
        return PatientSchema.model_dump(patient)
    except Exception as err:
        logger.error(f"Error in createPatient() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

async def getPatientById(id: int, db: Session):
    try:
        patient = db.query(Patient).filter(Patient.id == id).filter()
        if patient is not None:
            logger.info(f"getPatientById() Method, patient with id {id} found Successfully..")
            user_dict = PatientSchema.model_validate(patient).model_dump()
            return user_dict
        else:
            logger.info(f"getPatientById() Method, patient with id {id} not found..")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in the database")
    except Exception as err:
        logger.error(f"Error in getPatientById() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


async def getPatientbyUsername(username: str, db: Session):
    try:
        patient = db.query(Patient).filter(Patient.username == username).first()
        if patient is not None:
            logger.info(f"getPatientByUsername() Method, patient with username {username} found Successfully..")
            user_dict = PatientSchema.model_validate(patient).model_dump()
            return user_dict
        else:
            logger.info(f"getPatientByUsername() Method, patient with username {username} not found..")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="patient not found in the db")
    except Exception as err:
        logger.error(f"Error in getPatientByUsername() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


async def getAllPatients(db: Session):
    try:
        patients = db.query(Patient).all()
        if patients.count() == 0:
            logger.info(f"getAllPatients() Method, No patients found in the db")
            return []
        elif patients.count() > 0:
            logger.info(f"getAllPatients() Method, {patients.count()} patients found in the db")
            patients_dict = [PatientSchema.model_validate(patient).model_dump() for patient in patients]
            return patients_dict
    except Exception as err:
        logger.error(f"Error in getAllPatients() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    

async def getPatientAppointments(id: int, db: Session):
    try:
        patient = db.query(Patient).filter(Patient.id == id).first()
        if patient is None:
            logger.info(f"getPatientAppointments() Method, Patient with id {id} not found in the db")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found in the db")
        elif patient.appointments.count() == 0:
            logger.info(f"getPatientAppointments() Method, {patient.first_name} found in the db, but the Patient has no Appointments")
            return "No Appointments for {patient.first_name} found in the db"
        else:
            logger.info(f"getPatientAppointments() Method, {patient.first_name} found in the db, and the Patient has {patient.appointments.count()} Appointments")
            appointments_dict = [AppointmentSchema.model_validate(appointment).model_dump() for appointment in patient.appointments]
            return appointments_dict
    except Exception as err:
        logger.error(f"Error in getPatientAppointments() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    

async def getPatienAssignedDoctor(id: int, db: Session):
    try:
        patient = db.query(Patient).filter(Patient.id == id).first()
        if patient is None:
            logger.info(f"getPatienAssignedDoctor() Method, Patient with id {id} not found in the db")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found in the db")
        elif patient.doctor is None:
            logger.info(f"getPatienAssignedDoctor() Method, {patient.first_name} found in the db, but the Patient has no assigned Doctor")
            return "No Doctor assigned to {patient.first_name} found in the db"
        else:
            logger.info(f"getPatienAssignedDoctor() Method, {patient.first_name} found in the db, and the Patient has assigned Doctor {patient.doctor.first_name} {patient.doctor.last_name}")
            doctor_dict = PatientSchema.model_validate(patient.doctor).model_dump()
            return doctor_dict  # Return doctor details as a dictionary (not schema)  # TODO: Update to return schema with additional fields (e.g., department, specialties)  # TODO: Implement caching for doctor details  # TODO: Add pagination for doctor list  # TODO: Add search functionality for doctor search  # TODO: Add notification system for doctor updates  # TODO: Add appointment scheduling for doctor availability  # TODO: Add doctor availability tracking  # TODO: Add doctor availability scheduling and booking  # TODO: Add doctor ratings and reviews  # TODO: Implement doctor recommendation system based on patient preferences  # TODO: Add
    except Exception as err:
        logger.error(f"Error in getPatienAssignedDoctor() Method: {err}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")