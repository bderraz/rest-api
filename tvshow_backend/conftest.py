import random
from typing import Any, AsyncGenerator, Generator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from tvshow_backend.db.dependencies import get_db_session
from tvshow_backend.db.utils import create_database, drop_database
from tvshow_backend.settings import settings
from tvshow_backend.web.api.tvshow.schema import TvShowInputDTO
from tvshow_backend.web.application import get_app


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


# Create a fixture for the TvShowInputDTO
@pytest.fixture
def new_tvshow_object() -> Generator[TvShowInputDTO, None, None]:
    test_show_id = random.randint(1, 1000000)
    return TvShowInputDTO(
        show_id=test_show_id,
        type="Test Type",
        genre="Test Genre",
        title="Test Title",
        director="Test Director",
        cast="Test Cast",
        country="Test Country",
        date_added="2022-01-01",
        release_year=2022,
        rating="Test Rating",
        duration="Test Duration",
    )


@pytest.fixture(scope="session")
async def _engine() -> AsyncGenerator[AsyncEngine, None]:
    """
    Create engine and databases.

    :yield: new engine.
    """
    from tvshow_backend.db.meta import meta  # noqa: WPS433
    from tvshow_backend.db.models import load_all_models  # noqa: WPS433

    load_all_models()

    await create_database()

    engine = create_async_engine(str(settings.db_url))
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

    try:
        yield engine
    finally:
        await engine.dispose()
        await drop_database()


@pytest.fixture
async def dbsession(
    _engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """
    Get session to database.

    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.

    :param _engine: current engine.
    :yields: async session.
    """
    connection = await _engine.connect()
    trans = await connection.begin()

    session_maker = async_sessionmaker(
        connection,
        expire_on_commit=False,
    )
    session = session_maker()

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()


@pytest.fixture
def fastapi_app(
    dbsession: AsyncSession,
) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_db_session] = lambda: dbsession
    return application  # noqa: WPS331


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac
