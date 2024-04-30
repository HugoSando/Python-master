from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Entity User
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

# This is where the db its supposed to be getting the info
user_list = [User(id=1, name="Hugo", surname="Rene", url="https://hugo.dev", age=32),
            User(id=2, name="Heidy", surname="Raquel", url="https://heidy.dev", age=30),
            User(id=3, name="Bryan", surname="Stu", url="https://bryan.dev", age=29)
         ]

# http://127.0.0.1:8000/userjson
@app.get("/usersjson")
async def usersjson():
    return [
        {"name":"Hugo", "surname": "Rene", "url": "https://hugo.dev", "age":32},
        {"name":"Heidy", "surname": "Raquel", "url": "https://heidy.dev", "age":30},
        {"name":"Bryan", "surname": "Stu", "url": "https://bryan.dev", "age":25},
    ]

# http://127.0.0.1:8000/users
@app.get("/users")
async def users():
    return user_list

# PATH
# http://127.0.0.1:8000/user/1
@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)

# QUERY
# http://127.0.0.1:8000/userquery?id=1
@app.get("/user/")
async def user(id: int):
    return search_user(id)


def search_user(id: int):
    users = filter(lambda user: user.id == id, user_list)
    try:
        return list(users)[0]
    except:
        return {"error":"couldnt find user"}


### Post method
@app.post("/user/")
async def user(user: User):
    if type(search_user(user.id)) == User:
        return {"error":"Id of user already exist"}
    
    user_list.append(user)
    return user

### Put method
@app.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(user_list):
        if saved_user.id == user.id:
            user_list[index] = user
            found = True

    if not found:
        return {"error":"Couldn't update user"}
    else:
        return user
    
@app.delete("/user/{id}")
async def user(id: int):
    for index, saved_user in enumerate(user_list):
        print(saved_user.id)
        print(id)
        if saved_user.id == id:
            del user_list[index]
            return {"deleted":saved_user}
        else:
            return {"error":"Couldn't delete user"}