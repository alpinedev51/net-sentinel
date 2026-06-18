# Master router combining versions
from fastapi import APIRouter

from net_sentinel.controllers.v1.targets import router as targets_v1

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(targets_v1, prefix="/targets", tags=["Targets"])
