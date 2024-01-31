from fastapi import Response,status,HTTPException,Depends,APIRouter
from typing import List
from sqlalchemy.orm import Session
from database import get_db
import schemas,models




router=APIRouter(
  prefix="/posts"#id   posts/id
)



@router.get("/",response_model=List[schemas.Post])
def get_posts(db:Session=Depends(get_db)):
  posts=db.query(models.Post).all()
  return posts


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
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

@router.get("/{id}",response_model=schemas.Post)
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


@router.delete("/{id}",response_model=schemas.Post)
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

@router.put("/{id}")
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