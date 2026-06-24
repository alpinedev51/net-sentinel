from typing import List

from net_sentinel.models.target import Target as TargetORM
from net_sentinel.ports.target_repository import TargetRepositoryPort
from net_sentinel.schemas.target import TargetCreate, TargetResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyTargetRepository(TargetRepositoryPort):
    """
    The Adapter: This class physically implements the Port's contract
    using your specific database technology (SQLAlchemy).
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, target_id: int) -> TargetResponse | None:
        result = await self.session.execute(
            select(TargetORM).where(TargetORM.id == target_id)
        )
        db_obj = result.scalar_one_or_none()
        return TargetResponse.model_validate(db_obj) if db_obj else None

    async def list_active(self) -> List[TargetResponse]:
        result = await self.session.execute(
            select(TargetORM).where(TargetORM.is_active)
        )
        return [
            TargetResponse.model_validate(db_obj) for db_obj in result.scalars().all()
        ]

    async def create(self, target_data: TargetCreate) -> TargetResponse:
        new_target = TargetORM(**target_data.model_dump())
        self.session.add(new_target)

        await self.session.flush()
        await self.session.refresh(new_target)

        return TargetResponse.model_validate(new_target)
