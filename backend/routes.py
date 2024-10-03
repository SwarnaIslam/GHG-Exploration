from fastapi import APIRouter, HTTPException, Depends
from jose import jwt, JWTError
import requests
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from config import users_collection
from model import User, GoogleAuthRequest, Location
from typing import Any, List
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
import aiohttp
import json
from emailService import send_email
import os
from dotenv import load_dotenv
load_dotenv()

user=APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def verify_google_token(token: str):
    response = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}")
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Invalid token")
    return response.json()

@user.post("/auth/login")
async def login(token: GoogleAuthRequest):
    user_info = await verify_google_token(token.token)
    email = user_info["email"]
    name = user_info["name"]

    user = users_collection.find_one({"email": email})
    if not user:
        users_collection.insert_one({"email": email, "name": name, "location":[]})

    access_token = create_access_token(data={"email": email})
    return {"access_token": access_token, "token_type": "bearer"}



@user.get("/auth/verify", response_model=User)
async def verification(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        user = users_collection.find_one({"email": email}, {"name": 1, "email": 1})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
def fetch_location_by_coordinates(location:Location):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={location.label}&lat={location.lat}&lon={location.lon}&addressdetails=1&limit=1&polygon_geojson=1"

    headers = {
        "User-Agent": "MyApp/1.0 (your-email@example.com)",
        "Accept-Language": "en",
    }
    response = requests.get(url, headers=headers)
    return response.json()[0]["geojson"]

@user.post("/user/notify")
async def update(location:Location,  token: str= Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get("email")
    geojson= fetch_location_by_coordinates(location)
    result = users_collection.update_one(
        {"email": email},
        {"$set": {"location": geojson}}  
    )
    return {"message":"success"}
async def get_plume_update(limit):
    api_url = f"https://earth.gov/ghgcenter/api/stac/collections/emit-ch4plume-v1/items?limit={limit}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            data = await response.json()
            features = data.get("features", {})
            plumes = []
            for i in range(len(features)):
                plumes.append({"link":features[i]["links"][4]["href"], "geometry":features[i]["geometry"], "datetime":features[i]["properties"]["datetime"]})
            return plumes

def get_previous_length_from_file():
    try:
        with open('length.json', 'r') as file:
            data = json.load(file)
            return data.get('previous_length', 0)
    except FileNotFoundError:
        return 0

def save_previous_length_to_file(new_length):
    with open('length.json', 'w') as file:
        json.dump({'previous_length': new_length}, file)
async def notify_user(datetime_specific_plumes):
    for plume in datetime_specific_plumes:
        pipeline = [
            {
                "$match": {
                    "location": {
                        "$geoIntersects": {
                            "$geometry": plume["geometry"]
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "name": 1,
                    "email": 1
                }
            }
        ]  
        users = list(users_collection.aggregate(pipeline))
        if len(users)>0:
            await send_email(users, {"link":plume["link"], "datetime":plume["datetime"]})
    pass
async def check_latest_length():
    api_url = f"https://earth.gov/ghgcenter/api/stac/collections/emit-ch4plume-v1/items?limit=1"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            data = await response.json()
            latest_length=data.get("context",{}).get("matched",0)
            return latest_length
    return 0
async def checkPlumeUpdates():
    try:   
        previous_length = get_previous_length_from_file()
        latest_length = await check_latest_length()
        
        if previous_length < latest_length:
            
            datetime_specific_plumes = await get_plume_update(latest_length-previous_length)
            
            save_previous_length_to_file(latest_length)
            await notify_user(datetime_specific_plumes)  
            pass
        else:
            pass
    except requests.exceptions.RequestException as e:
        pass

def start_scheduler():
    loop = asyncio.get_event_loop()
    scheduler = BackgroundScheduler()

    # Instead of asyncio.run, use create_task to run the coroutine in the background
    scheduler.add_job(lambda: loop.create_task(checkPlumeUpdates()), 'interval', seconds=30)
    scheduler.start()

@user.on_event("startup")
async def startup_event():
    start_scheduler()
