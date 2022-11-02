from pydantic import BaseModel
from typing import Union


class TsnPieceEditIn(BaseModel):
    id: int
    code: Union[str, None] = None
    text: Union[str, None] = None
    price: Union[str, None] = None
    spgz_piece_id: Union[int, None] = None


class TsnPieceCreateIn(BaseModel):
    code: str
    text: str
    price: int
    spgz_piece_id: int
