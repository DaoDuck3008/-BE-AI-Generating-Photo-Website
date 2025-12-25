from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from uuid import uuid4
from config import UPLOAD_DIR
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from core.job_store import JOB_STORE, create_job
from core.run_stage_A import run_stage_A
from core.run_stage_B import run_stage_B, StageBError
import shutil
import threading
from core.ai_models import birefnet_model  # Đảm bảo mô hình được tải khi khởi động ứng dụng
from  pydantic import BaseModel

app = FastAPI()

# Thiết lập CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class EditImage(BaseModel):
    file: str = ""
    bgColor: str= "#0d93d1"
    size: str = "4x6"
    brightness: int = 100
    contrast: int = 100
    saturation: int = 100
    printForm: bool = False

# API xử lý ảnh Stage A
@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...)):
    # 1. Validate Loại file
    if file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ JPG/JPEG/PNG")
    
    # 2. Tạo job_id
    job_id = uuid4().hex

    # 3. lưu file tạm thời
    suffix = Path(file.filename).suffix
    save_path = UPLOAD_DIR / f"{job_id}{suffix}"

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 4. Tạo job trong JOB_STORE
    create_job(job_id)

    # 5. Chạy Stage A ở background
    threading.Thread(
        target=run_stage_A,
        args=(job_id, str(save_path)),
        daemon=True
    ).start()

    # 6. Trả về phản hồi
    return {
        "jobId": job_id,
        "status": "processing"
    }

# API Cập nhật trạng thái xử lý ảnh ở Stage A
@app.get("/api/status/{job_id}")
def get_status(job_id: str):
    job = JOB_STORE.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job không tồn tại")
    
    return job

# API Chỉnh sửa ảnh Stage B
@app.post('/api/edit')
async def edit_image(editImage: EditImage):
    try:
        result = run_stage_B(editImage.file, editImage.bgColor, editImage.size, editImage.brightness, editImage.contrast, editImage.saturation, editImage.printForm)

        return {
            "success": True,
            "img_url": result
        }

    except StageBError as e: 
        raise  HTTPException(
            status_code = 400,
            detail = {
                "code": e.code,
                "message": e.message
            }
        )

    except Exception:
        raise HTTPException(
            status_code = 500,
            detail={
                "code": "SERVER_ERROR",
                "message": "Unexpected server error"
            }
        )

    