from typing import List
from fastapi import Body, FastAPI, status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import SessionLocal, get_db
from .. import models, schemas, utils

router = APIRouter(
  prefix="/users",
  tags=["Users"]
)


"""********************************************"""
"""Path Operations Users"""
"""********************************************"""
#Create
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_users(user:schemas.CreateUsers, db: Session = Depends(get_db)):

  #hash the password of user - user.password
  hashed_password = utils.hash(user.password)
  user.password = hashed_password

  new_user = models.User(**user.dict())
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

#Read
@router.get("/", response_model=List[schemas.User])
def users(db: Session = Depends(get_db)):
  users = db.query(models.User).all()
  return users

# Read one
@router.get("/{id}", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id).first()

  if user == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User not found')
  return user

#update
@router.put("/{id}", response_model=schemas.User)
def update_users(id: int, updated_user:schemas.CreateUsers, db: Session = Depends(get_db)):
  user_query = db.query(models.User).filter(models.User.id == id)
  user = user_query.first()

  if user == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User not found')
  user_query.update(updated_user.dict())
  db.commit()
  return user_query.first()

#Delete
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
  deleted_user = db.query(models.User).filter(models.User.id == id)

  if deleted_user == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User not found')
  
  deleted_user.delete()
  db.commit()