from pydantic import BaseModel
from typing import Union, List
from app.database.schemas import HypothesisReturn


class TsnPieceEditIn(BaseModel):
    id: int
    code: Union[str, None] = None
    text: Union[str, None] = None
    price: Union[float, None] = None
    spgz_piece_id: Union[int, None] = None


class TsnPieceCreateIn(BaseModel):
    code: str
    text: str
    price: float
    spgz_piece_id: int


class SmetaLine(BaseModel):
    # userful info
    code: str = "DEFAULT CODE"
    name: str = "DEFAULT NAME"
    uom: str = "DEFAULT UOM"
    amount: int = 123321
    price: float = 123321
    hypothesises: List[HypothesisReturn] = []
    spgz_defined: bool = False

    line_number: int = -1


class SmetaCategory(BaseModel):
    name: str = "DEFAULT CATEGORY NAME"
    lines: List[SmetaLine] = []


class Smeta(BaseModel):
    address: str = "DEFAULT ADDRESS"
    categories: List[SmetaCategory] = []


class PatchPair(BaseModel):
    line_number: int
    spgz_id: int


class PatchSmetaIn(BaseModel):
    patches: List[PatchPair] = []
