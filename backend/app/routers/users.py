from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserResponse, UserUpdate
from ..auth import get_current_user, hash_password
import os
import shutil
from pathlib import Path

router = APIRouter(prefix="/api/users", tags=["users"])

UPLOAD_DIR = Path("uploads/user_photos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_update.email:
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = user_update.email
    
    if user_update.first_name:
        current_user.first_name = user_update.first_name
    if user_update.last_name:
        current_user.last_name = user_update.last_name
    if user_update.phone:
        current_user.phone = user_update.phone
    if user_update.password:
        current_user.password_hash = hash_password(user_update.password)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/me/photo", response_model=UserResponse)
async def upload_photo(
    photo: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    file_extension = photo.filename.split('.')[-1]
    file_name = f"user_{current_user.id}.{file_extension}"
    file_path = UPLOAD_DIR / file_name
    
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)
    
    current_user.photo_path = f"/uploads/user_photos/{file_name}"
    db.commit()
    db.refresh(current_user)
    return current_user
