from fastapi import APIRouter, Depends , status , HTTPException
from sqlalchemy.orm import Session
from ..database import *
from ..models.user import *
from ..models.ecommerceModels import *
from ..schemas import *
from ..oauth2 import *
from typing import List

#calls CryptContext and allows to create hash and incriptate data

router = APIRouter()

# create new user
@router.post("/item/create", response_model=ItemPrint)
def create_item(payload:CreateItem, db:Session = Depends(get_db), current_user: int = Depends(get_user)):
    #create a hash for the password

    store = db.query(StoreDb).filter(StoreDb.owner == current_user.id).first()
    #create a user using the payload information
    print(current_user.type)
    if  current_user.type == 'Store':
        new_item = ItemDb(owner_store=store.id,**payload.dict())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'NO PUEDES METER ESA MONDA')       

    return new_item   
#---------------------------------------------------------------------------------------
# get all items
@router.get("/items",response_model=List[ItemPrint])               
def get_item(db:Session = Depends(get_db), current_user: int = Depends(get_user)):
    #get all users registered in the dataset
    items = db.query(ItemDb).filter(ItemDb.owner_store ==current_user.id ).all()
    
    return items


    