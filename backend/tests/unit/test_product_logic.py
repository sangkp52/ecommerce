import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from bson import ObjectId

from src.models.products import Product, UpdateProduct
from src.routers.products import (
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product
)

@pytest.fixture
def mock_db():
    db = MagicMock()
    db["products"] = MagicMock()
    return db

@pytest.mark.asyncio
async def test_create_product_logic(mock_db):
    """Test unit: Logic tạo sản phẩm thành công"""
    # Chuẩn bị dữ liệu đầu vào dạng Pydantic Model
    input_product = Product(
        name="Unit Test Phone",
        description="A phone for testing",
        price=999.0
    )
    
    # Giả lập kết quả trả về từ MongoDB sau khi insert và find_one
    fake_id = ObjectId()
    mock_insert_result = MagicMock()
    mock_insert_result.inserted_id = fake_id
    
    mock_db["products"].insert_one = AsyncMock(return_value=mock_insert_result)
    mock_db["products"].find_one = AsyncMock(return_value={
        "_id": fake_id,
        "name": "Unit Test Phone",
        "description": "A phone for testing",
        "price": 999.0
    })

    # Gọi hàm xử lý logic của Route
    result = await create_product(product=input_product, db=mock_db)

    # Kiểm tra kết quả logic trả về
    assert result["_id"] == str(fake_id)
    assert result["name"] == "Unit Test Phone"
    assert result["price"] == 999.0


@pytest.mark.asyncio
async def test_get_all_products_logic(mock_db):
    """Test unit: Logic lấy danh sách sản phẩm"""
    # Giả lập danh sách dữ liệu thô từ DB
    fake_id_1 = ObjectId()
    fake_id_2 = ObjectId()
    fake_list = [
        {"_id": fake_id_1, "name": "P1", "description": "D1", "price": 10.0},
        {"_id": fake_id_2, "name": "P2", "description": "D2", "price": 20.0}
    ]
    
    # Giả lập chuỗi hàm .find().to_list(100) của Motor
    mock_find_cursor = MagicMock()
    mock_find_cursor.to_list = AsyncMock(return_value=fake_list)
    mock_db["products"].find = MagicMock(return_value=mock_find_cursor)

    # Gọi hàm xử lý
    result = await get_products(db=mock_db)

    # Kiểm tra danh sách nhận được
    assert len(result) == 2
    assert result[0]["_id"] == str(fake_id_1)
    assert result[1]["name"] == "P2"


@pytest.mark.asyncio
async def test_get_one_product_success_logic(mock_db):
    """Test unit: Lấy chi tiết một sản phẩm thành công"""
    fake_id = ObjectId()
    mock_db["products"].find_one = AsyncMock(return_value={
        "_id": fake_id,
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 1500.0
    })

    result = await get_product(id=str(fake_id), db=mock_db)

    assert result["_id"] == str(fake_id)
    assert result["name"] == "Laptop"


@pytest.mark.asyncio
async def test_get_one_product_not_found_logic(mock_db):
    """Test unit: Lấy sản phẩm thất bại khi ID không tồn tại (Phải ném ra lỗi 404)"""
    fake_id = str(ObjectId())
    mock_db["products"].find_one = AsyncMock(return_value=None)

    # Kiểm tra xem hàm có chủ động raised HTTPException 404 hay không
    with pytest.raises(HTTPException) as exc_info:
        await get_product(id=fake_id, db=mock_db)

    assert exc_info.value.status_code == 404
    assert f"Product {fake_id} not found" in exc_info.value.detail


@pytest.mark.asyncio
async def test_update_product_logic(mock_db):
    """Test unit: Cập nhật giá sản phẩm thành công"""
    fake_id = ObjectId()
    update_data = UpdateProduct(price=1200.0)

    # Giả lập update_one thành công (modified_count > 0)
    mock_update_result = MagicMock()
    mock_update_result.modified_count = 1
    mock_db["products"].update_one = AsyncMock(return_value=mock_update_result)
    
    # Giả lập dữ liệu mới sau khi sửa đổi để hàm find_one trả về
    mock_db["products"].find_one = AsyncMock(return_value={
        "_id": fake_id,
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 1200.0
    })

    result = await update_product(id=str(fake_id), product=update_data, db=mock_db)

    assert result["price"] == 1200.0


@pytest.mark.asyncio
async def test_delete_product_success_logic(mock_db):
    """Test unit: Xóa sản phẩm thành công"""
    fake_id = str(ObjectId())
    
    # Giả lập delete_one tìm thấy và xóa được 1 bản ghi
    mock_delete_result = MagicMock()
    mock_delete_result.deleted_count = 1
    mock_db["products"].delete_one = AsyncMock(return_value=mock_delete_result)

    result = await delete_product(id=fake_id, db=mock_db)

    # Kiểm tra xem hàm có trả về đúng mã trạng thái HTTP 204 không
    assert result.status_code == 204