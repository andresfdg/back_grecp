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
    #busca si el usuario tiene una tienda existente
    valide_store = db.query(StoreDb).filter(StoreDb.owner == current_user.id).first()
    print(current_user.id)
    #si el usuario tiene una tienda generamos una exepcion
    if valide_store:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE ,detail=f'No puedes generar mas de una tienda')
    #si el usuario es de tienda la creamos 
    if  current_user.type == 'Store':
        new_store = StoreDb(owner=current_user.id,**payload.dict())
        db.add(new_store)
        db.commit()
        db.refresh(new_store)
        print(new_store)
    #si el usuario no es de tienda hacemos una excepcion
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
#get the store asociated to the current user
@router.get("/onestore")
def onestore(db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    store = db.query(StoreDb).filter(StoreDb.id == current_user.id).first()

    return store

#get all the stores in the dataset
@router.get("/allstore")
def get_all_store(db:Session = Depends(get_db), current_user: int = Depends(get_user)):
    
    stores = db.query(StoreDb).all()
    
    return stores

#get a store using a specified id
@router.get("/allstore/{id}")
def get_all_store(id:int,db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    store = db.query(StoreDb).filter(StoreDb.id == id).first()
    
    return store

#print the items that have a store, and the avalability
@router.get("/storeitems/{id}")
def get_all_store_items(id:int,db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    #get the items of the store
    items = db.query(ItemDb).filter(ItemDb.owner_store == id ).all()
    #get the avilability 
    cur.execute(f""" SELECT items.id as item_id ,items.name, items.price, items.category, numericalguiel.id,(numericalguiel.quantity_max - SUM(orders.quantity)) as aval FROM orders LEFT JOIN numericalguiel ON orders.gield_id = numericalguiel.id LEFT JOIN items ON numericalguiel.item = items.id  WHERE numericalguiel.active = 'True' and items.owner_store ={str(id)} GROUP BY items.id, items.name, items.price, items.category,numericalguiel.id ORDER BY numericalguiel.id""")              
    availability = list(cur.fetchall())

    #save all the items in a new list
    lista = []
    for i in items:
        lista.append({"id":i.id,"name":i.name,"price":i.price,"category":i.category, "open":i.open})
    
    #assing the avilability to the correct item
    for i in lista:
        for j in availability:
            if i["id"] == j["item_id"]:
                i.update({"availability":j["aval"]})
               
    return lista   

#get all the orders that hace a store
@router.get("/storeorder")
def get_current_store_order(db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    cur.execute(f"""SELECT numericalguiel.item, orders.gield_id,numericalguiel.quantity_max,numericalguiel.active, numericalguiel.order_number, items.name, items.price FROM orders LEFT JOIN numericalguiel ON orders.gield_id = numericalguiel.id LEFT JOIN items ON numericalguiel.item = items.id  WHERE orders.owner_id = {str(current_user.id)}""")
    orders = cur.fetchall()
    return orders

###########???
@router.get("/storeord")
def store_orders(db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    cur.execute(f"""SELECT orders.item,orders.gield_id, orders.quantity, items.name, items.price FROM orders LEFT JOIN items ON orders.item = items.id LEFT JOIN users ON orders.owner_id = users.id  WHERE orders.store_id = {str(current_user.id)}""")
    orders = cur.fetchall()
    
    return orders

##############????
@router.get("/storegield")
def store_gield(db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    cur.execute(f"""SELECT orders.item,orders.gield_id,items.name,items.price,items.discount_low,items.discount_medium,numericalguiel.active,items.discount_high, SUM(orders.quantity) as totalq, COUNT(*) as total_ord   FROM orders  LEFT JOIN items ON orders.item = items.id LEFT JOIN users ON orders.owner_id = users.id LEFT JOIN numericalguiel ON numericalguiel.id = orders.gield_id   WHERE orders.store_id = {str(current_user.id)}  GROUP BY orders.item,orders.gield_id,items.name,items.price,items.discount_low,items.discount_medium,items.discount_high, numericalguiel.active""")
    gields = cur.fetchall()
    return gields

@router.get("/storegield2")
def store_gield(db:Session = Depends(get_db), current_user: int = Depends(get_user)):
    
    store = db.query(StoreDb).filter(StoreDb.owner== current_user.id).first()
    orders = db.query(OrderDb).filter(OrderDb.store_id == store.id).all()
    gremios = []
    guilds_id =[]
    counter = False
    
    
    for i in orders:
        for j in guilds_id:
            if i.gield_id == j:
                counter =True
                
        if counter==False: 
            guilds_id.append(i.gield_id)
            gremioact = db.query(GuildDb).filter(GuildDb.id == i.gield_id).first()
            itemact = db.query(ItemDb).filter(ItemDb.id == i.item).first()
            gremios.append({"name":itemact.name, "price":itemact.price,"id":gremioact.id, "total_ord":gremioact.order_number, "stade": gremioact.active})
        
        counter=False
        
    return gremios

################??
@router.get("/storegieldorder/{id}")
def storegieldorder(id:int,db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    cur.execute(f"""SELECT item,quantity,discount,name,email,phone,orders.id as id,orders.active, city,adress FROM orders LEFT JOIN users ON orders.owner_id = users.id   WHERE orders.gield_id = {str(id)} """)
    users = cur.fetchall()
    return users

################???
@router.get("/availability/{id}")
def get_all_store_items(id:int,db:Session = Depends(get_db), current_user: int = Depends(get_user)):


    #print(availability[0]["name"])
    #for i in lista:
     #   for j in availability:
      #      if j["name"] == i.name:
       #         i.update({"aval":j["sum"]})
        #    else:
         #       i.update({"aval":0})
    
    # print(items)
    
    #lista = []
    #for i in items:
     #   print(i.name)

    #for i in availability:
        
     #   i.update({"uno":1})
      #  lista.append(i)
    #print(lista)   
    return "lista"




@router.get("/items_store")
def stores_items(db:Session = Depends(get_db), current_user: int = Depends(get_user)):
    store = db.query(StoreDb).filter(StoreDb.owner == current_user.id).first()
    items = db.query(ItemDb).filter(ItemDb.owner_store == store.id).all()
    return items


@router.post("/send")
def send(payload:send, db:Session = Depends(get_db), current_user: int = Depends(get_user)):

    order = db.query(OrderDb).filter(OrderDb.id == payload.id).first()

    order.active = "send"

    db.commit()
    db.refresh(order)



    return "actualizado"

