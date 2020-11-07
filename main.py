from fastapi import FastAPI, Request, responses, templating, Form
import uvicorn
import fastapi
import socketio
import os
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db
from views import web_app
from dotenv import load_dotenv
import models, schema
from datetime import datetime
import json
from starlette.responses import RedirectResponse
from typing import Optional, List
from sqlalchemy import or_
import random
from fastapi.middleware.cors import CORSMiddleware
import httpx

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://frontend-grupo14-arqui.tk",
        "http://www.frontend-grupo14-arqui.tk",
        "https://frontend-grupo14-arqui.tk",
        "https://frontend-grupo14-arqui.tk",
        "http://localhost",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=[])
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)    
background_task_started = False 


print('\n\n\n#######################\n')
print("RUNNING!!!")
print('\n#######################\n\n\n')

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

# ############## Users #######################

@sio.on('connect')
def connect(sid, environ):
    print("SE HA CONECTADO", sid)

@sio.on('join')
def join(sid, dataUser, *args):
    print('Se ha unido', sid)
    sio.enter_room(sid, dataUser['room'])
    print(dataUser)

@sio.on('sendMessage')
async def sendMessage(sid, dataUser, *args):
    print('Mensaje de', sid)
    print(dataUser)
    print(dataUser['room'])
    dataUser['time'] = datetime.now().strftime("%H:%M")
    await sio.emit('message', dataUser, room=dataUser['room'])

app.add_route("/socket.io/", route=socket_app, methods=['GET', 'POST'])
app.add_websocket_route("/socket.io/", socket_app)
##########################################3


@app.get("/users/")
async def get_users():
    results = db.session.query(models.User).all()
    return results


@app.post("/user/")
def create_user(user: schema.UserCreate):
    db_user = models.User(
        username=user.username
    )
    db.session.add(db_user)
    db.session.commit()
    return {"message": 'ok'}
# ###########################################


# ############## Messages #######################
@app.get("/messages/")
def get_messages(userId: int, receptorId: int):
    results = db.session.query(models.Message).filter(or_(models.Message.userId==userId, models.Message.userId==receptorId)).filter(or_(models.Message.receptorId==userId, models.Message.receptorId==receptorId)).order_by(models.Message.time).all()
    for model in results:
        model.send_at = model.time.strftime("%H:%M")
        model.user = db.session.query(models.User).filter(models.User.id == model.userId).first()
    return results


@app.post("/message/")
async def post_messages(message: schema.MessageCreate):
    # host = request.base_url
    if message.body[:7] == "/excuse":
        # Generates a random excuse
        excuses = ["tengo el cumpleaños de mi abuela", "tengo que estudiar",
                   "estuve con alguien con COVID", "no me dejaron", "no he dormido nada esta semana"]
        excuse = excuses[random.randint(0,4)]
        message.body = f'Pucha, no voy a poder porque {excuse}'
    db_message = models.Message(
        body=message.body,
        userId=message.userId,
        receptorId=message.receptorId,
        time=datetime.now()
    )
    db.session.add(db_message)
    db.session.commit()
    messages = get_messages(message.userId, message.receptorId)
    return messages


@app.post("/new_group/")
async def new_group(new_group: schema.GroupCreate):
    db_group = models.Group(name=new_group.name)
    db.session.add(db_group)
    db.session.commit()
    group = db.session.query(models.Group).order_by(models.Group.id.desc()).first()
    for member in new_group.users:
        user = db.session.query(models.User).filter(models.User.id==member).first()
        user.groups.append(group)
        db.session.add(user)
        db.session.commit()
    user = db.session.query(models.User).filter(models.User.id==new_group.userId).first()
    user.groups.append(group)
    db.session.add(user)
    db.session.commit()
    return {'groupId': group.id, 'name': group.name}

@app.get('/groups/')
def get_groups(userId: int):
    user = db.session.query(models.User).filter(models.User.id==userId).first()
    groups = db.session.query(models.Group).filter(models.Group.users.contains(user)).all()
    return groups

@app.post('/groupMessage/')
async def group(message: schema.GroupMessageCreate):
    user = db.session.query(models.User).filter(models.User.username==message.username).first()
    group = db.session.query(models.Group).filter(models.Group.id==int(message.groupId)).first()
    body = message.body
    body_ls = body.split(" ")
    for word in body_ls:
        if word[0] == "@":
            to_notify = word[1:]
            notified_user = db.session.query(models.User).filter(models.User.username==to_notify).first()
            print(notified_user)
            if notified_user:
                db_notification = models.Notification(
                    message=body,
                    groupId=group.id,
                    notifiedUser=notified_user.id
                )
                db.session.add(db_notification)
                db.session.commit()
                # EL USUARIO PUEDE VER LA NOTIFICACIÓN EN SU PERFIL
                # AQUÍ SE MANDA LA NOTIFICACIÓN A TRAVÉS DE UN SISTEMA
                async with httpx.AsyncClient() as client:
                    resp = await client.get('https://nysgme96oe.execute-api.us-east-2.amazonaws.com/default/NotificationSystem')
                if resp.status_code == 200:
                    print('El servicio de envío de notificaciones está procesando la notificación')
                else:
                    print('El servicio de envío de notificaciones no pudo procesar la solicitud')
    if body[:5] == "/add ":
        # Add users to group
        users_to_add = body.split(" ")[1:]
        for new_username in users_to_add:
            new = db.session.query(models.User).filter(models.User.username==new_username).first()
            new.groups.append(group)
            db.session.add(new)
            db.session.commit()
        body = f"Ha agregado al grupo a: {', '.join(users_to_add)}"
    elif body[:6] == "/name ":
        # Change group name
        new_name = body[6:]
        group.name = new_name
        db.session.add(group)
        db.session.commit()
        body = f'Ha cambiado el nombre del grupo a: {new_name}'
    elif body[:7] == "/excuse":
        # Generates a random excuse
        excuses = ["tengo el cumpleaños de mi abuela", "tengo que estudiar",
                   "estuve con alguien con COVID", "no me dejaron", "no he dormido nada esta semana"]
        excuse = excuses[random.randint(0,4)]
        body = f'Pucha, no voy a poder porque {excuse}'
    db_message = models.GroupMessage(
        body=body,
        user_username=user.username,
        groupId=group.id,
        time=datetime.now()
    )
    db.session.add(db_message)
    db.session.commit()
    return get_group_messages(group)

@app.get('/groupMessages/')
def get_group_messages(group):
    messages = db.session.query(models.GroupMessage).filter(models.GroupMessage.groupId==group.id).all()
    for m in messages:
        m.send_at = m.time.strftime("%H:%M")
    return messages

@app.get('/notifications/')
def get_notifications(userId: int):
    notifications = db.session.query(models.Notification).filter(models.Notification.notifiedUser==userId).all()
    return notifications


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
