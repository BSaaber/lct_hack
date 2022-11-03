from fastapi import APIRouter, Depends, HTTPException, status
from app.security import check_for_moderator_permission
from typing import List
import app.database.api as db_api
import app.database.schemas as db_schemas
from sqlalchemy.orm import Session
from app.database.db_init import get_db
from .schemas import *
from app.database.schemas import TsnPieceEdit  # , TsnPieceCreate

router = APIRouter(
    prefix="/sprav",
    tags=["sprav"],
    dependencies=[Depends(check_for_moderator_permission)],
)


@router.get("/")  # response_model=
async def sprav_hello(item_id: str):
    # if True:
    #    raise HTTPException(status_code=404, detail="Item not found")
    return "Hello from /sprav/"


@router.get("/tsn", response_model=List[db_schemas.TsnPieceReturn])
async def get_tsn(offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tsn = await db_api.sprav_edit.get_tsn(db, offset, limit)
    return tsn


@router.post("/tsn/edit_one")
async def edit_tsn_piece(update_in: TsnPieceEditIn, db: Session = Depends(get_db)):
    update = TsnPieceEdit(**update_in.dict())
    tsn = await db_api.sprav_edit.edit_tsn_piece(db, update)
    if not tsn:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error")
    return "Ok"

# @router.post("/tsn/create_one")
# async def add_tsn_piece(update_in: TsnPieceCreateIn, db: Session = Depends(get_db)):
#    update = TsnPieceCreate(**update_in.dict())
#    tsn = await db_api.sprav_edit.add_tsn_piece(db, update)
#    if not tsn:
#        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error")
#    return "Ok"


# @router.delete("/tsn/{id}")
# async def add_tsn_piece(id: int, db: Session = Depends(get_db)):
#    res = await db_api.sprav_edit.delete_tsn_piece(db, id)
#    if not res:
#        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="error")
#    return "Ok"
