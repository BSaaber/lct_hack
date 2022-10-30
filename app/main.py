from fastapi import FastAPI
from .routers import *
from .database import engine  # noqa

app = FastAPI()

app.include_router(auth_router)
app.include_router(smeta_router)
app.include_router(sprav_router)
app.include_router(admin_router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
