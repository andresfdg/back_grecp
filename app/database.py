from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2 
from psycopg2.extras import RealDictCursor

#database conection
conn = psycopg2.connect(host='ec2-3-209-124-113.compute-1.amazonaws.com',database='d75mds7f270q2n',port='5432', user='knctyimjqmxfhx',password='13188ab683d7b133ec193c07d5f0f161c72fb10d0ec0032f2bf5581863b7c85b', cursor_factory=RealDictCursor)
cur = conn.cursor()
SQLALCHEMY_DATABASE_URL = "postgresql://knctyimjqmxfhx:13188ab683d7b133ec193c07d5f0f161c72fb10d0ec0032f2bf5581863b7c85b@ec2-3-209-124-113.compute-1.amazonaws.com/d75mds7f270q2n"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


        