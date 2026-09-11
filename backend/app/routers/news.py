from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, Form
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import get_db
from ..models import News, Tag, User, Comment
from ..schemas import NewsCreate, NewsResponse, TagResponse
from ..auth import get_current_user
import os
import shutil
from pathlib import Path

router = APIRouter(prefix="/api/news", tags=["news"])

UPLOAD_DIR = Path("uploads/news_images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/", response_model=dict)
def get_all_news(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=50),
    tag: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(News)
    
    if tag:
        query = query.join(News.tags).filter(Tag.name == tag)
    if search:
        query = query.filter(
            (News.title.ilike(f"%{search}%")) | 
            (News.text.ilike(f"%{search}%")) |
            (News.subtitle.ilike(f"%{search}%"))
        )
    
    total = query.count()
    news_list = query.order_by(News.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
    
    result = []
    for news in news_list:
        news_dict = NewsResponse.from_orm(news).dict()
        news_dict['comments_count'] = db.query(Comment).filter(Comment.news_id == news.id).count()
        result.append(news_dict)
    
    return {
        "items": result,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page
    }

@router.post("/", response_model=NewsResponse)
async def create_news(
    title: str = Form(...),
    text: str = Form(...),
    subtitle: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    news = News(title=title, subtitle=subtitle, text=text, author_id=current_user.id)
    
    if tags:
        tag_list = [t.strip() for t in tags.split(',')]
        for tag_name in tag_list:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
            news.tags.append(tag)
    
    if image:
        file_extension = image.filename.split('.')[-1]
        file_name = f"news_{len(os.listdir(UPLOAD_DIR)) + 1}.{file_extension}"
        file_path = UPLOAD_DIR / file_name
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        news.image_path = f"/uploads/news_images/{file_name}"
    
    db.add(news)
    db.commit()
    db.refresh(news)
    return news

@router.get("/tags", response_model=List[TagResponse])
def get_all_tags(db: Session = Depends(get_db)):
    return db.query(Tag).all()

@router.get("/{news_id}", response_model=NewsResponse)
def get_news_detail(news_id: int, db: Session = Depends(get_db)):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    news_dict = NewsResponse.from_orm(news).dict()
    news_dict['comments_count'] = db.query(Comment).filter(Comment.news_id == news.id).count()
    return news_dict
