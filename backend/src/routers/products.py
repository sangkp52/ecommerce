# from typing import List
# from fastapi import APIRouter, Body, HTTPException, status, Depends
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import Response

# from src.database import get_db
# from motor.motor_asyncio import AsyncIOMotorDatabase

# from src.models.products import Product, UpdateProduct

# from bson import ObjectId


# router = APIRouter(
#     prefix="/products",
#     tags=["Products"]
# )


# @router.get("/", response_model=List[Product])
# async def get_products(
#     db: AsyncIOMotorDatabase = Depends(get_db)
# ):
#     products = await db["products"].find().to_list(100)
#     return products


# @router.get("/{id}", response_model=Product)
# async def get_product(
#     id: str,
#     db: AsyncIOMotorDatabase = Depends(get_db)
# ):
#     if (product := await db["products"].find_one({"_id": ObjectId(id)})) is not None:
#         return product

#     raise HTTPException(status_code=404, detail=f"Product {id} not found")


# @router.post("/", response_model=Product)
# async def create_product(product: Product = Body(...), db: AsyncIOMotorDatabase = Depends(get_db)):
#     product = jsonable_encoder(product)
#     result = await db["products"].insert_one(product)
#     created = await db["products"].find_one({"_id": result.inserted_id})
#     return jsonable_encoder(created)


# @router.put("/{id}")
# async def update_product(
#     id: str,
#     product: UpdateProduct = Body(...),
#     db: AsyncIOMotorDatabase = Depends(get_db)
# ):
#     product = {
#         k: v for k, v in product.dict().items()
#         if v is not None
#     }

#     if len(product) >= 1:
#         update_result = await db["products"].update_one(
#             {"_id": ObjectId(id)},
#             {"$set": product}
#         )

#         if update_result.modified_count > 0:
#             updated_product = await db["products"].find_one({
#                 "_id": ObjectId(id)
#             })

#             return updated_product

#     existing_product = await db["products"].find_one({
#         "_id": ObjectId(id)
#     })

#     if existing_product is not None:
#         return existing_product

#     raise HTTPException(status_code=404, detail=f"Product {id} not found")


# @router.delete("/{id}")
# async def delete_product(
#     id: str,
#     db: AsyncIOMotorDatabase = Depends(get_db)
# ):
#     delete_result = await db["products"].delete_one({
#         "_id": ObjectId(id)
#     })

#     if delete_result.deleted_count == 1:
#         return Response(status_code=status.HTTP_204_NO_CONTENT)

#     raise HTTPException(status_code=404, detail=f"Product {id} not found")
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

# Đổi response_model thành dict hoặc bỏ qua để FastAPI không lọc mất '_id' từ MongoDB
@router.post("/", response_model=None)
async def create_product(
    product: Product = Body(...), 
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Lấy dữ liệu dạng dict loại bỏ hoàn toàn các trường chưa thiết lập (như id rỗng)
    product_dict = product.model_dump(by_alias=True, exclude_unset=True) 
    
    # Nếu có trường _id nhưng giá trị rỗng/None, xóa đi để MongoDB tự sinh ObjectId mới
    if "_id" in product_dict and not product_dict["_id"]:
        del product_dict["_id"]
        
    result = await db["products"].insert_one(product_dict)
    created = await db["products"].find_one({"_id": result.inserted_id})
    return jsonable_encoder(created)

@router.put("/{id}")
async def update_product(
    id: str,
    product: UpdateProduct = Body(...),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    product_data = {
        k: v for k, v in product.dict().items()
        if v is not None
    }

    if len(product_data) >= 1:
        update_result = await db["products"].update_one(
            {"_id": ObjectId(id)},
            {"$set": product_data}
        )

        if update_result.modified_count > 0:
            updated_product = await db["products"].find_one({
                "_id": ObjectId(id)
            })
            return jsonable_encoder(updated_product)

    existing_product = await db["products"].find_one({
        "_id": ObjectId(id)
    })

    if existing_product is not None:
        return jsonable_encoder(existing_product)

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