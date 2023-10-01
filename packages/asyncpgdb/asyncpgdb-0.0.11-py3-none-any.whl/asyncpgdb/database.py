from typing import Any, Optional, Type, TypeVar
from logging import Logger
from asyncpgdb.asyncpg import ConnectionAsyncpg, create_pool
from asyncpgdb.execute import ExecuteProtocol
from asyncpgdb.settings import Settings

T = TypeVar("T")


class Database(ExecuteProtocol):
    def __init__(
        self,
        dsn: str,
        min_size: int = 2,
        max_size: int = 60,
        command_timeout: int = 60,
        max_queries: int = 50000,
        max_inactive_connection_lifetime: float = 300,
        setup: Optional[Any] = None,
        init: Optional[Any] = None,
        loop: Optional[Any] = None,
        connection_class: Type[ConnectionAsyncpg] = ConnectionAsyncpg,
        record_class: Optional[Type] = None,
        logger: Optional[Logger] = None,
        ssl: Optional[str] = None,  # ("require",)
        **connect_kwargs: Any,
    ):
        self._settings = Settings(
            dsn=dsn,
            min_size=min_size,
            max_size=max_size,
            command_timeout=command_timeout,
            max_queries=max_queries,
            max_inactive_connection_lifetime=max_inactive_connection_lifetime,
            setup=setup,
            init=init,
            loop=loop,
            connection_class=connection_class,
            record_class=record_class,
            ssl=ssl,
        )
        self._connect_kwargs = self._settings.database_connect_kwargs()
        self._pool = None
        self._logger = logger

    def _log_exception(self, *args):
        if self._logger is not None:
            self._logger.exception(*args)

    async def connect(self):
        if not self._pool:
            try:
                self._pool = await create_pool(**self._connect_kwargs())
                self.log_info("Database pool connection opened")

            except Exception as err:
                self._log_exception(err)

    async def acquire_connection(self) -> ConnectionAsyncpg:
        try:
            await self.connect()
            result = await self._pool.acquire()
            if not isinstance(result, ConnectionAsyncpg):
                raise ValueError(
                    f"pool connection is not asyncpg.connection.Connection; {str(type(result))}"
                )
        except Exception as error:
            self._log_exception(f"Error creating connection:", error)

        return result

    async def release(self, __conn: ConnectionAsyncpg):
        await self._pool.release(__conn)

    async def close(self):
        if not self._pool:
            try:
                await self._pool.close()
                self.log_info("Database pool connection closed")
            except Exception as err:
                self._log_exception(err)
