from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from table_user import User
from table_post import Post

class Feed(Base):
    __tablename__ = "feed_action"

    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    post_id = Column(Integer, ForeignKey(Post.id), primary_key=True)
    action = Column(Text, nullable=True)
    time = Column(DateTime, nullable=True)

    user = relationship(User)
    post = relationship(Post)
