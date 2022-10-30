from datetime import datetime

from sqlalchemy import Column, Integer, String, VARCHAR, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from bot.db.sql_crud import AdminModelUser, AdminModelCategory, AdminModelPrice


BaseModel = declarative_base()


class User(BaseModel, AdminModelUser):

    __tablename__ = 'users'

    user_id = Column(Integer(), unique=True, nullable=False, primary_key=True)
    username = Column(VARCHAR(32), unique=False, nullable=True)
    date_registration = Column(Date, default=datetime.today())


class Category(BaseModel, AdminModelCategory):

    __tablename__ = 'categories'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name_category = Column(String(100), unique=True, nullable=False)
    aliases = Column(String(150))


class Price(BaseModel, AdminModelPrice):

    __tablename__ = 'prices'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    amount = Column(Integer(), nullable=False)
    date = Column(Date, default=datetime.today())
    user_id = Column(Integer(), ForeignKey('users.user_id'))
    category_id = Column(Integer(), ForeignKey('categories.id'))


