from fastapi import APIRouter, Depends, HTTPException
from app.security import check_for_moderator_permission

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

