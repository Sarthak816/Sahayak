from typing import List
from fastapi import APIRouter # pylint: disable=import-error
from pydantic import BaseModel
from .admin import index as admin
from .auth import index as auth
from .ticket import index as ticket

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["AUTHENTICATION"])
router.include_router(admin.router, prefix="/admin", tags=["ADMIN"])
router.include_router(ticket.router, prefix="/ticket", tags=["TICKETS"])
