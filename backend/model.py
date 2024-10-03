from pydantic import BaseModel

class User(BaseModel):
    email: str
    name: str

class GoogleAuthRequest(BaseModel):
    token: str

class Location(BaseModel):
    label:str
    lat:str
    lon:str