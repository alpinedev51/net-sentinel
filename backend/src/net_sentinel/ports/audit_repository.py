from typing import List, Protocol

from net_sentinel.schemas.audit import AuditCreate, AuditResponse


class AuditRepositoryPort(Protocol):
    async def get_by_id(self, audit_id: int) -> AuditResponse | None: ...

    async def list_all(self) -> List[AuditResponse]: ...

    async def create(self, audit_data: AuditCreate) -> AuditResponse: ...
