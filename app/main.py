
from fastapi import Body, FastAPI, status, Response, HTTPException, Depends
from random import randint, randrange
from psycopg2.extras import RealDictCursor
from time import sleep
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
import psycopg2
from . routers import post, user, auth



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


# my_posts = [{
#     "title":"Favorite quote",
#     "content":"Necessity is the mother of all",
#     "id":1
# },
# {"title":"Favorite lang",
# "content": "Python",
# "id":2}]

# def find_post(id):
#   for obj in my_posts:
#       if id == obj['id']:
#         return obj

# def find_post_index(id):
#   for obj in my_posts:
#       if id == obj['id']:
#         return my_posts.index(obj)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}





