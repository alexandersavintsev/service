from fastapi import FastAPI, HTTPException
from fastapi import Query
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import SessionLocal
from table_user import User
from table_post import Post
from table_feed import Feed
from schema import UserGet, PostGet, FeedGet

app = FastAPI()


# подключение к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔹 Получение пользователя
@app.get("/user/{id}", response_model=UserGet)
def get_user(id: int):
    db: Session = next(get_db())
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# 🔹 Получение поста
@app.get("/post/{id}", response_model=PostGet)
def get_post(id: int):
    db: Session = next(get_db())
    post = db.query(Post).filter(Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


# 🔹 Feed по пользователю
@app.get("/user/{id}/feed", response_model=List[FeedGet])
def get_user_feed(id: int, limit: int = 10):
    db: Session = next(get_db())
    feed = (
        db.query(Feed)
        .filter(Feed.user_id == id)
        .order_by(Feed.time.desc())
        .limit(limit)
        .all()
    )
    return feed


# 🔹 Feed по посту
@app.get("/post/{id}/feed", response_model=List[FeedGet])
def get_post_feed(id: int, limit: int = 10):
    db: Session = next(get_db())
    feed = (
        db.query(Feed)
        .filter(Feed.post_id == id)
        .order_by(Feed.time.desc())
        .limit(limit)
        .all()
    )
    return feed


# 🔹 Рекомендации по постам
@app.get("/post/recommendations/", response_model=List[PostGet])
def get_recommended_posts(id: int, limit: int = 10):
    db: Session = next(get_db())
    posts = (
        db.query(Post)
        .select_from(Feed)
        .join(Post, Feed.post_id == Post.id)
        .filter(Feed.action == "like")
        .group_by(Post.id)
        .order_by(func.count(Post.id).desc())
        .limit(limit)
        .all()
    )
    return posts
