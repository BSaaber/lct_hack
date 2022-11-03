from pydantic import BaseModel
from enum import Enum
from fastapi import HTTPException, status
from typing import Union


class EUserLevel(int, Enum):
    user = 1
    moderator = 2
    admin = 3


def check_user_level(level):
    if level < EUserLevel.user or level > EUserLevel.admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="no such user level")
    return level


class UserBase(BaseModel):
    email: str
    level: int


class UserCreate(UserBase):
    hashed_password: str


class UserReturn(UserBase):
    id: int

    class Config:
        orm_mode = True


class TsnPieceBase(BaseModel):
    code: str
    text: str
    price: int
    spgz_piece_id: int
    uom: str


class TsnPieceCreateWithoutSpgz(BaseModel):
    code: str
    text: str
    price: int
    uom: str


class TsnPieceReturn(TsnPieceBase):
    id: int

    class Config:
        orm_mode = True


class TsnPieceEdit(BaseModel):
    id: int
    code: Union[str, None] = None
    text: Union[str, None] = None
    price: Union[str, None] = None
    spgz_piece_id: Union[int, None] = None


class SpgzPieceCreate(BaseModel):
    name: Union[str, None] = None
    okpd: Union[str, None] = None
    okpd2: str
    uom: str
    description: Union[str, None] = None
    data_id: int
    kpgz_piece_id: int


class KpgzPieceCreate(BaseModel):
    name: str