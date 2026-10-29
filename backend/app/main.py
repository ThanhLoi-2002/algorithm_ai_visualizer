from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.api.api import api_router

app = FastAPI(title="FastAPI with uv")

# Danh sách các nguồn (origins) được phép gọi API
# Trong giai đoạn phát triển, bạn có thể dùng ["*"] cho phép tất cả,
# nhưng khi lên production nên chỉ định rõ domain của frontend.
origins = [
    "http://localhost:3000",  # Ví dụ: React/Next.js chạy ở cổng 3000
    "http://localhost:5173",  # Ví dụ: Vite / Vue / React chạy ở cổng 5173
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    # Thêm domain production của bạn ở đây sau khi deploy
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hoặc dùng ["*"] để cho phép mọi nguồn
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức (GET, POST, PUT, DELETE...)
    allow_headers=["*"],  # Cho phép tất cả các headers
)

app.include_router(api_router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Xin chào! FastAPI chạy bằng uv rất nhanh!"}


class SearchRequest(BaseModel):
    arr: List[int]
    target: int

@app.post("/api/simulate/binary-search")
def simulate_binary_search(data: SearchRequest):
    # Sắp xếp mảng để đảm bảo điều kiện tìm kiếm nhị phân
    arr = sorted(data.arr)
    target = data.target
    
    left = 0
    right = len(arr) - 1
    steps = []
    found = False
    result_index = -1

    # Mô phỏng từng bước thuật toán
    while left <= right:
        mid = (left + right) // 2
        
        step_info = {
            "left": left,
            "right": right,
            "mid": mid,
            "mid_value": arr[mid],
            "comparison": "equal" if arr[mid] == target else ("greater" if arr[mid] > target else "smaller")
        }
        steps.append(step_info)

        if arr[mid] == target:
            found = True
            result_index = mid
            break
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return {
        "algorithm": "Binary Search",
        "sorted_array": arr,
        "target": target,
        "found": found,
        "index": result_index,
        "total_steps": len(steps),
        "steps": steps
    }
