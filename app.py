from fastapi import FastAPI
from typing import Literal
from fastapi.middleware.cors import CORSMiddleware
from models import Admin, Doctor, Patient, Data
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
    return{"userCreated": res} 

@app.post("/create-doctor")
async def createDoctor(data: Doctor):
    res = await db.createDoctor(data=data)
    return{"userCreated": res}

@app.post("/create-patient")
async def createPatient(data: Patient):
    res = await db.createPatient(data=data)
    return{"userCreated": res}

@app.post("/login")
async def initiateLogin(user_id: str, password: str):
    res = await db.loginUser(user_id, password) 
    if res["loginStatus"] == True:
        return res["data"]

@app.get("/get-all-user/{type}")
async def getUsers(type: Literal["admin", "doctor", "patient", "all"]):
    res = await db.getAllUser(type)
    return res

@app.get("/get-user/{type}/{id}")
async def getUsers(type: Literal["admin", "doctor", "patient"], id: str):
    res = await db.getUser(type, id)
    return res

@app.post("/post-data")
async def addData(user_id: str,data: Data):
    res = await db.postData(user_id=user_id, data=data)
    return{"dataCreated": res}

@app.put("/put-data")
async def addData( data: Data):
    res = await db.putData(data=data)
    return{"dataCreated": res}

@app.get("/metrics/{id}")
async def getData(data_id: str):
    res = await db.getData(data_id)
    return res
