from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import database, schemas, models, utils, oauth2
from sqlalchemy.orm import Session


router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(user_credential: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(user_credential.email == models.User.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credential")


    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credential")
    
    access_token = oauth2.create_access_token(
        data={"user_id":user.id})
    return {"access_token": access_token, "token_type": "bearer"}
