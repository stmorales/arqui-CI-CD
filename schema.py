from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str


class User(UserCreate):
    id: int


class UserList(BaseModel):
    users: List[User] = []


class GroupCreate(BaseModel):
    name: str
    users: List[int]
    userId: int

class Group(BaseModel):
    id: int
    name: str

class GroupMessageCreate(BaseModel):
    body: str
    username: str
    groupId: int

class MessageCreate(BaseModel):
    body: str
    userId: int
    receptorId: int


class Message(BaseModel):
    body: str
    time: datetime
    user: User
    receptor: User

# class MessageList(BaseModel):
#     messages: List[Message]

class Notification(BaseModel):
    message: str
    groupId: int
    notifiedUser: User
