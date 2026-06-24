from typing import List

from net_sentinel.models.audit import Audit as AuditORM
from net_sentinel.ports.audit_repository import AuditRepositoryPort
from net_sentinel.schemas.audit import AuditCreate, AuditResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyAuditRepository(AuditRepositoryPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, audit_id: int) -> AuditResponse | None:
        result = await self.session.execute(select(AuditORM).where(AuditORM.id == audit_id))
        db_obj = result.scalar_one_or_none()
        return AuditResponse.model_validate(db_obj) if db_obj else None

    async def list_all(self) -> List[AuditResponse]:
        result = await self.session.execute(select(AuditORM))
        return [AuditResponse.model_validate(db_obj) for db_obj in result.scalars().all()]

    async def create(self, audit_data: AuditCreate) -> AuditResponse:
        new_audit = AuditORM(**audit_data.model_dump())
        self.session.add(new_audit)

        await self.session.flush()
        await self.session.refresh(new_audit)

        return AuditResponse.model_validate(new_audit)
