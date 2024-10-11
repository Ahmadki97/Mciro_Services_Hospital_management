from fastapi import Request
from Helper_Auth.errorhandlers import NotAuthorizedError
from Helper_Auth.loghandler import logger
from functools import wraps
import jwt
import os 


def jwt_required(func):
    @wraps(func)
    async def decoratedFunction(request: Request, *args, **kwargs):
        tokens = ['patient', 'doctor', 'admin', 'appointment', 'auth', 'users']
        if 'Authorization' not in request.headers:
            raise NotAuthorizedError('Request Not Authorized', 'jwt_required(): Request not coming from API Gateway')
        api_header = request.headers.get('Authorization')
        if not api_header.startswith('Bearer '):
            raise NotAuthorizedError('Request Not Authorized', 'jwt_required(): Request not coming from API Gateway')
        try:
            token = api_header.split(' ')[1]
            jwt_token = jwt.decode(token, key=os.getenv("GATEWAY_JWT_TOKEN"), algorithms='HS256')
            payload = jwt_token.get('service_name')
            data = await request.form()
            print(f"Request headers: {request.headers}")
            print(f"Token is : {jwt_token}")
            print(f"Payload is : {payload}")
            print(f"Data in the request is : {data} and type is {type(data)} ")
            if payload not in tokens:
                raise NotAuthorizedError('Request Not Authorized', 'jwt_required(): Request PayLoad is invalid ')
            return await func(request, *args, **kwargs)
        except Exception as err:
            logger.error(f"Error in jwt_required() Decorator: {err}")
    return decoratedFunction