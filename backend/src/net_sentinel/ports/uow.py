from typing import Protocol

from net_sentinel.ports.audit_repository import AuditRepositoryPort
from net_sentinel.ports.target_repository import TargetRepositoryPort


class UnitOfWorkPort(Protocol):
    audit_repo: AuditRepositoryPort
    target_repo: TargetRepositoryPort

    async def __aenter__(self) -> "UnitOfWorkPort": ...

    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    async def commit(self): ...

    async def rollback(self): ...
