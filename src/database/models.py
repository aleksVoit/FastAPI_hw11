from sqlalchemy import Column, Integer, String, ARRAY, UniqueConstraint, Boolean, func, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date, DateTime

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(25), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone_number = Column(String(20), nullable=False)
    birthday = Column(Date, nullable=False)  # new_user = User(name='Alice', birthdate=date(1995, 5, 17))
    notes = Column(ARRAY(String))
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref='contacts')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('created_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)






