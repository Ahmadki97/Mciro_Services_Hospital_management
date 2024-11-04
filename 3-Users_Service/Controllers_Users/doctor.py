from fastapi import Depends, APIRouter, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from Helper_Users.loghandler import logger
from Services_Users.doctorservices import *
from Helper_Users.verifytoken import jwt_required
from database import get_db


doctor_router = APIRouter()
templates = Jinja2Templates(directory="Templates")


@doctor_router.get('/get-doctor')
async def getDoctor(request: Request, db: Session = Depends(get_db)):
    try:
        doctor_id = request.state.user['id']
        doctor = await getDoctorById(id=doctor_id, db=db)
        return JSONResponse(doctor.to_dict())
    except Exception as err:
        logger.error(f"Error in doctor getDoctor() Controller Method: {err}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal Server Error")


@doctor_router.get('/dashboard')
async def getDashboard(request: Request, db: Session = Depends(get_db)):
    try:
        doctor_id = request.state.user['id']
        print(f"Doctor id is {doctor_id}")
        doctor = await getDoctorById(id=doctor_id, db=db)
        logger.info(f"doctor getDashboard() Controller, No Errors..")
        doctor_dict = doctor.to_dict()
        count = 0
        appointments_count = 0
        if len(doctor.patients) > 0:
            count = len(doctor.patients)
        elif len(doctor.appointments) > 0:
            appointments_count = len(doctor.appointments)
        response = {
            "doctor": doctor_dict,
            "count": count,
            "appointments": appointments_count
        }
        print(F"The response is {response}")
        return JSONResponse(response)
    except Exception as err:
        logger.error(f"Error in doctor getDashboard() Controller Method: {err}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal Server Error")


@doctor_router.get('/appointments')
async def getAppointments(request: Request, db: Session = Depends(get_db)):
    try:
        doctor_id = request.state.user['id']
        appointments = await getDoctorAppointments(id=doctor_id, db=db)
        logger.info(f"doctor getAppointments() Controller, appointments for doctor with id {doctor_id} retreived successfully")
        appointemnts_list = []
        for appointment in appointments:
            appointemnts_list.append(appointment.to_dict())
        return appointemnts_list
    except Exception as err:
        logger.error(f"Error in doctor getAppointments() Controller Method: {err}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal Server Error")
    

@doctor_router.get('/patients')
async def getPatients(request: Request, db: Session = Depends(get_db)):
    try:
        doctor_id = request.state.user['id']
        patients = await getDoctorPatients(id=doctor_id, db=db)
        logger.info(f"doctor getPatients() Controller, patients for doctor with id {doctor_id} retreived successfully")
        patients_list = []
        for patient in patients:
            patients_list.append(patient.to_dict())
        return patients_list
    except Exception as err:
        logger.error(f"Error in doctor getPatients() Controller Method: {err}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal Server Error")
    

@doctor_router.get('/timeslots')
async def getDoctorTimeSlots(request: Request, db: Session = Depends(get_db)):
    try:
        doctor_id = request.state.user['id']
        doctor = await getDoctorById(id=doctor_id, db=db)
        logger.info(f"doctor getDoctorTimeSlots() Controller, doctor with id {doctor_id} retreived successfully")
        return JSONResponse(doctor.time_slots)
    except Exception as err:
        logger.error(f"Error in doctor getDoctorTimeSlots() Controller Method: {err}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal Server Error")
    

