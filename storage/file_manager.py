from sqlalchemy import create_engine, String, Integer, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from datetime import datetime
import os 

# Load password from environment variable
db_password = os.getenv("DB_PASSWORD")

engine = create_engine(f'mysql+mysqlconnector://root:{db_password}@localhost/blog_system', echo=True)

#Creates a session factory and sessiom (EXPLANATION)
Session = sessionmaker(bind=engine)
session = Session()

class Base(DeclarativeBase):
    pass

class Post(Base): 
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(String(2500))
    author: Mapped[str] = mapped_column(String(100))
    creation_date: Mapped[datetime] = mapped_column(DateTime, default = datetime.now)
    is_published: Mapped[bool] = mapped_column(Boolean, default = False)

class User(Base): 
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key = True)
    username: Mapped[str] = mapped_column(String(100), unique = True)
    password: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(20), default = "user")
    is_banned: Mapped[bool] = mapped_column(Boolean, default = False)

Base.metadata.create_all(engine)
