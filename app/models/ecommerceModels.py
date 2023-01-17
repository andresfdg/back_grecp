from sqlalchemy import Column, Integer, String, Boolean, ForeignKey , Float
from ..database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship 

class OrderDb(Base):
    __tablename__="orders"

    id = Column(Integer, primary_key = True, nullable=False)
    item = Column(Integer, ForeignKey('items.id'))
    quantity = Column(Integer, nullable = False )
    discount = Column(Integer, nullable = False )
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable = False)
    owner = relationship('UserDb')
    gield_id = Column(Integer,  ForeignKey('numericalguiel.id'))
    store_id = Column(Integer,  ForeignKey('stores.id'))
    active = Column(Boolean, server_default='True',nullable = False)
    start_date = Column(TIMESTAMP(timezone=True),nullable=False,server_default = text('now()'))
     
class ItemDb(Base):
    __tablename__="items"

    id = Column(Integer , primary_key = True, nullable=False )
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    owner_store = Column(Integer,  ForeignKey('stores.id'))
    price = Column(Integer, nullable = False)
    actual_popularity = Column(String, nullable = False)
    discount_low=Column(Integer, nullable = False)
    discount_medium=Column(Integer, nullable = False)
    discount_high=Column(Integer, nullable = False)
    quantity_low=Column(Integer, nullable = False , server_default='10') #pop --- population
    quantity_medium=Column(Integer, nullable = False, server_default='20') #pop --- population
    quantity_high=Column(Integer, nullable = False, server_default='30') #pop --- population

class GuildDb(Base):
    __tablename__="numericalguiel"

    id = Column(Integer, primary_key = True, nullable=False)
    date = Column(TIMESTAMP(timezone=True),nullable=False,server_default = text('now()'))
    active = Column(Boolean, server_default='True',nullable = False)
    item = Column(Integer, ForeignKey('items.id'))
    order_number = Column(Integer, server_default= '1' )
    pop_max = Column(Integer, server_default= '0')
    discount = Column(Integer, server_default= '0')
 
class StoreDb(Base):
    __tablename__="stores"

    id = Column(Integer, primary_key = True, nullable=False)
    name = Column(String, nullable=False)
    date = Column(TIMESTAMP(timezone=True),nullable=False,server_default = text('now()'))
    active = Column(Boolean, server_default='False',nullable = False)
    owner = Column(Integer,  ForeignKey('store_users.id'))
    
    


    


