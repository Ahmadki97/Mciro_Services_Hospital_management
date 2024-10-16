from fastapi import Depends, HTTPException, status, APIRouter, Request
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from Helper_Auth.verifytoken import jwt_required
from Helper_Auth.loghandler import logger
from Services_Auth.authservices import loginUser, logoutUser
from databas import get_db
import json

login_out_router = APIRouter()
templates = Jinja2Templates(directory="Templates")
oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')

@login_out_router.post('/admin', name="Admin Login")
# @jwt_required
async def admin(request: Request, db: Session = Depends(get_db)):
    try:
        form_data = await request.form()
        username = form_data.get('username')
        password = form_data.get('password')
        token = await loginUser(username=username, password=password, db=db)
        return(f"User logged in Successfully..", token)
    except Exception as err:
        logger.error(f"Error in admin() controller: {err}")
        return(f"Could not login admin, Please try again..")
    

    

@login_out_router.post('/doctor', name="Doctor Login")
@jwt_required
async def doctor(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.form()
        print(f"Form Data is {data}")
        token = await loginUser(username=data['username'], password=data['password'], db=db)
        logger.info(f"Doctor Controller, User {data['username']} Logged in Successfully..")
        response = {
            "token": token,
        }
        return JSONResponse(response)
    except Exception as err:
        logger.error(f"Error in doctor() controller: {err}")
        return(f"Could not login doctor, Please try again..")



@login_out_router.post('/patient', name="Patient Login")
@jwt_required
async def patient(request: Request, db: Session = Depends(get_db)):
    try:
        form_data = await request.form()
        username = form_data.get('username')
        password = form_data.get('password')
        token = await loginUser(username=username, password=password, db=db)
        logger.info(f"Patient Controller, User {username} Logged in Successfully..")
        return(f"User logged in Successfully..", token)
    except Exception as err:
        logger.error(f"Error in patient() controller: {err}")
        return(f"Could not login patient, Please try again..")


@login_out_router.delete('/user', name="Logout User")
@jwt_required
async def userLogout(db: Session = Depends(get_db), token:str = Depends(oauth2_schema)):
    try:
        await logoutUser(db=db, token=token)
    except Exception as err:
        logger.error(f"Error in logoutUser() controller: {err}")
        return(f"Could not logout user, Please try again..")
