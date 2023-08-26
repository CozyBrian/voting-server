from extensions import db 
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

class User(db.Model):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    dob = db.Column(db.String(75))
    gender = db.Column(db.String(50))
    number = db.Column(db.String(50))
    classOfUser = db.Column(db.String(75))
    
# class Candidate(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(75))  #name of candidate
#     position = db.Column(db.String(150)) #president, vice-president
#     numberVotes = db.Column(db.Integer) #if null, use 0

class Role(db.Model):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    role = Column(Text, nullable=False)
    
class Candidate(db.Model):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    __tablename__ = 'candidates'
    
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    candidate = Column(Text, nullable=False)
    role = relationship("Role")
    
class Vote(db.Model):
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    __tablename__ = 'votes'
    
    vote_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    roles_id = Column(Integer, ForeignKey('roles.id'))
    candidate_id = Column(Integer, ForeignKey('candidates.id'))
    user = relationship("User")
    role = relationship("Role")
    candidate = relationship("Candidate")

    
"""
# PostgreSQL database configuration for creating new tables
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://georgette_project_user:xOLCvgOroVw5S4C3BBFbdTdasca4Qts6@dpg-ciuio7liuiedpv0b2prg-a.oregon-postgres.render.com/georgette_project"  # Replace with your PostgreSQL credentials and database details
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(20), unique=True)
    otp_code = Column(String(6))

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    dob = Column(String(75))
    gender = Column(String(50))
    number = Column(String(50))
    classOfUser = Column(String(75))
    voted = Column(Boolean)

class Candidate(Base):
    __tablename__ = 'candidate'
    id = Column(Integer, primary_key=True)
    name = Column(String(75))  #name of candidate
    position = Column(String(150)) #president, vice-president
    numberVotes = Column(Integer) #if null, use 0

Base.metadata.create_all(engine)

"""