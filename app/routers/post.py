from typing import List
from fastapi import Body, FastAPI, status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import SessionLocal, get_db
from .. import models, schemas

router = APIRouter(
  prefix="/posts",
  tags=["Posts"]
)


"""********************************************"""
"""Path Operations for Posts"""
"""********************************************"""

#CREATE
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.Post)
def create_post(post : schemas.PostCreate, db: Session = Depends(get_db)):
  # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """,(post.title, post.content, post.published)) #Parameterized Query or Sanitized Query(Query Parameterization) =  against SQL Injections
  # new_post = cursor.fetchone()
  # conn.commit()

  """SQLALCHEMY"""
  # new_post = models.Post(title=post.title, content=post.content, published=post.published) Key=value <= **dict()
  new_post = models.Post(**post.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post



#READ
@router.get("/", response_model=List[schemas.Post])
def root(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts



#READ BY ID
@router.get("/{id}", response_model= schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
  # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, str(id))
  # post = cursor.fetchone()
  post = db.query(models.Post).filter(models.Post.id == id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"details NOT FOUND!")
  return post 


#UPDATE
@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int, updated_post:schemas.PostCreate, db: Session = Depends(get_db)):
  # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
  # updated_post = cursor.fetchone()
  post_query = db.query(models.Post).filter(models.Post.id == id)
  post = post_query.first()
  if post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"details NOT FOUND!") 
  post_query.update(updated_post.dict())
  db.commit()
  return post_query.first()


#DELETE BY ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
  # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, str(id))
  # deleted_post = cursor.fetchone()
  delete_post = db.query(models.Post).filter(models.Post.id == id)
  
  if delete_post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"details NOT FOUND!") 
  
  delete_post.delete()
  db.commit()
  # return Response(status_code=status.HTTP_204_NO_CONTENT)