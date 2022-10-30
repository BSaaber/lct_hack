from fastapi import APIRouter, Depends, HTTPException
from app.security import check_for_user_permission
# from ..dependencies import get_token_header

router = APIRouter(
    prefix="/smeta",
    tags=["smeta"],
    dependencies=[Depends(check_for_user_permission)],
)


@router.get("/")  # response_model=
async def smeta_hello(item_id: str):
    # if True:
    #    raise HTTPException(status_code=404, detail="Item not found")
    return "Hello from /smeta/"

