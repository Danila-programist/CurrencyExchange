from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def get_currency():
    return {"message": "currency endpoint"}