from Helper_API.loghandler import logger
from Helper_API.requesthandler import RequestHandler
from fastapi import APIRouter, Request, UploadFile, File, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import os 




templates = Jinja2Templates(directory="Templates")
load_dotenv('.env')



auth_router = APIRouter()
request_handler = RequestHandler(service_url=os.getenv('AUTH_BASE_URL'))
users_service_handler = RequestHandler(service_url=os.getenv('USER_BASE_URL'))

@auth_router.get('/signup/doctor')
async def getSignupDoctor(request: Request):
    print(f"Auth Url is : {os.getenv('AUTH_BASE_URL')}")
    try:      
        return templates.TemplateResponse(request=request, name="doctorsignup.html")
    except Exception as err:
        logger.error(f"Error in getSignupDoctor() Method: {err}")
        return {"message": "Error in getSignupDoctor() process."}
    

@auth_router.post('/signup/doctor')
async def signupDoctor(request: Request, profile_pic: UploadFile=File(None)):
    print(f"Auth Url is : {os.getenv('AUTH_BASE_URL')}")
    try:
        await request_handler.makeRequest(endpoint='signup/doctor', service_token='auth', request=request)        
        logger.info(f"signupdoctor() Controller, Request sent to the Aplicable Service")
        return RedirectResponse(url="/api/v1/auth/login/doctor", status_code=status.HTTP_303_SEE_OTHER)
    except Exception as err:
        logger.error(f"Error in signupDoctor() Method: {err}")
        return {"message": "Error in signupDoctor() process."}
    

@auth_router.get('/signup/admin')
async def getSignupAdmin(request: Request):
    print(f"Auth Url is : {os.getenv('AUTH_BASE_URL')}")
    try:
        return templates.TemplateResponse(request=request, name="adminsignup.html")
    except Exception as err:
        logger.error(f"Error in getSignupAdmin() Method: {err}")
        return {"message": "Error in getSignupAdmin() process."}
    

@auth_router.post('/signup/admin')
async def signupAdmin(request: Request):
    print(f"Auth Url is : {os.getenv('AUTH_BASE_URL')}")
    try:
        await request_handler.makeRequest(endpoint='signup/admin', service_token='auth', request=request)        
        logger.info(f"signupAdmin() Controller, Request sent to the Aplicable Service")
        return RedirectResponse(url="/api/v1/auth/login/admin", status_code=status.HTTP_200_OK)
    except Exception as err:
        logger.error(f"Error in signupAdmin() Method: {err}")
        return {"message": "Error in signupAdmin() process."}
    

@auth_router.get('/signup/patient')
async def getSignupPatient(request: Request):
    print(f"Auth Url is : {os.getenv('AUTH_BASE_URL')}")
    try:
        return templates.TemplateResponse(request=request, name="patientsignup.html")
    except Exception as err:
        logger.error(f"Error in getSignupPatient() Method: {err}")
        return {"message": "Error in getSignupPatient() process."}
    

@auth_router.post('/signup/patient')
async def signupPatient(request: Request):
    print(f"Auth Url is : {os.getenv('AUTH_BASE_URL')}")
    try:
        await request_handler.makeRequest(endpoint='signup/patient', service_token='auth', request=request)        
        logger.info(f"signuppatient() Controller, Request sent to the Aplicable Service")
        return RedirectResponse(url="/api/v1/auth/login/patient")
    except Exception as err:
        logger.error(f"Error in signupPatient() Method: {err}")
        return {"message": "Error in signupPatient() process."}
    

##############################Login########################################
    

@auth_router.get("/login/admin")
async def getLoginAdmin(request: Request):
    try:
        return templates.TemplateResponse(request=request, name="adminlogin.html")
    except Exception as err:
        logger.error(f"Error in getLoginAdmin() Method: {err}")
        return {"message": "Error in getLoginAdmin() process."}
    

@auth_router.post("/login/admin")
async def loginAdmin(request: Request):
    try:
        await request_handler.makeRequest(endpoint='login/admin', service_token='auth', request=request)
        logger.info(f"loginAdmin() Controller, Request sent to the Aplicable Service")
        return RedirectResponse(url='api/v1/users/admin/dashboard', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as err:
        logger.error(f"Error in loginAdmin() Method: {err}")
        return {"message": "Error in loginAdmin() process."}
    

@auth_router.get("/login/doctor")
async def getLoginDoctor(request: Request):
    try:
        print("Hello from Login Doctor Page")
        return templates.TemplateResponse(request=request, name="doctorlogin.html")
    except Exception as err:
        logger.error(f"Error in getLoginDoctor() Method: {err}")
        return {"message": "Error in getLoginDoctor() process."}
    

@auth_router.post("/login/doctor")
async def loginDoctor(request: Request):
    try:
        pass 
        token = await request_handler.makeRequest(endpoint='login/doctor', service_token='auth', request=request)
        print(f"Token is: {token}")
        return token
        # response = RedirectResponse(url='/api/v1/users/doctor/dashboard', status_code=status.HTTP_303_SEE_OTHER)
        # response.set_cookie(key='token', value=token['token'], httponly=True, max_age=3600)
        # return response
    except Exception as err:
        logger.error(f"Error in loginDoctor() Method: {err}")
        return {"message": "Error in loginDoctor() process."}
    

@auth_router.get("/login/patient")
async def getLoginPatient(request: Request):
    try:
        return templates.TemplateResponse(request=request, name="patientlogin.html")
    except Exception as err:
        logger.error(f"Error in getLoginPatient() Method: {err}")
        return {"message": "Error in getLoginPatient() process."}
    

@auth_router.post("/login/patient")
async def loginPatient(request: Request):
    try:
        await request_handler.makeRequest(endpoint='login/patient', service_token='auth', request=request)
        logger.info(f"loginPatient() Controller, Request sent to the Aplicable Service")
        return RedirectResponse(url='api/v1/users/patient/dashboard', status_code=status.HTTP_303_SEE_OTHER)
    except Exception as err:
        logger.error(f"Error in loginPatient() Method: {err}")
        return {"message": "Error in loginPatient() process."}
    

##################################