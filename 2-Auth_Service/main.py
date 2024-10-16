from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from Helper_Auth.elastic import checkElasticsearchConnection
from Helper_Auth.rabbitmq import checkRabbitMQConnection
from Controllers_Auth.views import auth_service_views_router
from Controllers_Auth.signup import signup_router
from Controllers_Auth.password import password_router
from Controllers_Auth.login import login_out_router
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from databas import createTable
import uvicorn

load_dotenv('.env')






@asynccontextmanager
async def lifeSpan(app: FastAPI):
    print("Welcome from lIfeSpan..")
    await checkRabbitMQConnection()
    await checkElasticsearchConnection()
    createTable()
    yield


app = FastAPI(lifespan=lifeSpan)
app.add_middleware(CORSMiddleware, allow_origins=['*'], 
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth_service_views_router, prefix="/patient", tags=["patient"])
app.include_router(signup_router, prefix="/api/v1/signup", tags=["signup"])
app.include_router(password_router, prefix="/api/v1/password", tags=["password"])
app.include_router(login_out_router, prefix='/api/v1/login', tags=["login"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",port=8002, reload=True)