from datetime import datetime
from pydantic import BaseModel,EmailStr  #pydentics email string
# from typing import Optional



class PostBase(BaseModel):
  title:str
  content:str
  published:bool=True

class PostCreate(PostBase):
  pass


class Post(PostBase):
  id:int
  created_at:datetime
  class config:   #to tell this sqlalqamy model is orm modal
    orm_mode=True

class CreateUser(BaseModel):
  email:EmailStr
  password:str

class UserOut(BaseModel):
  id:int
  email:EmailStr
  created_at:datetime
  class config:   #to tell this sqlalqamy model is orm modal
    orm_mode=True
