from Helper_Users.loghandler import logger
from Services_Users.adminservices import *
from fastapi import APIRouter, Request, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db



admin_router = APIRouter()


@admin_router.get('/get-admin')
async def getAdmin(request: Request, db: Session=Depends(get_db)):
    try:
        admin_id = request.state.user['id']
        admin = await getAdminById(id=admin_id, db=db)
        response = {
            "admin": admin
        }
        return JSONResponse(response)
    except Exception as err:
        logger.error(f"Error in getAdmin() Method: {err}")
        return JSONResponse("Could not load admin data, please try again later..")


@admin_router.get('/dashboard')
async def getDashboard(request: Request, db: Session=Depends(get_db)):
    try:
        doctors = await getDoctors(db=db)
        patients = await getPatients(db=db)
        pending_doctors = await getPendingDoctors(db=db)
        pending_patients = await getPendingPatients(db=db)
        admin_id = request.state.user['id']
        print(f"Admin ID is: {admin_id}")
        admin = await getAdminById(id=admin_id, db=db)
        data = {
            "doctors": doctors,
            "patients": patients,   
            "admin": admin,
            "pending_doctors": pending_doctors,
            "pending_patients": pending_patients,
        }
        print(f"Data is: {data}")
        return JSONResponse(data)
    except Exception as err:
        logger.error(f"Error in getDashboard() Controller: {err}")
        return JSONResponse("Could not load admin data, please try again later..")
    

@admin_router.get('/doctors')
async def viewDoctors(request: Request, db: Session=Depends(get_db)):
    try:
        doctors = await getDoctors(db=db)
        logger.info(f"admin viewDoctors Controller, Successfully Found Doctors")
        data = {
            "doctors": doctors
        }
        return JSONResponse(data)
    except Exception as err:
        logger.error(f"Error in viewDoctors() Controller: {err}")
        return JSONResponse("Could not load doctor data, please try again later..")
    

@admin_router.put("/approve-doctor/{id}")
async def approveDoctor(request: Request, id: int, db: Session=Depends(get_db)):
    try:
        await acceptDoctor(id=id, db=db)
        logger.info(f"admin approveDoctor Controller, Successfully Approved Doctor with id {id}")
        return JSONResponse("Doctor approved successfully.")
    except Exception as err:
        logger.error(f"Error in approveDoctor() Controller: {err}")
        return JSONResponse("Could not approve doctor, please try again later..")
    

@admin_router.get('/patients')
async def viewPatients(request: Request, db: Session=Depends(get_db)):
    try:
        patients = await getPatients(db=db)
        logger.info(f"admin viewPatients Controller, Successfully Found Patients")
        data = {
            "patients": patients
        }
        print(data)
        return JSONResponse(data)
    except Exception as err:
        logger.error(f"Error in viewPatients() Controller: {err}")
        return JSONResponse("Could not load patient data, please try again later..")
    

@admin_router.delete("/decline-doctor/{id}")
async def declineDoctor(request: Request, id: int, db: Session=Depends(get_db)):
    try:
        await refuseDoctor(id=id, db=db)
        logger.info(f"admin refuseDoctor Controller, Successfully refused Doctor with id {id}")
        return JSONResponse("Doctor refused successfully.")
    except Exception as err:
        logger.error(f"Error in refuseDoctor() Controller: {err}")
        return JSONResponse("Could not refuse doctor, please try again later..")
    

@admin_router.put("/approve-patient/{id}")
async def approvePatient(request: Request, id: int, db: Session=Depends(get_db)):
    try:
        await acceptPatient(id=id, db=db)
        logger.info(f"admin approvePatient Controller, Successfully approved Patient with id {id}")
        return JSONResponse("Patient approved successfully.")
    except Exception as err:
        logger.error(f"Error in approvePatient() Controller: {err}")
        return JSONResponse("Could not approve patient, please try again later..")
    

@admin_router.delete("/decline-patient/{id}")
async def declineDoctor(request: Request, id: int, db: Session = Depends(get_db)):
    try:
        await refusePatient(id=id, db=db)
        logger.info(f"admin refusePatient Controller, Successfully refused Patient with id {id}")
        return JSONResponse("Patient refused successfully.")
    except Exception as err:
        logger.error(f"Error in refusePatient() Controller: {err}")
        return JSONResponse("Could not refuse patient, please try again later..")
    

@admin_router.get('/appointments')
async def viewAppointments(request: Request):
    try:
        # appointments = await getAppointments()
        logger.info(f"admin viewAppointments Controller, Successfully Found Appointments")
        # data = {
        #     "appointments": appointments
        # }
        # return JSONResponse(data)
    except Exception as err:
        logger.error(f"Error in viewAppointments() Controller: {err}")
        return JSONResponse("Could not load appointment data, please try again later..")