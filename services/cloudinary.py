import cloudinary
import cloudinary.uploader
from app.config import settings

cloudinary.config(
    cloud_name=settings.cloudinary_cloud_name,
    api_key=settings.cloudinary_api_key,
    api_secret=settings.cloudinary_api_secret,
)

@router.post("/avatar")
def upload_avatar(file: UploadFile, user=Depends(get_current_user)):
    result = cloudinary.uploader.upload(file.file)
    user.avatar_url = result["secure_url"]
    db.commit()
    return {"avatar": user.avatar_url}
