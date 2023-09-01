from fastapi import FastAPI, WebSocket
from typing import Literal
from fastapi.middleware.cors import CORSMiddleware
from models import Admin, Doctor, Patient, Data
import db
from models import ConnectionManager
from db import get_user_from_db


app = FastAPI()
manager = ConnectionManager()

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

@app.post("/metrics")
async def getData(data_id: list):
    res = await db.getData(data_id)
    return res

@app.websocket("/ws/metrics")
async def metrics_socket(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_json()  # Wait for incoming JSON data
        data_id = data.get("data", [])     # Extract data_id from the received data

        res = await db.getData(data_id)

        await websocket.send_json(res)        # Send the result back to the client


@app.websocket("/ws-get-user/{type}/{id}")
async def websocket_endpoint(type: Literal["admin", "doctor", "patient"], id: str, websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Fetch user data based on type and id here
        user = await db.getUser(type, id)  # Replace with your actual data retrieval function

        if user:
            user_data = user.dict()  # Convert user data to a dictionary
            response_message = {"status": "success", "data": user_data}
            await manager.send_message(websocket, response_message)
        else:
            error_message = {"status": "error", "message": "User not found"}
            await manager.send_message(websocket, error_message)
    except Exception as e:
        error_message = {"status": "error", "message": str(e)}
        await manager.send_message(websocket, error_message)
    finally:
        manager.disconnect(websocket)