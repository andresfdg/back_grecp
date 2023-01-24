from fastapi import APIRouter, Depends , status , HTTPException
from sqlalchemy.orm import Session
from ..database import *
from ..models.user import *
from ..models.ecommerceModels import *
from ..schemas import *
from ..oauth2 import *
from typing import List

router = APIRouter()

# create new item
@router.post("/item/create", response_model=ItemPrint)
def create_item(payload:CreateItem, db:Session = Depends(get_db), current_user: int = Depends(get_user)):
    
    #look for the store of the logged user
    store = db.query(StoreDb).filter(StoreDb.owner == current_user.id).first()
    
    #validate if the the current user is a store user
    if  current_user.type == 'Store':
        #if current user is a store user create a the new item using the payload information
        new_item = ItemDb(owner_store=store.id,**payload.dict())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        
    else:
        #if current user is not a store user raise an exception
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'NO PUEDES METER ESA MONDA')       

    return new_item

   
#--------------------------------------------------------------Get Functions------------------------------------------------------------------
# get all items in the data set
@router.get("/items",response_model=List[ItemPrint])               
def get_item(db:Session = Depends(get_db), current_user: int = Depends(get_user)):
    ##################?
    items = db.query(ItemDb).filter(ItemDb.owner_store ==current_user.id ).all()
    
    return items



@router.get("/item/{id}")
def get_item(id:int, db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    item = db.query(ItemDb).filter(ItemDb.id == id).first()

    return item




    