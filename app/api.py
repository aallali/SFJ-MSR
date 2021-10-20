# ************************************************************************************************** #
#                                                                                                    #
#                                                         :::   ::::::::   ::::::::  :::::::::::     #
#    api.py                                            :+:+:  :+:    :+: :+:    :+: :+:     :+:      #
#                                                       +:+         +:+        +:+        +:+        #
#    By: ALLALI <hi@allali.me>                         +#+      +#++:      +#++:        +#+          #
#                                                     +#+         +#+        +#+      +#+            #
#    Created: 2021/10/21 00:22:46 by ALLALI          #+#  #+#    #+# #+#    #+#     #+#              #
#    Updated: 2021/10/21 00:22:46 by ALLALI       ####### ########   ########      ###.ma            #
#                                                                                                    #
# ************************************************************************************************** #


from fastapi import FastAPI, Body, Depends, WebSocket

from app.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.auth_bearer import sJWTBearer
from app.auth.auth_handler import signJWT
from app.db.mongodb import close, connect, AsyncIOMotorClient, get_database
from app.db.helper import find_user_by_prop, insert_user

from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_204_NO_CONTENT,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

posts = [
    {
        "id": 1,
        "title": "Pancake",
        "content": "Lorem Ipsum ..."
    }
]

users = []

app = FastAPI(title="SFJ-MSR", version="1")

@app.on_event("startup")
async def on_app_start():
    """Anything that needs to be done while app starts
    """
    await connect()
    print("== MongoDB == ready ================")



@app.on_event("shutdown")
async def on_app_shutdown():
    """Anything that needs to be done while app shutdown
    """
    await close()

# helpers


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


# route handlers

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your blog!."}


@app.get("/posts", tags=["posts"])
async def get_posts(db: AsyncIOMotorClient = Depends(get_database)) -> dict:
    db = db.client["SFJ-MSR"]
    users = db["users"].find()
    print(users)
    return {"data": posts}


@app.get("/posts/{id}", tags=["posts"])
async def get_single_post(id: int) -> dict:
    if id > len(posts):
        return {
            "error": "No such post with the supplied ID."
        }

    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }


@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def add_post(post: PostSchema) -> dict:
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "data": "post added."
    }


@app.post("/user/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...), db: AsyncIOMotorClient = Depends(get_database)):

    rowUser = await find_user_by_prop("username", db, user.username)

    if rowUser is None:
        print("============>")
        res = await insert_user(user, db)
        raise HTTPException(
            status_code=HTTP_200_OK,
            detail={'jwtsign': res['_jwtsign'],
                    'user_id': str(res['dbuser'].inserted_id)}
        )
    else:
        raise HTTPException(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User with this username already exists",
        )


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }
