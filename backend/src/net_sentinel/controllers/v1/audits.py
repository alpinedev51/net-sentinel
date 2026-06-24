# Audits router
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from net_sentinel.adapters.db import async_session_maker
from net_sentinel.adapters.uow import SQLAlchemyUnitOfWork
from net_sentinel.ports.uow import UnitOfWorkPort
from net_sentinel.schemas.audit import AuditCreate, AuditResponse
from net_sentinel.services.audit_service import AuditService

router = APIRouter()


def get_uow() -> UnitOfWorkPort:
    """
    Injects the session factory into the UoW.
    The UoW will now safely open and close its own session.
    """
    return SQLAlchemyUnitOfWork(session_factory=async_session_maker)


def get_audit_service(uow: UnitOfWorkPort = Depends(get_uow)) -> AuditService:
    return AuditService(uow=uow)


@router.post("/", response_model=AuditResponse, status_code=status.HTTP_201_CREATED)
async def create_audit(
    payload: AuditCreate, service: AuditService = Depends(get_audit_service)
):
    return await service.register_new_audit(payload)
