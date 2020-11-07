from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship, backref
from datetime import datetime


Base = declarative_base()
association_table = Table('association', Base.metadata,
    Column('userId', Integer, ForeignKey('user.id')),
    Column('groupId', Integer, ForeignKey('group.id'))
)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    messages = relationship("Message")
    notifications = relationship("Notification")
    groups = relationship(
        "Group",
        secondary=association_table,
        back_populates="users")


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    users = relationship(
        "User",
        secondary=association_table,
        back_populates="groups")


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey('user.id'))
    body = Column(String)
    time = Column(DateTime, default=datetime.now())
    receptorId = Column(Integer)


class GroupMessage(Base):
    __tablename__ = "group_message"
    id = Column(Integer, primary_key=True, index=True)
    user_username= Column(String)
    groupId = Column(Integer, ForeignKey('group.id'))
    body = Column(String)
    time = Column(DateTime, default=datetime.now())


class Notification(Base):
    __tablename__ = "notification"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    groupId = Column(Integer, ForeignKey('group.id'))
    notifiedUser = Column(Integer, ForeignKey('user.id'))
