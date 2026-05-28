from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from src.auth.models import UserLoginSchema, UserSignupSchema
from datetime import datetime

from src.database import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.models.users import User
from src.auth.utils import hash_password, verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["Auth"])


# @router.post("/login", tags=["Auth"])
# async def login(user: UserLoginSchema = Body(...)):
# @router.post("/login", tags=["Auth"])
# async def login(user: UserLoginSchema, db: AsyncIOMotorDatabase = Depends(get_db)):
#     registered = await db["users"].find_one({"email": user.email})
    
#     if registered is None:
#         return {"error": "users does not exists."}

#     # user = user.dict()

#     if not registered.get("password"):
#         raise HTTPException(status_code=401, detail="Invalid user data in DB")

#     # if verify_password(user.get("password"), registered.get("password")):
#     if verify_password(user.password, registered["password"]):
#         token = create_access_token(user["email"])
#         return {"access_token": token}
#     else:
#         return {"error", "password is incorrect."}

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

@router.post("/login")
async def login(
    user: UserLoginSchema = Body(...),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    registered = await db["users"].find_one({
        "email": user.email
    })

    if registered is None:
        return {"error": "user does not exist"}

    if verify_password(user.password, registered["password"]):
        token = create_access_token(user.email)

        return {
            "access_token": token
        }

    return {
        "error": "password incorrect"
    }

@router.post("/signup", tags=["Auth"])
# async def signup(user: UserSignupSchema = Body(...)):
#     already_exists = await db["users"].find_one({"email": user.email })
async def signup(
    user: UserSignupSchema,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    already_exists = await db["users"].find_one({"email": user.email})

    if already_exists:
        return { "error": "User already exists" }

    if user.password != user.password_confirmation:
        return { "error": "Passwords are different" }
    
    hashed = hash_password(user.password)
    new_user = {
        "email": user.email,
        "password": hashed,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    # created = await db["users"].insert_one(new_user)
    # return jsonable_encoder(created)
    created = await db["users"].insert_one(new_user)
    return {
        "id": str(created.inserted_id),
        "email": user.email
    }
