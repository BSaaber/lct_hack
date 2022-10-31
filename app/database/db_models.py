from sqlalchemy import Column, Integer, String

from .engine import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    level = Column(Integer)


class TsnPiece(Base):
    __tablename__ = "tsn"

    # название сборника?
    # доп информация джсоном?
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)  # шифр
    text = Column(String)  # наименование работ и затрат
    price = Column(Integer)  # всего затрат в текущем уровне, руб
    # TODO Добавить метч с SpgzPiece. Возможно храним список даже, а не единственное число. т е многие ко многим


class SpgzPiece(Base):
    __tablename__ = "spgz"

    id = Column(Integer, primary_key=True, index=True)

    # TODO поля
