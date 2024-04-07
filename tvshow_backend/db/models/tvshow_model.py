from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import Date, Integer, String

from tvshow_backend.db.base import Base


class TvShowModel(Base):
    __tablename__ = "tvshow_model"

    show_id: Mapped[int] = mapped_column(String, primary_key=True)
    type: Mapped[str] = mapped_column(String)
    genre: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    director: Mapped[str] = mapped_column(String)
    cast: Mapped[str] = mapped_column(String)
    country: Mapped[str] = mapped_column(String)
    date_added: Mapped[Date] = mapped_column(String)
    release_year: Mapped[int] = mapped_column(Integer)
    rating: Mapped[str] = mapped_column(String)
    duration: Mapped[str] = mapped_column(String)
