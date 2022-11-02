from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


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
    code = Column(String, unique=True)  # шифр
    text = Column(String)  # наименование работ и затрат
    price = Column(Integer)  # всего затрат в текущем уровне, руб
    # spgz_piece_id = Column(Integer, ForeignKey("spgz.id"))
    # spgz_piece = relationship("SpgzPiece")
    hypothesises = relationship("Hypothesis")
    # TODO Добавить метч с SpgzPiece. Возможно храним список даже, а не единственное число. т е многие ко многим


class Hypothesis(Base):
    __tablename__ = "hypothesis"
    id = Column(Integer, primary_key=True, index=True)
    priority = Column(Integer)
    tsn_piece_id = Column(Integer, ForeignKey("tsn.id"))
    spgz_piece_id = Column(Integer, ForeignKey("spgz.id"))


class SpgzPiece(Base):
    __tablename__ = "spgz"

    id = Column(Integer, primary_key=True, index=True)
    data_id = Column(Integer, unique=True)  # ID из датасета, по тз просили хранить в базе
    name = Column(String)
    description = Column(String)
    okpd = Column(String)
    okpd2 = Column(String)
    uom = Column(String)  # unit of measurement
    kpgz_piece_id = Column(Integer, ForeignKey("kpgz.id"))
    kpgz_piece = relationship("KpgzPiece")


class KpgzPiece(Base):
    __tablename__ = "kpgz"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,
                  unique=True)  # в данных в названии идет еще и код. Возможно, его нужно выделить в отдельный столбец
