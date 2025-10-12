from typing import List
from fastapi import APIRouter # pylint: disable=import-error
from pydantic import BaseModel

router = APIRouter()

@router.get("/")
async def get_users():
    return "Admin"
