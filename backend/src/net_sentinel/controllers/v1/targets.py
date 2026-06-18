# Targets router
from fastapi import APIRouter, Depends

from net_sentinel.adapters.db import async_session_maker
from net_sentinel.adapters.uow import SQLAlchemyUnitOfWork
from net_sentinel.ports.uow import UnitOfWorkPort
from net_sentinel.schemas.target import TargetCreate, TargetResponse
from net_sentinel.services.target_service import TargetService

router = APIRouter()


def get_uow() -> UnitOfWorkPort:
    """
    Injects the session factory into the UoW.
    The UoW will now safely open and close its own session.
    """
    return SQLAlchemyUnitOfWork(session_factory=async_session_maker)


def get_target_service(uow: UnitOfWorkPort = Depends(get_uow)) -> TargetService:
    return TargetService(uow=uow)


@router.post("/", response_model=TargetResponse)
async def create_target(
    payload: TargetCreate, service: TargetService = Depends(get_target_service)
):
    return await service.register_new_target(payload)
