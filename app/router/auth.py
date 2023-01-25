from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import *
from ..models.user import *
from ..schemas import *
from ..oauth2 import *

router = APIRouter(

tags=["Auth"]

)

#allows the user to login
@router.post('/login')
def login(payload:Login ,db:Session = Depends(get_db)):
    #looks for the user in the dataset
    if payload.type == 'Person':
        user = db.query(UserDb).filter(UserDb.email == payload.email).first()
    else:
        user = db.query(StoreUserDb).filter(StoreUserDb.email == payload.email).first()    

    #if the user not exist raise an error
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
    #if the user exist create a token for the user
    token = create_access_token(data={"user_id":user.id,"type":user.type})    

    return token
