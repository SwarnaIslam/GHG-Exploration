from fastapi import FastAPI
from routes import user

app=FastAPI()
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    
    CORSMiddleware,
    allow_origins=["https://ghg-exploration.netlify.app"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

app.include_router(user)
