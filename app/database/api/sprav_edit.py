from sqlalchemy.orm import Session
from .. import db_models, schemas


# TODO переназвать файл

# returning None if something goes wrong


async def get_tsn_piece_by_code(db: Session, code: str):
    return db.query(db_models.TsnPiece).filter(db_models.TsnPiece.code == code).first()


async def get_tsn(db: Session, offset: int = 0, limit: int = 100):
    return db.query(db_models.TsnPiece).offset(offset).limit(limit).all()


async def delete_tsn_piece(db: Session, id: int):
    delete_result = db.query(db_models.TsnPiece).filter(db_models.TsnPiece.id == id).delete()
    if delete_result != 1:
        return None
    return delete_result


async def edit_tsn_piece(db: Session, tsn_piece: schemas.TsnPieceEdit):  # двойная запись?
    update = {k: v for k, v in tsn_piece.dict().items() if v is not None}
    if "spgz_piece_id" in update:
        if await get_spgz_piece_by_id(db, update["spgz_piece_id"]) is None:
            return None
    del update["id"]
    db.query(db_models.TsnPiece).filter(db_models.TsnPiece.id == tsn_piece.id).update(update)
    db.commit()
    db.refresh(tsn_piece)
    return tsn_piece


async def add_tsn_piece(db: Session, tsn_piece: schemas.TsnPieceCreate):  # двойная запись?
    new_tsn_piece = db_models.TsnPiece(**tsn_piece.dict())
    if await get_spgz_piece_by_id(db, new_tsn_piece.spgz_piece_id) is None:
        return None
    db.add(new_tsn_piece)
    db.commit()
    db.refresh(new_tsn_piece)
    return new_tsn_piece

async def add_kpgz_piece(db: Session, kpgz_piece: schemas.KpgzPieceCreate):
    new_kpgz_piece = db_models.KpgzPiece(**kpgz_piece.dict())
    db.add(new_kpgz_piece)
    db.commit()
    db.refresh(new_kpgz_piece)
    return new_kpgz_piece

async def get_spgz_piece_by_id(db: Session, id: int):
    return db.query(db_models.SpgzPiece).filter(db_models.SpgzPiece.id == id).first()

async def get_kpgz_piece_by_id(db: Session, id: int):
    return db.query(db_models.KpgzPiece).filter(db_models.KpgzPiece.id == id).first()


async def add_spgz_piece(db: Session, spgz_piece: schemas.SpgzPieceCreate):
    new_spgz_piece = db_models.SpgzPiece(**spgz_piece.dict())
    if await get_kpgz_piece_by_id(db, new_spgz_piece.kpgz_piece_id) is None:
        return None
    db.add(new_spgz_piece)
    db.commit()
    db.refresh(new_spgz_piece)
    return new_spgz_piece


