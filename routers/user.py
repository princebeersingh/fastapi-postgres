from fastapi import status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
import models,schemas,utils
from database import get_db
router=APIRouter(prefix="/users",tags=['Users'])





@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.CreateUser,db:Session=Depends(get_db)):

  #hash the passwd

  hashed_pwd=utils.hashin(user.password)
  user.password=hashed_pwd

  new_user=models.User(**user.dict())  #dict method easy to add new feature to the schema
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  
  return new_user



@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id:int ,db:Session=Depends(get_db)):
  user=db.query(models.User).filter(models.User.id==id).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id {id} doesn`t exists")
  

  return user