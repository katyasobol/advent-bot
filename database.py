from os import getenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

engine = create_engine(getenv('DATABASE'), echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Members(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    username = Column(String)
    name = Column(String)
    score = Column(Integer)

    def __init__(self, id, name, user_id, username, score):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.username = username
        self.score = score


Base.metadata.create_all(bind=engine)

session = Session()
session.close()