from fastapi import FastAPI, Request, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any

from fastapi_authtools import AuthManager, login_required
from fastapi_authtools.models import UserModel, UsernamePasswordToken


app = FastAPI()

SECRET_KEY = 'secretSERCRET007'
EXPIRE_MINUTES = 60 * 40
ALGORITHM = "HS256"

# create login manager
auth_manager = AuthManager(
    app=app,
    secret_key=SECRET_KEY,
    algorithm=ALGORITHM,
    expire_minutes=EXPIRE_MINUTES
)
app.state.auth_manager = auth_manager


fakedb: list[dict] = [
    {
        "id": 1,
        "username": "admin",
        "email": "admin@gmail.com",
        "password": "password_for_admin"
    },
    {
        "id": 2,
        "username": "michael7nightingale",
        "email": "suslanchikmopl@gmail.com",
        "password": "password"
    },

]


class UserRegisterDbModel(BaseModel):
    username: str
    password: str
    email: str


class UserInDbModel(UserRegisterDbModel):
    id: int


def get_user_from_db(key: str, value: Any) -> UserInDbModel | None:
    for user in fakedb:
        if user.get(key) == value:
            return UserInDbModel(**user)


def validate_password(password: str, hash_: str) -> bool:
    return password == hash_


@app.get("/")
async def homepage(request: Request):
    return request.user


@app.post("/login")
async def login(user_token_data: UsernamePasswordToken = Body()):
    user = get_user_from_db("username", user_token_data.username)
    if user is None:
        return JSONResponse(
            content={'detail': "Cannot find user with this credentials."},
            status_code=400,
        )
    if not validate_password(user_token_data.password, user.password):
        return JSONResponse(
            content={'detail': "Password is invalid."},
            status_code=400,
        )
    user_model = UserModel(**user.model_dump())
    token = app.state.auth_manager.create_token(data=user_model)
    return {'access-token': token}


@app.post("/register", status_code=201)
async def register(user_register_data: UserRegisterDbModel = Body()):
    user_data = user_register_data.model_dump()
    user_data['id'] = fakedb[-1]['id'] + 1
    fakedb.append(user_data)
    return fakedb[-1]


@app.get("/me")
@login_required
async def me(request: Request):
    return request.user
