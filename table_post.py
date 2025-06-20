from sqlalchemy import Column, Integer, Text, select, desc
from database import Base, SessionLocal

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=True)
    topic = Column(Text, nullable=True)

if __name__ == "__main__":
    db = SessionLocal()

    stmt = select(Post.id).where(Post.topic == "business").order_by(desc(Post.id)).limit(10)
    result = db.execute(stmt).fetchall()

    ids = [row[0] for row in result]
    print(ids)

    db.close()
