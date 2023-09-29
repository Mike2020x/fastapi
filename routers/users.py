from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/users", tags=["users"], responses={404: {"message": "No encontrado"}}
)


# class User
class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int


users_list = [
    User(id=1, name="Michael", surname="Gonzalez", age=26),
    User(id=2, name="Juan", surname="Gonzalez", age=20),
    User(id=3, name="Jorge", surname="Gonzalez", age=51),
]


# function search user
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "User not found"}


# @router.get("/users")
# async def users():
#     return [
#         {"name": "Michael", "surname": "Gonzalez", "age": 26},
#         {"name": "Juan", "surname": "Gonzalez", "age": 20},
#         {"name": "Jorge", "surname": "Gonzalez", "age": 51},
#     ]


### get
@router.get("/users")
async def users():
    return users_list


# path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)


# query
@router.get("/userquery/")
async def user(id: int):
    return search_user(id)


## create
@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="User already exists")
    users_list.append(user)
    return user


## edit
@router.put("/user/")
async def user(user: User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "User not found"}
    else:
        return user


# delete
@router.delete("/user/{id}")
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        return {"error": "User not deleted"}
