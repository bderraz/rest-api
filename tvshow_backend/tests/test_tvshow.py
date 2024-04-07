import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from tvshow_backend.db.dao.tvshow_dao import TvShowDAO
from tvshow_backend.web.api.tvshow.schema import TvShowInputDTO


@pytest.mark.anyio
async def test_create_tvshow_model(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    new_tvshow_object: TvShowInputDTO,  # Use the fixture here
) -> None:
    """Tests TV show model creation."""
    url = fastapi_app.url_path_for("create_tvshow")
    response = await client.post(  # Change this line
        url,
        json=new_tvshow_object.model_dump(),
    )
    assert response.status_code == status.HTTP_200_OK
    tvshow_dao = TvShowDAO(dbsession)
    instances = await tvshow_dao.filter(show_id=new_tvshow_object.show_id)
    assert int(instances[0].show_id) == new_tvshow_object.show_id


# TEST GET TV SHOW BY TYPE
@pytest.mark.anyio
async def test_search_tvshow_by_genre(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    new_tvshow_object: TvShowInputDTO,  # Use the fixture here
) -> None:
    """Tests TV show search by type."""
    tvshow_dao = TvShowDAO(dbsession)

    await tvshow_dao.create_tv_show_model(
        show_id=new_tvshow_object.show_id,
        type=new_tvshow_object.type,
        genre=new_tvshow_object.genre,
        title=new_tvshow_object.title,
        director=new_tvshow_object.director,
        cast=new_tvshow_object.cast,
        country=new_tvshow_object.country,
        date_added=new_tvshow_object.date_added,
        release_year=new_tvshow_object.release_year,
        rating=new_tvshow_object.rating,
        duration=new_tvshow_object.duration,
    )

    # Now, search the TV show by type
    url = fastapi_app.url_path_for(
        "retrieve_tvshow_by_genre",
        genre=new_tvshow_object.genre,
    )
    response = await client.get(url)

    # Check that the search was successful
    assert response.status_code == status.HTTP_200_OK

    # Retrieve the TV show from the response
    tvshows = response.json()

    # Check that the TV show was indeed found
    assert len(tvshows) > 0
    assert tvshows[0]["type"] == new_tvshow_object.type


# TEST UPDATE TV SHOW
@pytest.mark.anyio
async def test_update_tvshow_model(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    new_tvshow_object: TvShowInputDTO,  # Use the fixture here
) -> None:
    """Tests TV show model update."""
    tvshow_dao = TvShowDAO(dbsession)

    await tvshow_dao.create_tv_show_model(
        show_id=new_tvshow_object.show_id,
        type=new_tvshow_object.type,
        genre=new_tvshow_object.genre,
        title=new_tvshow_object.title,
        director=new_tvshow_object.director,
        cast=new_tvshow_object.cast,
        country=new_tvshow_object.country,
        date_added=new_tvshow_object.date_added,
        release_year=new_tvshow_object.release_year,
        rating=new_tvshow_object.rating,
        duration=new_tvshow_object.duration,
    )

    # Now, update the TV show model
    updated_tvshow_object = TvShowInputDTO(
        show_id=new_tvshow_object.show_id,
        type="Updated Test Type",
        genre="Updated Test Genre",
        title="Updated Test Title",
        director="Updated Test Director",
        cast="Updated Test Cast",
        country="Updated Test Country",
        date_added="2022-02-02",
        release_year=2023,
        rating="Updated Test Rating",
        duration="Updated Test Duration",
    )
    url = fastapi_app.url_path_for(
        "update_tvshow",
        show_id=new_tvshow_object.show_id,
    )
    response = await client.put(
        url,
        json=updated_tvshow_object.model_dump(),
    )

    # Check that the update was successful
    assert response.status_code == status.HTTP_200_OK

    # Retrieve the updated TV show model
    instances = await tvshow_dao.filter(show_id=new_tvshow_object.show_id)

    # Check that the TV show model was indeed updated
    assert instances[0].type == "Updated Test Type"
    assert instances[0].genre == "Updated Test Genre"
    assert instances[0].title == "Updated Test Title"
    assert instances[0].director == "Updated Test Director"
    assert instances[0].cast == "Updated Test Cast"
    assert instances[0].country == "Updated Test Country"
    assert instances[0].date_added == "2022-02-02"
    assert instances[0].release_year == 2023
    assert instances[0].rating == "Updated Test Rating"
    assert instances[0].duration == "Updated Test Duration"


# TEST DELETE TV SHOW
@pytest.mark.anyio
async def test_delete_tvshow_model(
    fastapi_app: FastAPI,
    client: AsyncClient,
    dbsession: AsyncSession,
    new_tvshow_object: TvShowInputDTO,  # Use the fixture here
) -> None:
    """Tests TV show model deletion."""
    # First, create a new TV show model to delete
    tvshow_dao = TvShowDAO(dbsession)

    await tvshow_dao.create_tv_show_model(
        show_id=new_tvshow_object.show_id,
        type=new_tvshow_object.type,
        genre=new_tvshow_object.genre,
        title=new_tvshow_object.title,
        director=new_tvshow_object.director,
        cast=new_tvshow_object.cast,
        country=new_tvshow_object.country,
        date_added=new_tvshow_object.date_added,
        release_year=new_tvshow_object.release_year,
        rating=new_tvshow_object.rating,
        duration=new_tvshow_object.duration,
    )

    # Now, delete the TV show model
    url = fastapi_app.url_path_for(
        "delete_tvshow",
        show_id=new_tvshow_object.show_id,
    )
    response = await client.delete(url)

    # Check that the deletion was successful
    assert response.status_code == status.HTTP_200_OK

    # Try to retrieve the deleted TV show model
    instances = await tvshow_dao.filter(show_id=new_tvshow_object.show_id)

    # Check that the TV show model was indeed deleted
    assert len(instances) == 0
