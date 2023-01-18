from fastapi import APIRouter, Depends , status , HTTPException
from sqlalchemy.orm import Session
from ..database import *
from ..models.user import *
from ..models.ecommerceModels import *
from ..schemas import *
from ..oauth2 import *
from typing import List



router = APIRouter()

#create a new store
@router.post("/store/create")
def create_item(payload:StoreCreate, db:Session = Depends(get_db), current_user: int = Depends(get_user)):
    print(current_user.type)

    valide_store = db.query(StoreDb).filter(StoreDb.owner == current_user.id).first()
    print(current_user.id)
    if valide_store:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE ,detail=f'cuantas tiendas quieres care verga? ya tienes una!')

    if  current_user.type == 'Store':
        new_store = StoreDb(owner=current_user.id,**payload.dict())
        db.add(new_store)
        db.commit()
        db.refresh(new_store)
        print(new_store)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'NO PUEDES METER ESA MONDA')       

    return new_store 
#---------------------------------------------------------------------------------------
# get all stores
@router.get("/allstore")               
def get_store(db:Session = Depends(get_db)):
    #get all users registered in the dataset

    stores = db.query(StoreDb).all()
    
    return stores


@router.get("/onestore")
def onestore(db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    store = db.query(StoreDb).filter(StoreDb.id == current_user.id).first()

    return store


@router.get("/allstore")
def get_all_store(db:Session = Depends(get_db), current_user: int = Depends(get_user)):


    stores = db.query(StoreDb).all()

    return stores

@router.get("/allstore/{id}")
def get_all_store(id:int,db:Session = Depends(get_db), current_user: int = Depends(get_user)):


    store = db.query(StoreDb).filter(StoreDb.id == id).first()

    return store

@router.get("/storeitems/{id}")
def get_all_store_items(id:int,db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    items = db.query(ItemDb).filter(ItemDb.owner_store == id ).all()
    
    


    return items   

@router.get("/storeorder")
def get_current_store_order(db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    cur.execute(f"""SELECT numericalguiel.item, orders.gield_id,numericalguiel.pop_max,numericalguiel.active, numericalguiel.order_number, items.name, items.price FROM orders LEFT JOIN numericalguiel ON orders.gield_id = numericalguiel.id LEFT JOIN items ON numericalguiel.item = items.id  WHERE orders.owner_id = {str(current_user.id)}""")
    orders = cur.fetchall()
    return orders

@router.get("/storeord")
def store_orders(db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    cur.execute(f"""SELECT orders.item,orders.gield_id, orders.quantity, items.name, items.price FROM orders LEFT JOIN items ON orders.item = items.id LEFT JOIN users ON orders.owner_id = users.id  WHERE orders.store_id = {str(current_user.id)}""")
    orders = cur.fetchall()


    return orders


@router.get("/storegield")
def store_gield(db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    cur.execute(f"""SELECT orders.item,orders.gield_id,items.name,items.price,items.discount_low,items.discount_medium,items.discount_high, SUM(orders.quantity) as totalq, COUNT(*) as total_ord   FROM orders  LEFT JOIN items ON orders.item = items.id LEFT JOIN users ON orders.owner_id = users.id WHERE orders.store_id = {str(current_user.id)}  GROUP BY orders.item,orders.gield_id,items.name,items.price,items.discount_low,items.discount_medium,items.discount_high""")
    gields = cur.fetchall()
    return gields


@router.get("/storegieldorder/{id}")
def storegieldorder(id:int,db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    cur.execute(f"""SELECT item,quantity,discount,name,email,phone, city,adress FROM orders LEFT JOIN users ON orders.owner_id = users.id   WHERE orders.gield_id = {str(id)} """)
    users = cur.fetchall()
    return users





@router.get("/availability/{id}")
def get_all_store_items(id:int,db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    

    guild = db.query(GuildDb).filter(GuildDb.item == id).filter(GuildDb.active == True).first()
   
    print(guild)
    item = db.query(ItemDb).filter(ItemDb.id == id).first()
    avalibility = 0

    if not guild:
        
        popularity = item.actual_popularity 
        
        if popularity == 'low':
            avalibility = item.quantity_low
        elif popularity == 'medium':
            avalibility = item.quantity_medium
        else:
            avalibility = item.quantity_high
    else:
         cur.execute(f"""SELECT SUM(quantity) FROM orders WHERE orders.gield_id = {str(guild.id)}""")
         actual_quantity = cur.fetchone()
         actual_quantity = list(actual_quantity.items())
         
         max_quantity = guild.pop_max
         avalibility = max_quantity - actual_quantity[0][1]
         
         print(avalibility)  
              


                    

    
    
    return avalibility


