from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from app import models, schemas, database


# to get a string like this run:
# openssl rand -hex 32 (use a bash terminal)
SECRET_KEY = "8232eedbb90bf0ee4c028c705efafb06c261a014b889f57421a13668b43ea20d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #path for authentication (login without the "/")


def create_access_token(data: dict):
    to_encode = data.copy() # copy dict_data of the user that you want to embed in the token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # add time to utcnow to define expiring time
    to_encode.update({"exp": expire}) # python dic syntax to add expirint time to the copied dict_data
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #create a signature with the header(algo), userdata and secret key to be hashed
    return encoded_jwt # a hashed str containing header, userdata, secret password


def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #to decode the token from the user, the secret key and algo is used from the backend
        id: str = payload.get("user_id") # user data is extracted from the decoded token
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id) #user data is validated per the schema of the token (check data type, and data integrity)
    except JWTError:
        raise credentials_exception
    return token_data #return the user's data

#to get the current user, its depends on the token received from the login route, the password bearer (current_user) can be known from the token decoded
def get_current_user(token: str = Depends (oauth2_scheme), db: database.SessionLocal = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token =  verify_access_token(token, credentials_exception)
    
    user = db.query(models.User).filter(models.User.id == token.id).first()
    print(user.email)
    return user