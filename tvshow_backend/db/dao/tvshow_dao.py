from typing import List, Optional

from fastapi import Depends
from sqlalchemy import delete, func, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from tvshow_backend.db.dependencies import get_db_session
from tvshow_backend.db.models.tvshow_model import TvShowModel


class TvShowDAO:
    """Class for accessing TV Show table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    async def create_tv_show_model(
        self,
        show_id: int,
        type: str,
        genre: str,
        title: str,
        director: str,
        cast: str,
        country: str,
        date_added: str,
        release_year: int,
        rating: str,
        duration: str,
    ) -> None:
        """
        Add single TV Show to session.

        :param show_id: Unique ID for every Movie / Tv Show
        :param type: Identifier - A Movie or TV Show
        :param genre: Genre of the Movie / Tv Show
        :param title: Title of the Movie / Tv Show
        :param director: Director of the Movie
        :param cast: Actors involved in the movie / show
        :param country: Country where the movie / show was produced
        :param date_added: Date it was released
        :param release_year: Actual Release year of the move / show
        :param rating: TV Rating of the movie / show
        :param duration: Total Duration - in minutes or number of seasons
        """
        # Check if the TV show with the given ID already exists
        existing_show = await self.session.execute(
            select(TvShowModel).where(TvShowModel.show_id == show_id),
        )
        if existing_show.scalars().first():
            raise ValueError("A TV show with this ID already exists.")

        self.session.add(
            TvShowModel(
                show_id=show_id,
                type=type,
                genre=genre,
                title=title,
                director=director,
                cast=cast,
                country=country,
                date_added=date_added,
                release_year=release_year,
                rating=rating,
                duration=duration,
            ),
        )

    async def get_all_tv_shows(self, limit: int, offset: int) -> List[TvShowModel]:
        """
        Get all TV Show models with limit/offset pagination.

        :param limit: limit of TV Shows.
        :param offset: offset of TV Shows.
        :return: stream of TV Shows.
        """
        # Get the total count of TV shows
        total_count = await self.session.execute(
            select(func.count()).select_from(TvShowModel),
        )
        total_count = total_count.scalar_one()

        # Check if limit is greater than total count, if so, set limit to total count to avoid throwing an error
        if limit > total_count:
            limit = total_count

        raw_tv_shows = await self.session.execute(
            select(TvShowModel).limit(limit).offset(offset),
        )
        found_tv_shows = list(raw_tv_shows.scalars().fetchall())
        if not found_tv_shows:
            raise NoResultFound("No TV shows found in the database.")
        return found_tv_shows

    async def get_tv_show_by_id(self, show_id: int) -> TvShowModel:
        """
        Get specific TV Show model.

        :param show_id: show_id of TV Show instance.
        :return: TV Show model.
        """
        raw_tv_show = await self.session.execute(
            select(TvShowModel).where(TvShowModel.show_id == show_id),
        )
        found_tv_show = raw_tv_show.scalars().first()
        if found_tv_show is None:
            raise NoResultFound(f"No TV show found with ID {show_id}")
        return found_tv_show

    async def search_tv_show_by_genre(self, genre: str) -> List[TvShowModel]:
        """
        Get specific TV Show model.

        :param genre: genre of TV Show instance.
        :return: TV Show model.
        """
        raw_tv_show = await self.session.execute(
            select(TvShowModel).where(TvShowModel.genre == genre),
        )
        found_tv_show = list(raw_tv_show.scalars().fetchall())
        if not found_tv_show:
            raise NoResultFound(f"No TV shows found with genre {genre}")
        return found_tv_show

    async def update_tv_show_model(
        self,
        show_id: int,
        type: str,
        genre: str,
        title: str,
        director: str,
        cast: str,
        country: str,
        date_added: str,
        release_year: int,
        rating: str,
        duration: str,
    ) -> None:
        """
        Update specific TV Show model.

        :param show_id: show_id of TV Show instance.
        :param type: Identifier - A Movie or TV Show
        :param genre: Genre of the Movie / Tv Show
        :param title: Title of the Movie / Tv Show
        :param director: Director of the Movie
        :param cast: Actors involved in the movie / show
        :param country: Country where the movie / show was produced
        :param date_added: Date it was released
        :param release_year: Actual Release year of the move / show
        :param rating: TV Rating of the movie / show
        :param duration: Total Duration - in minutes or number of seasons
        """

        # Check if the TV show with the given ID exists
        found_tv_show = await self.session.execute(
            select(TvShowModel).where(TvShowModel.show_id == show_id),
        )
        if not found_tv_show.scalars().first():
            raise NoResultFound(
                f"Could not update, TV show with ID {show_id} not found",
            )

        await self.session.execute(
            update(TvShowModel)
            .where(TvShowModel.show_id == show_id)
            .values(
                type=type,
                genre=genre,
                title=title,
                director=director,
                cast=cast,
                country=country,
                date_added=date_added,
                release_year=release_year,
                rating=rating,
                duration=duration,
            ),
        )

    async def delete_tv_show_model(self, show_id: int) -> None:
        """
        Delete specific TV Show model.

        :param show_id: show_id of TV Show instance.
        """
        # Execute the delete operation and get the result
        found_tv_show = await self.session.execute(
            delete(TvShowModel).where(TvShowModel.show_id == show_id),
        )

        # If no rows were deleted, it means no TV show with the given ID exists
        if found_tv_show.rowcount == 0:
            raise NoResultFound(f"No TV show found with ID {show_id}")

    async def filter(self, show_id: Optional[int] = None) -> List[TvShowModel]:
        """
        Get specific TV Show model.

        :param show_id: show_id of TV Show instance.
        :return: TV Show model.
        """
        query = select(TvShowModel)
        if show_id:
            query = query.where(TvShowModel.show_id == show_id)
        found_tv_shows = await self.session.execute(query)
        return list(found_tv_shows.scalars().fetchall())
