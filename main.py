from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import models
from database import engine,get_db
from routers import post,user

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






# Here code for user schema not for posts schema



# new post by user
# login






app.include_router(post.router)
app.include_router(user.router)




