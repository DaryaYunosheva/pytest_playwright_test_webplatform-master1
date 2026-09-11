from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import News, Comment, User
from ..schemas import CommentCreate, CommentResponse
from ..auth import get_current_user

router = APIRouter(prefix="/api/news", tags=["comments"])

@router.post("/{news_id}/comments", response_model=CommentResponse)
def create_comment(
    news_id: int,
    comment: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    
    db_comment = Comment(text=comment.text, author_id=current_user.id, news_id=news_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/{news_id}/comments", response_model=List[CommentResponse])
def get_comments(news_id: int, db: Session = Depends(get_db)):
    news = db.query(News).filter(News.id == news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return db.query(Comment).filter(Comment.news_id == news_id).order_by(Comment.created_at.desc()).all()
