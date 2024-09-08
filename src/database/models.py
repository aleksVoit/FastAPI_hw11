from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.ext.declarative import declarative_base

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
