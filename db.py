from motor import motor_asyncio
from models import *

client = motor_asyncio.AsyncIOMotorClient("mongodb+srv://lifogira:passwordPassword@main.zcij1ne.mongodb.net/?retryWrites=true&w=majority")
db = client.Main
users = db.users

async def getAllUser(type):
    try:
        allUsers = []
        if type == "all":
            cursor = users.find({}, {'_id': 0})
        else:
            cursor = users.find({"type": type}, {'_id': 0})
        for document in await cursor.to_list(length=100):
            allUsers.append(document)
    except Exception as e:
        print(e)
    return allUsers

async def createAdminUser(data: Admin):
    try:
        await users.insert_one(dict(data))
        return True
    except Exception as e:
        print(e)
        return False
    
async def createDoctor(data: Doctor):
    try:
        await users.insert_one(dict(data))
        return True
    except:
        return False
    
async def createPatient(data: Patient):
    try:
        await users.insert_one(dict(data))
        return True
    except:
        return False
    
async def loginUser(user_id, password):
    user = {"data": {}, "loginStatus": False}
    res = await users.find_one({"user_id": user_id, "password": password},{'_id': 0})
    try: 
        user["data"] = res
        user["loginStatus"] = True
    except Exception as e:
        print(e)
        user["loginStatus"] = False
    finally:
        return user