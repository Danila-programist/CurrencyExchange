from fastapi import APIRouter

router = APIRouter()

@router.get('/all')
async def get_all_currencies():
    return {"message": "currency endpoint"}