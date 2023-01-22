from pydantic import BaseModel
from typing import Optional

#------------------------------------------------users schemas ------------------------------------------------------------------------
#schema when you want to create a user info in the payload
class CreateUser(BaseModel): 
    #credential info                           
    name : str       
    email: str
    password : str
    #adress and aditional info
    phone : int
    birthdate : str
    city : str
    adress : str
 

class CreateStoreUser(BaseModel): 
    #credential info                           
    name : str       
    email: str
    password : str
    #adress and aditional info
    phone : int
    city : str
    adress : str
  

#schema when user is print in console
class UserPrint(BaseModel):
    name :str
    email:str
    
    class Config:
        orm_mode = True

#schema to login 
class Login(BaseModel):

    email: str
    password: str
    type : str
#--------------------------------------------------guild schemas -----------------------------------------------------------------------------------------
#schema when user want to create a order info in the payload
class StoreGuildCreation(BaseModel):
    item : int
    quantity_max : int
    life_time: int
    discount: int

class UserGuildCreation(BaseModel):
    item : int
    quantity : int
    quantity_max : int
    life_time: int
    
class InterGulid(BaseModel):
    guild_id: int
    quantity: int
    
    
#--------------------------------------------------items schemas -----------------------------------------------------------------------------------------
#schema to create an item
class CreateItem(BaseModel):
    name: str
    category: str
    price: int
    actual_popularity: str
    discount_low: int   
    discount_medium: int
    discount_high: int
    
class ItemPrint(BaseModel):
    id: int 
    name :str
    category: str
    owner_store: int
    price: int
    actual_popularity: str
    
    class Config:
        orm_mode = True

#--------------------------------------------------Orders schemas -----------------------------------------------------------------------------------------
#schema when user want to create a order info in the payload
class OrderCreation(BaseModel):
    item : int
    quantity : int
    

#schema to view Order information
class OrderOut(BaseModel):
    
    item : int     
    price: int
    owner_id: int 

    class Config:
        orm_mode = True
        
#-------------------------------------------------- token schema -----------------------------------------------------------------------------------------
class tokenData(BaseModel):
    id:Optional[str] = None


class StoreCreate(BaseModel):

    name:str
  



