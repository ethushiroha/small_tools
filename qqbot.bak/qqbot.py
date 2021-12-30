from Models.Msg import Msg
from fastapi import FastAPI

import json

app = FastAPI()


@app.post("/")
async def index(msg: Msg):
    
    return None
