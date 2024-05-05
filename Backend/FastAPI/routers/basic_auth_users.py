from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

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
        "password": "123456"
    },
    "heidyra": {    
        "username": "heidyra",
        "name": "Heidy de Sandoval",
        "email": "heidygreen3@gmail.com",
        "disabled": False,
        "password": "123qwe"
    }
}


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Disabled")
    
    return user

@router.post("/loginbasic")
async def login(form: OAuth2PasswordRequestForm = Depends()):

    user = search_user_db(form.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username")

    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/user/mebasic")
async def me(user: User = Depends(current_user)):
    return user
    