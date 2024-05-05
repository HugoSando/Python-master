from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "50c394ea453bde4405a72cfd6fda658911fdaf7145798958b445105b91455c88"

router = APIRouter()

#VALIDATING TOKEN STEP 1
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "hugosa": {    
        "username": "hugosa",
        "name": "Hugo Sandoval",
        "email": "hugosa291@gmail.com",
        "disabled": False,
        "password": "$2b$12$XHKYSDB6Cvm24WjIniTHFOYA3aQWhaTahCifCBRam5YNJTDs1dDvO" #123456
    },
    "heidyra": {    
        "username": "heidyra",
        "name": "Heidy de Sandoval",
        "email": "heidygreen3@gmail.com",
        "disabled": False,
        "password": "$2b$12$6eQJviGvWCXNtr.L.7K8buFlQTLgr9Vh89pEDqGrNW3veYac/LBOu" #123qwe
    }
}

################################################
#FOR LOGIN
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
#LOGIN PROCESS
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):

    user = search_user_db(form.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username")

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    access_token = {
        "sub": user.username,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }
    
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

################################################
#FOR VALIDATION OF USER
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

#VALIDATING TOKEN STEP 2
async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")
        if username is None:
            raise exception
        elif not search_user(username):
            raise exception
     
    except JWTError:
        raise exception
    
    return search_user(username)

#VALIDATING TOKEN STEP 3
async def current_user(user: User = Depends(auth_user)):
    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Disabled")
    
    return user

#STEP 4 WITH TOCKEN VALIDATED RETREIVES USER INFO
@router.get("/user/me")
async def me(user: User = Depends(current_user)):
    return user