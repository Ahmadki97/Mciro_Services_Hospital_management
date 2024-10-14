from Helper_Auth.loghandler import logger
from Helper_Auth.verifytoken import jwt_required
from Models_Auth.userschemas import UserSchema
from Services_Auth.authservices import getAuthUserById, getAuthUserByEmail, getAuthUserByUsername
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="Templates")
get_router = APIRouter()

@get_router.get('/<int:id>', name="getId")
@jwt_required
async def UserById(request: Request, id: int):
    try:
        user = await getAuthUserById(id)
        logger.info(f"UserById() Controller Method, User with ID: {id} returned successfully.")
        return(user)
    except Exception as err:
        logger.error(f"Error in UserById() Controller Method: {err}")
        return {"message": "Error in UserById() process."}
    

@get_router.get('/<str:username>', name="getUsername")
@jwt_required
async def userByUsername(request: Request, username: str):
    try:
        user = await getAuthUserByUsername(username)
        logger.info(f"UserByUsername() Controller Method, User with username: {username} returned successfully.")
        return(user)
    except Exception as err:
        logger.error(f"Error in UserByUsername() Controller Method: {err}")
        return {"message": "Error in UserByUsername() process."}