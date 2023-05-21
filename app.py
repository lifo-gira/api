from fastapi import FastAPI
from typing import Literal
from fastapi.middleware.cors import CORSMiddleware
from models import Admin, Doctor, Patient
import db


app = FastAPI()

storedData = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"Message": "use '/docs' endpoint to find all the api related docs "}


@app.post("/post-data/{data}")
def postData(data):
    try:
        storedData.append(data)
        return {"inserted": "true"}

    except:
        return {"inserted": "false"}

@app.get("/get-all-data")
def getData():
    return storedData

    
@app.post("/create-adminuser")
async def createAdminUser(data: Admin):
    res = await db.createAdminUser(data=data)
    return{"user creation status": res} 

@app.post("/create-doctor")
async def createDoctor(data: Doctor):
    res = await db.createDoctor(data=data)
    return{"user creation status": res}

@app.post("/create-patient")
async def createPatient(data: Patient):
    res = await db.createPatient(data=data)
    return{"user creation status": res}

@app.post("/login")
async def initiateLogin(user_id: str, password: str):
    res = await db.loginUser(user_id, password) 
    if res["loginStatus"] == True:
        return res["data"]

@app.get("/get-all-user/{type}")
async def getUsers(type: Literal["admin", "doctor", "patient", "all"]):
    res = await db.getAllUser(type)
    return res