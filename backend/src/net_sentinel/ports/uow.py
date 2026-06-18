from typing import Protocol

from net_sentinel.ports.target_repository import TargetRepositoryPort


class UnitOfWorkPort(Protocol):
    """
    The Port: The application knows it can start a transaction,
    access repositories, commit, and rollback. It doesn't know HOW.
    """

    target_repo: TargetRepositoryPort

    async def __aenter__(self) -> "UnitOfWorkPort": ...

    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    async def commit(self): ...

    async def rollback(self): ...
