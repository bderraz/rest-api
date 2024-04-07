from pydantic import BaseModel


class TvShowDTO(BaseModel):
    """
    :param show_id: Unique identifier for the TV show
    :param type: Type of the TV show (e.g., Movie, Series)
    :param title: Title of the TV show
    :param director: Director of the TV show
    :param cast: Cast of the TV show
    :param country: Country where the TV show was produced
    :param date_added: Date when the TV show was added
    :param release_year: Year when the TV show was released
    :param rating: Rating of the TV show
    :param duration: Duration of the TV show
    """

    show_id: int
    type: str
    genre: str
    title: str
    director: str
    cast: str
    country: str
    date_added: str
    release_year: int
    rating: str
    duration: str


class TvShowInputDTO(BaseModel):
    """
    :param show_id: Unique identifier for the TV show (optional)
    :param type: Type of the TV show (optional)
    :param title: Title of the TV show (optional)
    :param director: Director of the TV show (optional)
    :param cast: Cast of the TV show (optional)
    :param country: Country where the TV show was produced (optional)
    :param date_added: Date when the TV show was added (optional)
    :param release_year: Year when the TV show was released (optional)
    :param rating: Rating of the TV show (optional)
    :param duration: Duration of the TV show (optional)
    """

    show_id: int
    type: str
    genre: str
    title: str
    director: str
    cast: str
    country: str
    date_added: str
    release_year: int
    rating: str
    duration: str
