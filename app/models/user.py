from sqlalchemy import Column, Integer, String, Boolean
from ..database import Base


class UserDb(Base):

    __tablename__ = "users"
    #credential info
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    #adress and aditional info
    phone = Column(Integer, nullable=False)
    birthdate = Column(String, nullable=False)
    city = Column(String, nullable=False)
    adress = Column(String, nullable=False)
    favorite_store = Column(String)
    favorite_item = Column(String)
    type = Column(String,server_default='Person', nullable=False)
    #guild information
    active_guilds = Column(Integer, server_default= '0')

class StoreUserDb(Base):

    __tablename__ = "store_users"
    #credential info
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    #adress and aditional info
    phone = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    adress = Column(String, nullable=False)
    type = Column(String ,server_default='Store', nullable=False)
