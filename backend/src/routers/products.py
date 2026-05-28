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
    # Tránh lỗi mã hóa ObjectId bằng cách chuyển đổi nó thành chuỗi thủ công cho từng sản phẩm
    for p in products:
        if "_id" in p:
            p["_id"] = str(p["_id"])
    return products


@router.get("/{id}", response_model=Product)
async def get_product(
    id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    if (product := await db["products"].find_one({"_id": ObjectId(id)})) is not None:
        if "_id" in product:
            product["_id"] = str(product["_id"])
        return product

    raise HTTPException(status_code=404, detail=f"Product {id} not found")


# @router.post("/", response_model=None)
# async def create_product(
#     product: Product = Body(...), 
#     db: AsyncIOMotorDatabase = Depends(get_db)
# ):
#     # Lấy dữ liệu dạng dict và loại bỏ trường id mặc định để tránh ghi đè dữ liệu rỗng
#     product_dict = product.dict(by_alias=True, exclude_unset=True)
    
#     if "_id" in product_dict and not product_dict["_id"]:
#         del product_dict["_id"]
#     if "id" in product_dict and not product_dict["id"]:
#         del product_dict["id"]
        
#     result = await db["products"].insert_one(product_dict)
#     created = await db["products"].find_one({"_id": result.inserted_id})
    
#     # SỬA LỖI TẠI ĐÂY: Biến ObjectId thành chuỗi (str) trước khi đẩy vào jsonable_encoder
#     if created and "_id" in created:
#         created["_id"] = str(created["_id"])
        
#     return jsonable_encoder(created)

@router.post("/", response_model=None)
async def create_product(
    product: Product = Body(...), 
    db: AsyncIOMotorDatabase = Depends(get_db),
    # SỬA TẠI ĐÂY: Thêm dòng này để FastAPI tự động chặn đứng nếu không có Token hợp lệ
    current_user: dict = Depends(get_current_user) 
):
    # Dưới này giữ nguyên logic cũ của bạn
    product_dict = product.dict(by_alias=True, exclude_unset=True)
    
    if "_id" in product_dict and not product_dict["_id"]:
        del product_dict["_id"]
    if "id" in product_dict and not product_dict["id"]:
        del product_dict["id"]
        
    result = await db["products"].insert_one(product_dict)
    created = await db["products"].find_one({"_id": result.inserted_id})
    
    if created and "_id" in created:
        created["_id"] = str(created["_id"])
        
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
            if updated_product and "_id" in updated_product:
                updated_product["_id"] = str(updated_product["_id"])
            return jsonable_encoder(updated_product)

    existing_product = await db["products"].find_one({
        "_id": ObjectId(id)
    })

    if existing_product is not None:
        if "_id" in existing_product:
            existing_product["_id"] = str(existing_product["_id"])
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