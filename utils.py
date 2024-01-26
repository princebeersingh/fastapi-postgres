from passlib.context import CryptContext
pwd_context =CryptContext(schemes=["bcrypt"],deprecated="auto")

def hashin(password:str):
  return pwd_context.hash(password)