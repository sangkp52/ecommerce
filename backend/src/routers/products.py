from typing import List
from fastapi import APIRouter, Body, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response

from src.database import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.models.products import Product, UpdateProduct

from bson import ObjectId


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/", response_model=List[Product])
async def get_products(
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    products = await db["products"].find().to_list(100)
    return products


@router.get("/{id}", response_model=Product)
async def get_product(
    id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    if (product := await db["products"].find_one({"_id": ObjectId(id)})) is not None:
    return product

    raise HTTPException(status_code=404, detail=f"Product {id} not found")


@router.post("/", response_model=Product)
async def create_product(product: Product = Body(...), db: AsyncIOMotorDatabase = Depends(get_db)):
    product = jsonable_encoder(product)
    result = await db["products"].insert_one(product)
    created = await db["products"].find_one({"_id": result.inserted_id})
    return jsonable_encoder(created)


@router.put("/{id}")
async def update_product(
    id: str,
    product: UpdateProduct = Body(...),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    product = {
        k: v for k, v in product.dict().items()
        if v is not None
    }

    if len(product) >= 1:
        update_result = await db["products"].update_one(
            {"_id": ObjectId(id)},
            {"$set": product}
        )

        if update_result.modified_count > 0:
            updated_product = await db["products"].find_one({
                "_id": ObjectId(id)
            })

            return updated_product

    existing_product = await db["products"].find_one({
        "_id": ObjectId(id)
    })

    if existing_product is not None:
        return existing_product

    raise HTTPException(status_code=404, detail=f"Product {id} not found")


@router.delete("/{id}")
async def delete_product(
    id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    delete_result = await db["products"].delete_one({
        "_id": ObjectId(id)
    })

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Product {id} not found")