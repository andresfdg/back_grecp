from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2 
from psycopg2.extras import RealDictCursor

#database conection
conn = psycopg2.connect(host='ec2-34-201-95-176.compute-1.amazonaws.com',database='dba7424k8vok5v',port='5432', user='ffkkeppylkfbeq',password='d6a693e56d0e924cfe1d49ef69b8fa69cc2dccd546c2f8156dc27d09fa9403f6', cursor_factory=RealDictCursor)
cur = conn.cursor()
SQLALCHEMY_DATABASE_URL = "postgresql://ffkkeppylkfbeq:d6a693e56d0e924cfe1d49ef69b8fa69cc2dccd546c2f8156dc27d09fa9403f6@ec2-34-201-95-176.compute-1.amazonaws.com/dba7424k8vok5v"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


        