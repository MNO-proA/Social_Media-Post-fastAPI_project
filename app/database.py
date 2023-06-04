from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# python library for postgres (just like mysql connector for mysql)


# loop database connection code until connection is successful, this is to prevent the main code below from running if connection isn't successfull
# while True:
#   try:
#     conn = psycopg2.connect(host='localhost', database='fastAPI', user='postgres', password='pilato666', cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print("database connection was successful")
#     break
#   except Exception as error:
#     sleep(2)
#     print("connection to database failed")
#     print("Error: ", error)