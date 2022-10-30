from . import engine
from . import db_models # noqa
engine.Base.metadata.create_all(bind=engine.engine_instance)

print("--------------------\n\n\n\n-------------------")


def get_db():
    db = engine.SessionLocal()
    try:
        yield db
    finally:
        db.close()