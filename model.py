from sqlalchemy import Column,String,Integer,Text,DateTime,Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  sessionmaker

engine = create_engine("mysql+pymysql://chan:1@localhost:3306/weibo")
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "user"

    id = Column(Integer,primary_key=True)
    nickname = Column(String(20),unique=True)
    password = Column(String(128))
    gender = Column(String(10))
    city = Column(String(10))
    bio = Column(String(256))

class Weibo(Base):
    __tablename__ = "weibo"
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer)
    content = Column(Text)
    created = Column(DateTime)

class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer)
    wb_id = Column(Integer)
    cmt_id = Column(Integer,default=0)
    content = Column(Text)
    created = Column(DateTime)

    @property
    def up_comment(self):
        '''当前评论的上游评论'''
        session = Session()
        return session.query(Comment).get(self.cmt_id)

class Like(Base):
    __tablename__ = 'like'

    wb_id = Column(Integer,primary_key=True)
    user_id = Column(Integer,primary_key=True)
    status = Column(Boolean,default=True)
    created = Column(DateTime)

class Follow(Base):
    __tablename__ = 'foloow'

    wb_id = Column(Integer, primary_key=True)
    follow_id = Column(Integer, primary_key=True)
    status = Column(Boolean, default=True)
    created = Column(DateTime)

