from fastapi import APIRouter

router = APIRouter()

@router.get('/all')
async def get_currency():
    return {"message": "currency endpoint"}