from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from sqlalchemy.exc import NoResultFound

from tvshow_backend.db.dao.tvshow_dao import TvShowDAO
from tvshow_backend.db.models.tvshow_model import TvShowModel
from tvshow_backend.web.api.tvshow.schema import TvShowDTO, TvShowInputDTO

router = APIRouter()


@router.post("/create")
async def create_tvshow(
    new_tvshow_object: TvShowInputDTO,
    tvshow_dao: TvShowDAO = Depends(),
) -> None:
    """
    Creates tvshow in the database.

    :param new_tvshow_object: new tvshow model item.
    :param tvshow_dao: DAO for tvshow models.
    """
    try:
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
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


# Retrieve all TV shows.
@router.get("/all", response_model=List[TvShowDTO])
async def retrieve_tvshow(
    limit: int = 10,
    offset: int = 0,
    tvshow_dao: TvShowDAO = Depends(),
) -> List[TvShowModel]:
    """
    Retrieve all tvshow objects from the database.

    :param limit: limit of tvshow objects, defaults to 10.
    :param offset: offset of tvshow objects, defaults to 0.
    :param tvshow_dao: DAO for tvshow models.
    :return: list of tvshow objects from database.
    """

    try:
        return await tvshow_dao.get_all_tv_shows(limit=limit, offset=offset)
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred while retrieving all TV shows: {str(e)}",
        )


# Retrieve a single TV show by its ID.
@router.get("/detail/{show_id}", response_model=TvShowDTO)
async def retrieve_tvshow_by_id(
    show_id: int,
    tvshow_dao: TvShowDAO = Depends(),
) -> TvShowModel:
    """
    Retrieve tvshow object from the database.

    :param show_id: show_id of tvshow object.
    :param tvshow_dao: DAO for tvshow models.
    :return: tvshow object from database.
    """
    try:
        return await tvshow_dao.get_tv_show_by_id(show_id=show_id)
    except NoResultFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred while retrieving a TV show: {str(e)}",
        )


# Search TV show by genre.
@router.get("/genre/{genre}", response_model=List[TvShowDTO])
async def retrieve_tvshow_by_genre(
    genre: str,
    tvshow_dao: TvShowDAO = Depends(),
) -> List[TvShowModel]:
    """
    Retrieve tvshow objects from the database by genre.

    :param genre: genre of tvshow object.
    :param tvshow_dao: DAO for tvshow models.
    :return: list of tvshow objects from database.
    """
    try:
        return await tvshow_dao.search_tv_show_by_genre(genre=genre)
    except NoResultFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred while retrieving a TV show: {str(e)}",
        )


# Update an existing TV show.
@router.put("/update/{show_id}")
async def update_tvshow(
    show_id: int,
    updated_tvshow_object: TvShowInputDTO,
    tvshow_dao: TvShowDAO = Depends(),
) -> None:
    """
    Update tvshow object in the database.

    :param show_id: show_id of tvshow object.
    :param updated_tvshow_object: updated tvshow model item.
    :param tvshow_dao: DAO for tvshow models.
    """
    try:
        await tvshow_dao.update_tv_show_model(
            show_id=show_id,
            type=updated_tvshow_object.type,
            genre=updated_tvshow_object.genre,
            title=updated_tvshow_object.title,
            director=updated_tvshow_object.director,
            cast=updated_tvshow_object.cast,
            country=updated_tvshow_object.country,
            date_added=updated_tvshow_object.date_added,
            release_year=updated_tvshow_object.release_year,
            rating=updated_tvshow_object.rating,
            duration=updated_tvshow_object.duration,
        )

    except NoResultFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred while updating a TV show: {str(e)}",
        )


# Delete a TV show by its ID.
@router.delete("/delete/{show_id}")
async def delete_tvshow(
    show_id: int,
    tvshow_dao: TvShowDAO = Depends(),
) -> None:
    """
    Delete tvshow object from the database.

    :param show_id: show_id of tvshow object.
    :param tvshow_dao: DAO for tvshow models.
    """
    try:
        await tvshow_dao.delete_tv_show_model(show_id=show_id)
    except NoResultFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred while deleting a TV show: {str(e)}",
        )
