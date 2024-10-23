from typing import Any
from fastapi import FastAPI, Request, status, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from Helper_Users.loghandler import logger
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from jwt import PyJWTError, ExpiredSignatureError, InvalidTokenError
import jwt
import os 


load_dotenv('.env')

class JwtMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        authorization = request.cookies
        print(f"Authorization is {authorization}")
        print(f"Headers is {request.headers}")
        if not authorization or not authorization['token']:
            logger.info(f"Token Missing or Invalid")
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content="Token Missing or Invalid")
        token = authorization['token']
        print(f"The token is: {token}")
        print(f"Authorization is {authorization}")
        # Verify The token
        try:
            print(f"Secret KEY is: {os.getenv('SECRET_KEY')}")
            # The decode automatically checks for token experation if exp is found ni the token
            payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            request.state.user = {
                "id": payload.get('id'),
                "email": payload.get('email'),
                "username": payload.get('username'),
            }
        except PyJWTError as err:
            logger.error(f"PyJWTError in JWTMiddleware: {err}")
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content="Invalid Token")
        
        except ExpiredSignatureError:
            logger.error(f"ExpiredSignatureError in JWTMiddleware: {err}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is expired")
        
        except InvalidTokenError:
            logger.error(f"InvalidTokenError in JWTMiddleware: {err}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
        response = await call_next(request)
        return response

