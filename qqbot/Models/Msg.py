from typing import Optional
from pydantic import BaseModel


class Sender(BaseModel):
    nickname: str
    user_id: int


class Msg(BaseModel):
    message: str
    raw_message: str
    message_type: str
    sender: Optional[Sender] = None
    time: int
    user_id: int
    group_id: int
