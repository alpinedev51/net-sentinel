from typing import List, Protocol

from net_sentinel.schemas.target import TargetCreate, TargetResponse


class TargetRepositoryPort(Protocol):
    """
    The Port: The core application strictly defines WHAT it needs,
    knowing absolutely nothing about SQLAlchemy or the database.
    """

    async def get_by_id(self, target_id: int) -> TargetResponse | None: ...

    async def list_active(self) -> List[TargetResponse]: ...

    async def create(self, target_data: TargetCreate) -> TargetResponse: ...
