from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import *
from ..models.ecommerceModels import *
from ..schemas import *
from ..oauth2 import *
from typing import List
import datetime


#routers
router = APIRouter()

#create a order an asigned to a gremio
@router.post("/create_new_order")
def create_new_order(payload:OrderCreation,db:Session = Depends(get_db),current_user: int = Depends(get_user)):
    #look for the item that the user is buying using yhe payload information
    order_item = db.query(ItemDb).filter(ItemDb.id == payload.item).first()
    #look for the actual popularity of an item
    popularity = order_item.actual_popularity
    #inicialice variables for dicount and guild population
    dicount = 0
    pop = 0
     
    #assing values to dicount and pop  
    if popularity == 'low':
        dicount = order_item.discount_low
        pop =  order_item.quantity_low
    if popularity == 'medium':
        dicount = order_item.discount_medium
        pop =  order_item.quantity_medium
    if popularity == 'high':
        dicount = order_item.discount_high
        pop =  order_item.quantity_high
         
    #look if there is a exitent guield for the current item
    gremio_validado = db.query(GuildDb).filter(GuildDb.item == payload.item)
  
    #this happen is there is no a guield
    if not gremio_validado.first():
        #create a new gield
        gremio = GuildDb(item = payload.item, quantity_max=pop )
        db.add(gremio)
        db.commit()
        db.refresh(gremio)

        new_post = OrderDb(store_id=order_item.owner_store, discount=dicount ,owner_id=current_user.id,gield_id=gremio.id  ,**payload.dict()) 

    #if the gremio exist increment the order_number     
    else:   #gre = gremio in database
        gremio_exist = db.query(GuildDb).filter(GuildDb.item == order_item.id).filter(GuildDb.active == 'True').first()
        if not gremio_exist:
            gremio = GuildDb(item = payload.item , quantity_max=pop)
            db.add(gremio)
            db.commit()
            db.refresh(gremio)
            new_post = OrderDb(store_id=order_item.owner_store, discount=dicount ,owner_id=current_user.id,gield_id=gremio.id  ,**payload.dict()) 
        else:
            
            cur.execute(f"""SELECT SUM(quantity) FROM orders WHERE orders.gield_id = {str(gremio_exist.id)}""")
            actual_quantity = cur.fetchone()
            actual_quantity = list(actual_quantity.items())
            print(actual_quantity[0][1] + payload.quantity)
            if(actual_quantity[0][1] + payload.quantity > gremio_exist.quantity_max):
                 raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
            elif(actual_quantity[0][1] + payload.quantity < gremio_exist.quantity_max):
                gremio_exist.order_number = gremio_exist.order_number + 1
                new_post = OrderDb(store_id=order_item.owner_store, discount=dicount ,owner_id=current_user.id,gield_id=gremio_exist.id  ,**payload.dict()) 
            else:
                gremio_exist.active = 'False'
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

#allows store user to create their own guilds
@router.post("/store_create_new_guild")
def store_create_new_guild(payload:StoreGuildCreation,db:Session = Depends(get_db),current_user: int = Depends(get_user)):
    
    gremio = GuildDb(item = payload.item, quantity_max=payload.quantity_max, life_time= payload.life_time, order_number=0, discount = payload.discount)
    db.add(gremio)
    db.commit()
    db.refresh(gremio)
    
    return gremio

#allows person user to create their own guilds
@router.post("/user_create_new_guild")
def user_create_new_guild(payload:UserGuildCreation,db:Session = Depends(get_db),current_user: int = Depends(get_user)):
    #look for the item that the user is buying using yhe payload information
    order_item = db.query(ItemDb).filter(ItemDb.id == payload.item).first()
    user = db.query(UserDb).filter(UserDb.id == current_user.id).first()
    #inicialice variables for dicount and guild population
    dicount=0 #discount of the order
    time=0 # life time of the guild
    
    if (payload.quantity_max >= payload.quantity) and (user.active_guilds <= 5):
        user.active_guilds = user.active_guilds + 1
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="You can't have more guilds, or too much quantity")
    
    if payload.quantity_max == order_item.quantity_low:
        dicount = order_item.discount_low
        time = order_item.time_guild_low
    elif payload.quantity_max == order_item.quantity_medium:
        dicount = order_item.discount_medium
        time = order_item.time_guild_medium
    elif payload.quantity_max == order_item.quantity_high:
        dicount = order_item.discount_high
        time = order_item.time_guild_high
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Not an acceptable quantity")
        
    totalcostc = (order_item.price-(order_item.price*(dicount/100)))*payload.quantity #total cost of the order
    gremio = GuildDb(item = payload.item , quantity_max=payload.quantity_max, life_time= time, actual_quantity=payload.quantity, discount=dicount)
    
    new_post = ""
    
    if gremio.actual_quantity == gremio.quantity_max:
        gremio.active = "In process"
        user.active_guilds = user.active_guilds - 1
        db.add(gremio)
        db.commit()
        db.refresh(gremio)
        new_post = OrderDb(store_id=order_item.owner_store, discount=dicount ,owner_id=current_user.id,gield_id=gremio.id,totalcost=totalcostc, item=payload.item, quantity = payload.quantity, active="In process")
    else:
        db.add(gremio)
        db.commit()
        db.refresh(gremio)
        new_post = OrderDb(store_id=order_item.owner_store, discount=dicount ,owner_id=current_user.id,gield_id=gremio.id,totalcost=totalcostc, item=payload.item, quantity = payload.quantity)
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.post("/user_inter_guild")
def user_inter_guild(payload:InterGulid,db:Session = Depends(get_db),current_user: int = Depends(get_user)):
    #look for the item that the user is buying using yhe payload information
    request_guild= db.query(GuildDb).filter(GuildDb.id==payload.guild_id).first()
    order_item = db.query(ItemDb).filter(ItemDb.id == request_guild.item).first()
    #inicialice variables for dicount and guild population
    user = db.query(UserDb).filter(UserDb.id == current_user.id).first()
    
    #verify if quantity is acceptable
    date_1 = request_guild.date
    end_date = date_1 + datetime.timedelta(days=request_guild.life_time)
    print("creation: " + str(date_1))
    print("end: " + str(end_date))
    
    if end_date <= datetime.datetime.now(end_date.tzinfo):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Guild is deprecated')
    
    if (request_guild.quantity_max >= (request_guild.actual_quantity + payload.quantity)):
        user.active_guilds = user.active_guilds + 1
        request_guild.actual_quantity = request_guild.actual_quantity + payload.quantity
        request_guild.order_number = request_guild.order_number + 1
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='User can not create more guilds or orders')
        
    totalcostc = (order_item.price-(order_item.price*(request_guild.discount/100)))*payload.quantity #total cost of the order
    
    new_post = OrderDb(store_id=order_item.owner_store, discount=request_guild.discount, owner_id=current_user.id,gield_id=request_guild.id,totalcost=totalcostc, item=order_item.id, quantity = payload.quantity)
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    if request_guild.actual_quantity == request_guild.quantity_max:
        request_guild.active = "In process"
        orders= db.query(OrderDb).filter(OrderDb.gield_id==request_guild.id).all()
        for i in orders: 
            i.active = "In process"
            user = db.query(UserDb).filter(UserDb.id == i.owner_id).first()
            user.active_guilds = user.active_guilds - 1 
    
    db.commit()
    db.refresh(new_post)
   
    return new_post

@router.post("/send_order")
def total(id:str, db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    order=id

    return order

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

##################?
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

    


 

