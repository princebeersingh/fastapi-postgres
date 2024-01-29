from fastapi import FastAPI,Response,status,HTTPException,Depends

from fastapi.params import Body
from utils import hashin
import psycopg2
from typing import Optional,List
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
import time
import models,schemas,utils
from database import engine,get_db

models.Base.metadata.create_all(bind=engine)

#  for increasing the efficiency of the database





app=FastAPI()
# schema of users  =>
# title str content str category bool published 
# object relational mappers => we doesnt connect database directly by sql  we use python as middle man


while True:
    try:
      conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='postgres',cursor_factory=RealDictCursor)
      cursor=conn.cursor()
      print("database connected successfully")
      break
    except Exception as error:
      print("connection to database failed")
      print("Error",error)
      time.sleep(2)



# here orm starts 

@app.get("/")
async def root():
  return {"message":"hello"}

# my_posts=[{"title":"beaw","content":"fhv","id":"1"},{"title":"world","content":"fhvgujj","id":"5"},{"title":"hello","content":"ffffffffffhv","id":"4"}]

# @app.get("/sqlalchemy")
# def test_posts(db:Session=Depends(get_db)):                        only for learning not needed so far
#   posts=db.query(models.Post).all()
#   return {"data":posts}



@app.get("/posts",response_model=List[schemas.Post])
def get_posts(db:Session=Depends(get_db)):
  posts=db.query(models.Post).all()
  return posts


@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db:Session=Depends(get_db)):
  # post.dict()
  # cursor.execute(f"INSERT INTO posts (title,content,published) VALUES ({post.title,post.content,post.published})") wrong way can bee hacked 
  # cursor.execute("""INSERT INTO posts (title ,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
  # new_post=cursor.fetchone()
  # conn.commit()
  # new_post=models.Post(title=post.title,content=post.content,published=post.published)   ******lengthy process***
  new_post=models.Post(**post.dict())  #dict method easy to add new feature to the schema
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post





# @app.get("/posts/{id}")
# def get_post(db:Session=Depends(get_db)):
#   posts=db.query(models.Post).all()
# #   cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
# #   post=cursor.fetchone()
  # if not post:
  #   raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} was not found")
  # return {"data":posts}



#  handling code for single query in database

@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id:int,db:Session=Depends(get_db)):
  post=db.query(models.Post).filter(models.Post.id==id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} was not found")
  return post





# @app.delete("/posts/{id}")
# def delete_post(id:int):
#   cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING *""",(str(id),))
#   deleted_post=cursor.fetchone()
#   conn.commit()                                                                             for sql query method
#   if  not deleted_post:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} doesn`t exist")
#   return Response(status_code=status.HTTP_204_NO_CONTENT)

# for sqlalchemy method


@app.delete("/posts/{id}",response_model=schemas.Post)
def delete_post(id:int,db:Session=Depends(get_db)):
  posts=db.query(models.Post).filter(models.Post.id==id)
  if  not posts.first():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} doesn`t exist")
  posts.delete()#syncronize_session=False
  db.commit()
  return Response(status_code=status.HTTP_204_NO_CONTENT)





# old sql query method to update posts

# @app.put("/posts/{id}")
# def update_post(id:int,post:Post):
#   cursor.execute("""UPDATE  posts  SET title=%s,content=%s ,published=%s WHERE id=%s RETURNING * """,
#                  (post.title,post.content,post.published,str(id),))
#   updated_post=cursor.fetchone()
#   conn.commit()
#   if not updated_post:
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id } doesnt exist")
#   return {"data":updated_post}


# sqlalchemy method of update post

@app.put("/posts/{id}")
def update_post(id:int,updated_post:schemas.PostCreate,db:Session=Depends(get_db)):
# in update post we basically create newpost and replace the post by newly created post
  query_posts=db.query(models.Post).filter(models.Post.id==id)
  post=query_posts.first()

  
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id } doesnt exist")
  

  query_posts.update(updated_post.dict(),synchronize_session=False)
  db.commit()
  # db.refresh()
  return query_posts.first()


# Here code for user schema not for posts schema

@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.CreateUser,db:Session=Depends(get_db)):

  #hash the passwd

  hashed_pwd=utils.hashin(user.password)
  user.password=hashed_pwd

  new_user=models.User(**user.dict())  #dict method easy to add new feature to the schema
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  
  return new_user



@app.get('/users/{id}',response_model=schemas.UserOut)
def get_user(id:int ,db:Session=Depends(get_db)):
  user=db.query(models.User).filter(models.User.id==id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id {id} doesn`t exists")
  

  return user

# new post by user
# login








