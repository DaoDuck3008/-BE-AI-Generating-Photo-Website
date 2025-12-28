from core.job_store import update_job
from core.stage_A.background_removal import remove_background, RemoveBackgroundError
from core.stage_A.align_and_crop import align_and_crop_image
from core.save_img import save_img, SaveImageError
from PIL import Image

def run_stage_A(job_id: str, image: Image.Image):
    try:

        # A1. Validate
        update_job(
            job_id,
            process="processing",
            step="validate",
            progress=10,
            message="Phân tích ảnh"
        )

        # A2. Background removal
        update_job(
            job_id,
            step="background",
            progress=40,
            message="Tách nền AI"
        )
        img = remove_background(image)

        # A3. Align & crop
        update_job(
            job_id,
            step="align",
            progress=70,
            message="Căn chỉnh khuôn mặt"
        )
        result = align_and_crop_image(img)

        # A4. Save
        result = save_img(image=result, public_id=job_id, folder="potrait_photos", format="PNG")
        
        update_job(
            job_id,
            status="done",
            step="done",
            progress=100,
            message="Hoàn tất"
        )
    except RemoveBackgroundError as e: 
        update_job(
            job_id,
            status="error",
            message=str(e)
        )

    except SaveImageError as e:
        update_job(
            job_id,
            status="error",
            message=str(e)
        )

    except Exception as e:
        update_job(
            job_id,
            status="error",
            message=str(e)
        )
