from sqlalchemy import Column, Integer, Text, func
from database import Base, SessionLocal

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    age = Column(Integer, nullable=True)
    city = Column(Text, nullable=True)
    country = Column(Text, nullable=True)
    exp_group = Column(Integer, nullable=True)
    gender = Column(Integer, nullable=True)
    os = Column(Text, nullable=True)
    source = Column(Text, nullable=True)

if __name__ == "__main__":
    db = SessionLocal()

    result = (
        db.query(User.country, User.os, func.count("*"))
        .filter(User.exp_group == 3)
        .group_by(User.country, User.os)
        .having(func.count("*") > 100)
        .order_by(func.count("*").desc())
        .all()
    )

    print(result)

    db.close()
