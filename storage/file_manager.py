from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
import os 
from dotenv import load_dotenv 

load_dotenv()

# Load password from environment variable
db_password = os.getenv("DB_PASSWORD")

engine = create_engine(f'mysql+mysqlconnector://root:{db_password}@localhost/blog_system', echo=True)

#Creates a session factory and sessiom (EXPLANATION)
Session = sessionmaker(bind=engine)
session = Session()

Base= declarative_base()

class Post(Base): 
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True)
    title = Column(String(200))
    content = Column(String(2500))
    author = Column(String(100))
    creation_date = Column(DateTime, default = datetime.now)
    is_published = Column(Boolean, default = False)

class User(Base): 
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    username = Column(String(100), unique = True)
    password = Column(String(100))
    role = Column(String(20), default = "user")
    is_banned = Column(Boolean, default = False)

Base.metadata.create_all(engine)
