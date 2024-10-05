import json
import jwt
import os 
import aiohttp
from fastapi import Request, HTTPException, status, UploadFile, File
from fastapi.responses import HTMLResponse 
from dotenv import load_dotenv
from Helper_API.loghandler import logger

load_dotenv('.env')
gateway_jwt_token = os.getenv('GATEWAY_JWT_TOKEN')

class RequestHandler():
    def __init__(self, service_url):
        self.service_url = service_url
        self.key = gateway_jwt_token

    async def createJwtToken(self, service_token):
        try:
            payload = {
                "service_name": service_token
            }
            token = jwt.encode(payload, gateway_jwt_token, algorithm='HS256')
            return token
        except Exception as err:
            logger.error(f"Error in createJwtToken() Method: {err}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in generating JWT token.")
        
        
    async def makeRequest(self, endpoint, service_token, request: Request):
        try:
            url = f"{self.service_url}/api/v1/{endpoint}"
            if "users" not in url:
                token = await self.createJwtToken(service_token=service_token)
                headers = {
                'Authorization': f"Bearer {token}",
            }
            else:
                headers = request.headers
            print(f"Destination url is : {url}")
            form_data = await request.form()
            file = form_data.get('profile_pic')
            # Prepare files dictionary
            data = aiohttp.FormData()
            if file is not None:
                data.add_field(name="profile_pic", value=await file.read())
            for key, value in form_data.items():
                if key=="profile_pic":
                # Add file directly
                    print(f"This is instance of UploadFile, and it will not be add")
                    continue
                else:
                    data.add_field(key, value)
            async with aiohttp.ClientSession() as session:
                if request.method == "GET":
                    async with session.get(url, headers=headers) as response:
                        content_type = response.headers.get('Content-Type', '')
                        if 'text/html' in content_type:
                            return HTMLResponse(content=await response.text(), status_code=response.status)
                        return await response.json()
                elif request.method == "POST":
                    async with session.post(url, headers=headers, data=data) as response:
                        content_type = response.headers.get('Content-Type', '')
                        if 'text/html' in content_type:
                            return HTMLResponse(content=await response.text(), status_code=response.status)
                        return await response.json()
                elif request.method == "PUT":
                    async with session.put(url, headers=headers, data=data) as response:
                        content_type = response.headers.get('Content-Type', '')
                        if 'text/html' in content_type:
                            return HTMLResponse(content=await response.text(), status_code=response.status)
                        return await response.json()
                elif request.method == "DELETE":
                    async with session.delete(url, headers=headers) as response:
                        content_type = response.headers.get('Content-Type', '')
                        if 'text/html' in content_type:
                            return HTMLResponse(content=await response.text(), status_code=response.status)
                        return await response.json()
        except Exception as err:
            logger.error(f"Error in makeRequest() Method: {err}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in making request to the remote service.")
