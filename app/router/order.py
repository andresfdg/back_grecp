from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import *
from ..models.ecommerceModels import *
from ..schemas import *
from ..oauth2 import *
from typing import List


#routers
router = APIRouter()

#create a order an asigned to a gremio

@router.post("/create_new_order")
def create_new_order(payload:OrderCreation,db:Session = Depends(get_db),current_user: int = Depends(get_user)):

    order_item = db.query(ItemDb).filter(ItemDb.id == payload.item).first()
        
    popularity = order_item.actual_popularity

    dicount = 0
    pop = 0

    if popularity == 'low':
        dicount = order_item.discount_low
        pop =  order_item.quantity_low
    if popularity == 'medium':
        dicount = order_item.discount_medium
        pop =  order_item.quantity_medium
    if popularity == 'high':
        dicount = order_item.discount_high
        pop =  order_item.quantity_high 

    gremio_validado = db.query(GuildDb).filter(GuildDb.item == payload.item)

    

    #this if is use to comprobate if a gremio exist for the order product
    if not gremio_validado.first():
        gremio = GuildDb(item = payload.item, pop_max=pop )
        db.add(gremio)
        db.commit()
        db.refresh(gremio)
      

        new_post = OrderDb(store_id=order_item.owner_store, discount=dicount ,owner_id=current_user.id,gield_id=gremio.id  ,**payload.dict()) 

    #if the gremio exist increment the order_number     
    else:   #gre = gremio in database
        gremio_exist = db.query(GuildDb).filter(GuildDb.item == order_item.id).filter(GuildDb.active == True).first()
        if not gremio_exist:
            gremio = GuildDb(item = payload.item , pop_max=pop)
            db.add(gremio)
            db.commit()
            db.refresh(gremio)
            new_post = OrderDb(store_id=order_item.owner_store, discount=dicount ,owner_id=current_user.id,gield_id=gremio.id  ,**payload.dict()) 
        else:
            
            cur.execute(f"""SELECT SUM(quantity) FROM orders WHERE orders.gield_id = {str(gremio_exist.id)}""")
            actual_quantity = cur.fetchone()
            actual_quantity = list(actual_quantity.items())
            print(actual_quantity[0][1] + payload.quantity)
            if(actual_quantity[0][1] + payload.quantity > gremio_exist.pop_max):
                 raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
            elif(actual_quantity[0][1] + payload.quantity < gremio_exist.pop_max):
                gremio_exist.order_number = gremio_exist.order_number + 1
                new_post = OrderDb(store_id=order_item.owner_store, discount=dicount ,owner_id=current_user.id,gield_id=gremio_exist.id  ,**payload.dict()) 
            else:
                gremio_exist.active = False
                gremio_exist.order_number = gremio_exist.order_number + 1
                new_post = OrderDb(store_id=order_item.owner_store, discount=dicount ,owner_id=current_user.id,gield_id=gremio_exist.id  ,**payload.dict())    
                
       
        #x = gremio_validado.first()    
        #x.order_number = x.order_number + 1
        #new_post = OrderDb(owner_id=current_user.id,gield_id=x.id  ,**payload.dict())
         
    #new order created
        
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# get all orders
@router.get("/all_orders")                
def get_all_orders(db:Session = Depends(get_db)):

    orders = db.query(OrderDb).all()
    return orders

#get how many items were buy by all users
@router.get("/total_quantity_item/{id}")
def total_quantity_item(id:int, db:Session = Depends(get_db)):

    cur.execute(f"  SELECT SUM(quantity) FROM orders WHERE item ={str(id)} ")
    count = cur.fetchone()

    return count


#get how many orders exist for a consulted item 
@router.get("/totalitem/{id}")
def total(id:int, db:Session = Depends(get_db)):

    cur.execute(f"  SELECT COUNT(item) FROM orders WHERE item ={str(id)} ")
    count = cur.fetchone()

    return count


@router.get("/prueba/{id}")
def prueba(id:int):

    cur.execute(f"""SELECT * FROM users """)
    user =  cur.fetchall()
    return user
    
#RETURN ALL GIELD AND THEIR ORDERS
@router.get("/join")
def prueba():

    cur.execute(f""" SELECT * FROM orders LEFT JOIN numericalguiel ON orders.gield_id = numericalguiel.id ORDER BY numericalguiel.id """)
    orders = cur.fetchall()

    return orders


@router.get("/userorders")
def get_user_orders(db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    orders = db.query(OrderDb).filter(OrderDb.owner_id == current_user.id).all()



    return orders

    


 

