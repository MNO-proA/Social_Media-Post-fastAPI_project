from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr



#Pydantic Model
# User sending data to us
class PostBase(BaseModel):
  """This is the schema for the payload in the browser. When the user fills an input form, the data is matched to this schema on the server side to validate the information coming in as data(request.POST), this is called SERVER SIDE VALIDATION
  FRONT END
  <input type='text' name='title'/>
  <input type='text' name='content'/>
  <input type='checkbox' name='published' value='true'/>
  
  BACK END => Broswer, inspect, networks, payload
  (THE NAME OF THE MODEL)post:{
    TITLE: str (frontend input content for title),
    CONTENT: str (frontend input content for content)
    PUBLISHED: bool (frontend input content for published)
  }"""
  title: str
  content: str
  published: bool = True

  """Schema/Pydantic Models define the structure of a request and response ('Agreement/law all must abide'). This ensure that when a user wants to create a post, the request will only go through if it has a 'title' and 'content' in the body. Pydantic performs validation to make sure that all the needed requirements are satisfied (all the data fields including data types in the request match up to what we want) mainly making sure request and response are shaped in a specific way"""

"""Resquest Schema for POST"""
class PostCreate(PostBase):
    pass

"""Response Schema for USER"""
class User(BaseModel):
  id: int
  email: EmailStr
  created_at: datetime

  class Config:
    orm_mode = True

"""Response Schema"""
class Post(PostBase):
  # other attributes inherited from the Postbase Model
  created_at: datetime
  owner_id:int
  owner:User #refering to the response schema for user, so as to embed user details in the response for a post (in models, owner = relationship(User))

  class Config:
    orm_mode = True


"""Resquest Schema for USER"""
class BaseUsers(BaseModel):
  email: EmailStr
  password: str


class CreateUsers(BaseUsers):
  pass


    

"""Resquest Schema for LOGIN"""
class UserLogin(BaseModel):
  email:EmailStr
  password:str


  """Schema for Token"""
class Token(BaseModel):
  access_token:str
  token_type:str

class TokenData(BaseModel):
  id:Optional[str] = None
