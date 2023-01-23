from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import *
from ..models.ecommerceModels import *
from ..schemas import *
from ..oauth2 import *
from typing import List




router = APIRouter()

##############?
@router.get("/guieluser")
def gielduser(db:Session = Depends(get_db),current_user: int = Depends(get_user)):

    user_order = db.query(OrderDb).filter(OrderDb.owner == current_user.id).all()

    return "helo"


@router.get("/guielditem/{id}")
def guielitem(id:int,db:Session = Depends(get_db),current_user: int = Depends(get_user)):

    guielitems = db.query(GuildDb).filter(GuildDb.item == id).all()

    

    return guielitems


















