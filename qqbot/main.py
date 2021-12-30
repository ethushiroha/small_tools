from Models.Msg import Msg
from fastapi import FastAPI
from Utils.Manager import Parser
from Config.Config import *
from Utils.Reminder import Reminder

app = FastAPI()


@app.post("/")
async def index(msg: Msg):
    try:
        return Parser(msg)
    except Exception as e:
        logger.error("index exception: " + e.__str__())
        return None


@app.get("/Remind")
async def Remind(func: str):
    try:
        return Reminder(func=func).remind()
    except Exception as e:
        logger.error("RemindCard Error")
        return None
