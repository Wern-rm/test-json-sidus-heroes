from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,  index=True)
    login = Column(String, index=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    at_create = Column(TIMESTAMP, nullable=False, default=datetime.now())
