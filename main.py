from fastapi import FastAPI, Request, responses, templating, Form
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.encoders import jsonable_encoder
from datetime import timedelta
import uvicorn
import fastapi
import socketio
import os
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db
from views import web_app
from dotenv import load_dotenv
import models, schema
from schema import User
from datetime import datetime
import json
from starlette.responses import RedirectResponse
from typing import Optional, List
from sqlalchemy import or_
import random
from fastapi.middleware.cors import CORSMiddleware
import httpx
from fastapi_login import LoginManager


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
SECRET = "123"

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

################ Login Manager ###############

manager = LoginManager(SECRET, tokenUrl='/auth/token')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

@manager.user_loader
def load_user(email: str):  # could also be an asynchronous function
    user = db.session.query(models.User).filter(models.User.email.match(email))
    user = user.all()
    try:
        return user[0]
    except:
        return None

@app.post('/auth/token')
def login(user: schema.UserCreate):
    email = user.userName
    password = user.password
    user = load_user(email)  # we are using the same function to retrieve the user
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user.password:
        raise InvalidCredentialsException

    #expires after 365 days
    access_token = manager.create_access_token(
        data=dict(sub=email), expires_delta=timedelta(days=365)
    )

    return {'access_token': access_token, 'token_type': 'bearer', "user_id": user.id}

    # db.query(models.User).filter(models.User.email == email).first()
@app.post("/user/signup")
def create_user(user: schema.UserCreate):
    db_user = models.User(
        username=user.userName,
        password = user.password,
        email = user.email,
        admin = False
    )
    db.session.add(db_user)
    db.session.commit()
    access_token = manager.create_access_token(
        data=dict(sub=user.email), expires_delta=timedelta(days=365)
    )
    db.session.refresh(db_user)
    return {"message": 'ok', 'access_token': access_token, 'token_type': 'bearer', "user_id": db_user.id}

@app.post("/user/admin/signup")
def create_admin(user: schema.UserCreate):
    db_user = models.User(
        username=user.userName,
        password = user.password,
        email = user.email,
        admin = True
    )
    db.session.add(db_user)
    db.session.commit()
    access_token = manager.create_access_token(
        data=dict(sub=user.email), expires_delta=timedelta(days=365)
    )
    db.session.refresh(db_user)
    return {"message": 'ok', 'access_token': access_token, 'token_type': 'bearer', "user_id": db_user.id}


@app.get("/users/")
async def get_users():
    results = db.session.query(models.User).all()
    return results

# ###########################################


# ############## Messages #######################
@app.get("/messages/")
def get_messages(userId: int, receptorId: int, user=Depends(manager), token: str = Depends(oauth2_scheme)):
    results = db.session.query(models.Message).filter(or_(models.Message.userId==userId, models.Message.userId==receptorId)).filter(or_(models.Message.receptorId==userId, models.Message.receptorId==receptorId)).order_by(models.Message.time).all()
    for model in results:
        model.send_at = model.time.strftime("%H:%M")
        model.user = db.session.query(models.User).filter(models.User.id == model.userId).first()
    return results


@app.post("/message/")
async def post_messages(message: schema.MessageCreate, token: str = Depends(oauth2_scheme)):
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


@app.post("/new_group/{type_of_group}")
async def new_group(type_of_group: str, new_group: schema.GroupCreate, token: str = Depends(oauth2_scheme)):
    if type_of_group=="private":
        db_group = models.Group(name=new_group.name, private=True)
    else:
        db_group = models.Group(name=new_group.name, private=False)
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
def get_groups(userId: int, token: str = Depends(oauth2_scheme)):
    user = db.session.query(models.User).filter(models.User.id==userId).first()
    groups = db.session.query(models.Group).filter(models.Group.users.contains(user)).all()
    return groups

@app.post('/groupMessage/')
async def group(message: schema.GroupMessageCreate, token: str = Depends(oauth2_scheme)):
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
def get_group_messages(group, token: str = Depends(oauth2_scheme)):
    if type(group)==str:
        messages = db.session.query(models.GroupMessage).filter(models.GroupMessage.groupId==int(group)).all()
    else:
        messages = db.session.query(models.GroupMessage).filter(models.GroupMessage.groupId==group.id).all()
    for m in messages:
        m.send_at = m.time.strftime("%H:%M")
    return messages

@app.get('/notifications/')
def get_notifications(userId: int, token: str = Depends(oauth2_scheme)):
    notifications = db.session.query(models.Notification).filter(models.Notification.notifiedUser==userId).all()
    return notifications

########## CRUDS ADMIN ###################

@app.get('/admin/all-users/{user_id}')
def get_all_users_admin(user_id: int, token: str = Depends(oauth2_scheme)):
    user = db.session.query(models.User).filter(models.User.id==user_id).first()
    if user.admin:
        users = db.session.query(models.User).all()
        return {"message": 'ok', "users": users}
    return {"message": 'not admin'}

@app.post('/admin/create-user/{user_id}')
def create_user_admin(user: schema.UserCreate, user_id: int, token: str = Depends(oauth2_scheme)):
    user2 = db.session.query(models.User).filter(models.User.id==user_id).first()
    if user2.admin:
        db_user = models.User(
            username=user.userName,
            password = user.password,
            email = user.email,
            admin = False
        )
        db.session.add(db_user)
        db.session.commit()
        return {"message": 'ok'}
    return {"message": 'not admin'}

@app.patch('/admin/edit-user/{user_id}/{user_edit}')
def update_user_admin(user_edit: int, user_id: str, user: schema.UserCreate, token: str = Depends(oauth2_scheme)):
    user_admin = db.session.query(models.User).filter(models.User.id==user_id).first()
    user_edit1 = db.session.query(models.User).filter(models.User.id==user_edit).first()
    if user_admin.admin:
        user_edit1.email= user.email
        user_edit1.username = user.userName
        user_edit1.password = user.password
        db.session.commit()
        db.session.refresh(user_edit1)
        return {"message": 'ok'}
    return {"message": 'not admin'}

@app.delete('/admin/delete-user/{user_id}/{user_delete}')
def delete_user_admin(user_id: int, user_delete: int, token: str = Depends(oauth2_scheme)):
    user = db.session.query(models.User).filter(models.User.id==user_id).first()
    if user.admin:
        user_instance = db.session.query(models.User).filter(models.User.id==user_delete).first()
        db.session.delete(user_instance)
        db.session.commit()
        return {"message": 'ok'}
    return {"message": 'not admin'}

@app.get('/admin/all-groups/{user_id}')
def get_all_groups_admin(user_id: int, token: str = Depends(oauth2_scheme)):
    user = db.session.query(models.User).filter(models.User.id==user_id).first()
    if user.admin:
        groups = db.session.query(models.Group).all()
        return {"message": 'ok', "Groups": groups}
    return {"message": 'not admin'}

@app.delete('/admin/delete-group/{user_id}/{group_id}')
def delete_group_admin(user_id: int, group_id: int, token: str = Depends(oauth2_scheme)):
    user = db.session.query(models.User).filter(models.User.id==user_id).first()
    if user.admin:
        group_instance = db.session.query(models.Group).filter(models.Group.id==group_id).first()
        db.session.delete(group_instance)
        db.session.commit()
        return {"message": 'ok'}
    return {"message": 'not admin'}

@app.put('/admin/private-group/{user_id}/{group_id}')
def make_group_private_admin(user_id: int, group_id: int, token: str = Depends(oauth2_scheme)):
    user = db.session.query(models.User).filter(models.User.id==user_id).first()
    if user.admin:
        group_instance = db.session.query(models.Group).filter(models.Group.id==group_id).first()
        group_instance.private = True
        db.session.commit()
        db.session.refresh(group_instance)
        return {"message": 'ok'}
    return {"message": 'not admin'}

@app.put('/admin/public-group/{user_id}/{group_id}')
def make_group_public_admin(user_id: int, group_id: int, token: str = Depends(oauth2_scheme)):
    user = db.session.query(models.User).filter(models.User.id==user_id).first()
    if user.admin:
        group_instance = db.session.query(models.Group).filter(models.Group.id==group_id).first()
        group_instance.private = False
        db.session.commit()
        db.session.refresh(group_instance)
        return {"message": 'ok'}
    return {"message": 'not admin'}

@app.get('/admin/groupMessages/{user_id}/{group_id}')
def get_group_messages_admin(user_id: int, group_id: int, token: str = Depends(oauth2_scheme)):
    user = db.session.query(models.User).filter(models.User.id==user_id).first()
    if user.admin:
        messages = db.session.query(models.Message).filter(models.Group.id==group_id).all()
        for m in messages:
            m.send_at = m.time.strftime("%H:%M")
        return messages
    return {"message": 'not admin'}

@app.delete('/admin/groupMessages/delete/{user_id}/{message_id}')
def delete_group_messages_admin(user_id: int, message_id: int, token: str = Depends(oauth2_scheme)):
    user = db.session.query(models.User).filter(models.User.id==user_id).first()
    if user.admin:
        message_instance = db.session.query(models.Message).filter(models.Message.id==message_id).all()
        db.session.delete(message_instance)
        db.session.commit()
        return {"message": 'ok'}
    return {"message": 'not admin'}

@app.put('/admin/groupMessages/edit/{user_id}/{message_id}')
def edit_group_messages_admin(user_id: int, message_id: int, message: str, token: str = Depends(oauth2_scheme)):
    user = db.session.query(models.User).filter(models.User.id==user_id).first()
    if user.admin:
        message_instance = db.session.query(models.Message).filter(models.Message.id==message_id).first()
        message_instance.body = message
        db.session.commit()
        db.session.refresh(message_instance)
        return {"message": 'ok'}
    return {"message": 'not admin'}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
