from fastapi import APIRouter

from app.api.schemas import UserRequest
from app.db.db_utils import get_db

router = APIRouter()

@router.post('/register')
async def register(user: UserRequest):
    ...


@router.post('login')
async def login():
    ...