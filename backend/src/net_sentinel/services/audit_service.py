# Coordinates auditing pipelines
from net_sentinel.ports.uow import UnitOfWorkPort
from net_sentinel.schemas.audit import AuditCreate, AuditResponse


class AuditService:
    def __init__(self, uow: UnitOfWorkPort):
        self.uow = uow

    async def register_new_audit(self, target_in: AuditCreate) -> AuditResponse:
        async with self.uow:
            new_target = await self.uow.audit_repo.create(target_in)
            await self.uow.commit()
            return new_target
