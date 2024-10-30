from fastapi import Depends, APIRouter, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from Helper_Users.loghandler import logger
from Services_Users.doctorservices import *
from Helper_Users.verifytoken import jwt_required
from database import get_db


doctor_router = APIRouter()
templates = Jinja2Templates(directory="Templates")


@doctor_router.get('/dashboard')
async def getDashboard(request: Request, db: Session = Depends(get_db)):
    try:
        doctor_id = request.state.user['id']
        print(f"Doctor id is {doctor_id}")
        doctor = await getDoctorById(id=doctor_id, db=db)
        logger.info(f"doctor getDashboard() Controller, No Errors..")
        doctor_dict = doctor.to_dict()
        response = {
            "doctor": doctor_dict
        }
        print(F"The response is {response}")
        return JSONResponse(response)
    except Exception as err:
        logger.error(f"Error in doctor getDashboard() Controller Method: {err}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal Server Error")


@doctor_router.get('/appointements')
async def getAppointments(request: Request, db: Session = Depends(get_db)):
    try:
        doctor_id = request.state.user['id']
        appointments = await getDoctorAppointments(db, doctor_id)
        logger.info(f"doctor getAppointments() Controller, No Errors..")
        appointemnts_list = []
        for appointment in appointments:
            appointemnts_list.append(appointment.to_dict())
        return appointemnts_list
    except Exception as err:
        logger.error(f"Error in doctor getAppointments() Controller Method: {err}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal Server Error")
    

