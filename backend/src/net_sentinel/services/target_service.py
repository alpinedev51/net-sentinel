# Coordinate target actions
from net_sentinel.ports.uow import UnitOfWorkPort
from net_sentinel.schemas.target import TargetCreate, TargetResponse


class TargetService:
    def __init__(self, uow: UnitOfWorkPort):
        self.uow = uow

    async def register_new_target(self, target_in: TargetCreate) -> TargetResponse:
        async with self.uow:
            new_target = await self.uow.target_repo.create(target_in)
            await self.uow.commit()
            return new_target
