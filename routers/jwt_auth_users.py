from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "5bf7bc3a9ffe4bda9f3685e57381ef138d53b82bec9f99a8b1d6424b988ae9a5"

router = APIRouter()
## oauth
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
## contexto de encrictacion
crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


##
class UserDB(User):
    password: str


users_db = {
    "mike": {
        "username": "mike",
        "full_name": "Michael Gonzalez",
        "email": "michadsad@gmail.com",
        "disabled": False,
        "password": "$2a$12$t6G/5LsbNZZ.C3Gd/VlUauJiYNsHMPTQXh7nmFJJCb7Kixb132qF2",
    },
    "mouredev": {
        "username": "mouredev",
        "full_name": "Brais Moure",
        "email": "mouredev@gmail.com",
        "disabled": True,
        "password": "$2a$12$z7asW96xK.Xd5rZCnlVLfuUi/ALFkRh8EPsIosN..DuIBmM/2miey",
    },
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid auth credentials",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception
    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user is not activated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect user"
        )

    user = search_user_db(form.username)
    # usamos cryp para comparar las contraseñas
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )
    # 1min
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_DURATION)
    expire = datetime.utcnow() + access_token_expires

    access_token = {"sub": user.username, "exp": expire}
    ## retornamos el token encryptado
    return {
        "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM),
        "token_type": "bearer",
    }


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
