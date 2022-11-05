from pydantic import BaseModel
from typing import Union, List


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


class SpgzHypothesis(BaseModel):
    # userful info
    name: str = "DEFAULT NAME"
    kpgz_name: str = "DEFAULT NAME"

    id: int = -1  # db id


class SmetaLine(BaseModel):
    # userful info
    code: str = "DEFAULT CODE"
    name: str = "DEFAULT NAME"
    uom: str = "DEFAULT UOM"
    amount: int = 123321
    cost_per_unit: int = 123321
    price: int = 123321
    hypothesises: List[SpgzHypothesis] = []
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
