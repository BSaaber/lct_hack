from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from app.security import check_for_moderator_permission
from typing import List
import app.database.api as db_api
import app.database.schemas as db_schemas
from sqlalchemy.orm import Session
from app.database.db_init import get_db
from .schemas import *
from app.database.schemas import TsnPieceEdit  # , TsnPieceCreate
from openpyxl import load_workbook
from . import work_with_smeta
from fastapi.responses import FileResponse
from io import BytesIO
# import aiofiles
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SMETAS_DIR = os.path.join(BASE_DIR, "smetas")


def make_file_path(user_id: int):
    return os.path.join(SMETAS_DIR, str(user_id) + ".xlsx")


router = APIRouter(
    prefix="/sprav",
    tags=["sprav"],
    dependencies=[Depends(check_for_moderator_permission)],
)


@router.post("/parse_smeta/{user_id}", response_model=Smeta)
async def parse_smeta(user_id: int, db: Session = Depends(get_db), file: bytes = File()):
    result = await work_with_smeta.parse_smeta(db, file)
    print("ALL WENT DONE")
    path = make_file_path(user_id)
    print(path)
    with open(path, "wb") as save_file:
        save_file.write(file)
    print("returning result")
    print("\n\n\n")
    print(result)
    print("\n\n\n")
    return result


# TODO хранить имя файла и возвращать с нормальным именем
@router.post("/patch_smeta/{user_id}", response_class=FileResponse)
async def patch_smeta(user_id: int, patches: PatchSmetaIn, db: Session = Depends(get_db)):
    path = make_file_path(user_id)
    filename = str(user_id) + ".xlsx"
    await work_with_smeta.patch_smeta(db, path, patches)
    headers = {f'Content-Disposition': f'attachment; filename="{filename}"'}
    return FileResponse(path=path, headers=headers)  # media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # return FileResponse(BytesIO(file))


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
