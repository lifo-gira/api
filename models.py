from pydantic import BaseModel
from typing import Literal, Optional
from datetime import datetime

class Admin(BaseModel):
    type: Literal["admin", "doctor", "patient"]
    name: str
    user_id: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "type": "admin",
                "name": "admin 1",
                "user_id": "admin001",
                "password": "Password@123"
            }
        }

class Doctor(BaseModel):
    type: Literal["admin", "doctor", "patient"]
    name: str
    user_id: str
    password: str
    patients: list

    class Config:
        schema_extra = {
            "example": {
                "type": "doctor",
                "name": "doctor 1",
                "user_id": "doctor001",
                "password": "Password@123",
                "patients": ["13234", "341324"]
            }
        }

class Patient(BaseModel):
    type: Literal["admin", "doctor", "patient"]
    name: str
    user_id: str
    password: str
    data: list
    videos: list
    doctor: str


    class Config:
        schema_extra = {
            "example": {
                "type": "patient",
                "name": "patien 1",
                "user_id": "patient001",
                "password": "Password@123",
                "data": ["data1", "data2"],
                "videos": [],
                "doctor": "doctor001"
                
            }
        }