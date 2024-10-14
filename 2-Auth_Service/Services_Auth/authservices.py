from Models_Auth.Users import User
from Models_Auth.userschemas import UserSchema, CreateUser
from fastapi import HTTPException, status, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from Helper_Auth.loghandler import logger
from Helper_Auth.rabbitmq import startPuplishingMessage
from dotenv import load_dotenv
import datetime
import json
import jwt
import os 


load_dotenv('.env')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
async def createAuthUser(user_create: dict, db:Session):
    try:
        hashed_password = pwd_context.hash(user_create['password'])
        user_create['password'] = hashed_password
        user = User(**user_create)
        db.add(user)
        logger.info(f"createAuthUser() Method, User with id {user.id} is added to the database")
        db.commit()
        db.refresh(user)
        return user
    except Exception as err:
        logger.error(f"Error in createAuthUser() Method: {err}")
        return False
    

async def getAuthUserById(user_id: int, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        user_dict = UserSchema.model_validate(user).model_dump()
        if user is None:
            logger.info(f"getAuthUserById() Method, Could not Found user with id {user_id}")
        else:
            logger.info(f"getAuthUserById() Method, User with id {user_id} Found")
            return user_dict 
    except Exception as err:
        logger.error(f"Error in getAuthUserById() Method, could not found user with id {user_id}: {err}")
        return False
    

async def getAuthUserByEmail(email: str, db:Session):
    try:
        user = db.query(User).filter(User.email == email).first()
        user_dict = UserSchema.model_validate(user).model_dump()
        if user is None:
            logger.info(f"getAuthUserByEmail() Method, Could not find User with email {email}")
        else:
            logger.info(f"getAuthUserByEmail() Method, User with email {email} Found")
            return user_dict
    except Exception as err:
        logger.error(f"Error in getAuthUserByEmail() Method, could not found user with email {email}: {err}")

async def getAuthUserByUsername(username: str, db:Session):
    try:
        user = db.query(User).filter(User.username == username).first()
        user_dict = UserSchema.model_validate(user).model_dump()
        if user is None:
            logger.info(f"getAuthUserByUsername() Method, Could not find user with username {username}")
        else:
            logger.info(f"getAuthUserByUsername() Method, User with username {username} Found.")
            return user_dict  
    except Exception as err:
        logger.error(f"Error in getAuthUserByUsername() Method, could not find user with username {username}: {err}")
        return False


async def updateAuthUserStatus(id: int, db: Session):
    try:
        user = db.query(User).filter(User.id == id).first()
        if user is None:
            logger.info(f"updateAuthUserStatus() Method, could not find user with id {id}")
        else:
            user.status = True
            db.commit()
            db.refresh(user)
            logger.info(f"updateAuthUserStatus() Method, User with id {id} status has been updated successfully")
    except Exception as err:
        logger.error(f"Error in updateAuthUserStatus() Method: {err}")
        return False
    

async def updateAuthUserPassword(id: int, old_password: str, new_password: str, db: Session):
    try:
        user = db.query(User).filter(User.id == id).first()
        if user is None:
            logger.info(f"updateAuthUserPassword() Method, could not find user with id {id}")
            return False
        elif pwd_context.verify(old_password, user.password):
            user.password = pwd_context.hash(new_password)
            db.commit(user)
            logger.info(f"updateAuthUserPassword() Method, Password for user with id {user.id} Updated Successfully")
            return True
    except Exception as err:
        logger.error(f"Error in updateAuthUserPassword() Method: {err}")
        return False
    

async def passwordResetToken(email: str, db: Session):
    try:
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            logger.info(f"passwordResetToken() Method, could not find user with id {id}")
            return False
        # Generate JWT Token for Password Reset
        expire = datetime.datetime.now() + datetime.timedelta(hours=1)
        payload = {
            "sub": email,
            "exp": expire
        }
        token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm="HS256")
        # add the token to the user record
        user.reset_password_token = token
        user.reset_password_token_expired = expire
        db.commit()
        # Initaite Password Reset Link
        reset_link = f"http://{os.getenv('CLIENT_URL')}/reset-password?token={token}"
        # Send The Reset Link to the Notification Service
        message = {
            "email": email,
            "reset_link": reset_link
        }
        await startPuplishingMessage(queue='password', exchange_name='', routing_key='password', body=json.dumps(message))
        logger.info(f"User reset password token Updated for user with id {user.id}")
    except Exception as err:
        logger.error(f"Error in sendPasswordResetToken() Method: {err}")


async def loginUser(username: str, password: str, db: Session):
    try:
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            logger.error(f"loginUser() Method, Could not find user with username {username}")
            return {"Message": HTTPException(status_code=status.HTTP_404_NOT_FOUND)}
        elif pwd_context.verify(password, user.password):
            # Initiate JWT Token
            expire = datetime.datetime.now() + datetime.timedelta(weeks=1)
            payload = {
                "user": user.username,
                "id": user.id,
                "email": user.email,
                "exp": expire
            }
            token = user.token
            if token is None:
                token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm="HS256")
                user.token = token
                db.commit()
                print(f"User is: {user} and type is {type(user)}")
            else:
                logger.info(f"Token for user with id {user.id} already exists.")
            print(f"Token in LoginUser() is: {token}")
            return token
        else:
            logger.error(f"loginUser() Method, Incorrect password for user with username {username}")
            return {"Message": "Incorrect username or password..please try again."}
    except Exception as err:
        logger.error(f"Error in loginUser() Method: {err}")
        return False
    

async def logoutUser(db: Session, token: str):
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        id = payload['id']
        user = db.query(User).filter(User.id == id).first()
        user.token = None
        db.commit()
        logger.info(f"Token for user with id {user.id} deleted successfully.")
        return True 
    except Exception as err:
        logger.error(f"Error in logoutUser() Method: {err}")
        return False