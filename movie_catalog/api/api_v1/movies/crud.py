from pydantic import BaseModel
from fastapi import status, HTTPException

from schemas.movie_description import (
    MovieDescription,
    MovieDescriptionCreate,
    MovieDescriptionUpdate,
)


class MoviesStorage(BaseModel):
    slug_to_movies: dict[str, MovieDescription] = {}

    def get_list_movies(self) -> list[MovieDescription]:
        return list(self.slug_to_movies.values())

    def get_movies_by_slug(self, slug: str) -> MovieDescription | None:
        result = self.slug_to_movies.get(slug)
        if result:
            return result
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie {slug} not found",
        )

    def create_movies(self, movie_in: MovieDescriptionCreate) -> MovieDescription:
        movie = MovieDescription(
            **movie_in.model_dump(),
        )
        self.slug_to_movies[movie.slug] = movie

        return movie

    def update(
        self,
        movie: MovieDescription,
        movie_in: MovieDescriptionUpdate,
    ):
        for field_name, value in movie_in:
            setattr(movie, field_name, value)

        return movie

    def delete_movies(self, slug: str) -> None:
        self.slug_to_movies.pop(slug, None)

    def delete(self, movie: MovieDescription) -> None:
        self.delete_movies(slug=movie.slug)


storage = MoviesStorage()

storage.create_movies(
    MovieDescriptionCreate(
        slug="krestnyy_otec",
        title="Крестный отец",
        description="""
        Криминальная сага, повествующая о нью-йоркской сицилийской мафиозной семье Корлеоне.
        Фильм охватывает период 1945-1955 годов.
        Глава семьи, Дон Вито Корлеоне, выдаёт замуж свою дочь. В это время со Второй мировой войны возвращается его 
        любимый сын Майкл. Майкл, герой войны, гордость семьи, не выражает желания заняться жестоким семейным бизнесом. 
        Дон Корлеоне ведёт дела по старым правилам, но наступают иные времена, и появляются люди, желающие изменить 
        сложившиеся порядки. На Дона Корлеоне совершается покушение.
        """,
        genre=["Драма", "Криминал"],
        release_year=1972,
    ),
)
storage.create_movies(
    MovieDescriptionCreate(
        slug="belye_rosy",
        title="Белые росы",
        description="""
                Ветеран труда и трех войн, уважаемый человек в деревне Белые росы – Федор Ходас уже давно овдовел и имеет трех 
                взрослых сыновей. Старший чрезмерно расчетлив, младший чересчур весел. Средний уехал на Курилы и каков он теперь
                отцу неведомо. Но за всех у старика душа болит, особенно за младшего балагура.
                """,
        genre=["Драма", "Мелодрама", "Комедия"],
        release_year=1983,
    ),
)
storage.create_movies(
    MovieDescriptionCreate(
        slug="igra_prestolov",
        title="Игра престолов (сериал)",
        description="""
                К концу подходит время благоденствия, и лето, длившееся почти десятилетие, угасает. Вокруг средоточия власти 
                Семи королевств, Железного трона, зреет заговор, и в это непростое время король решает искать поддержки у друга 
                юности Эддарда Старка. В мире, где все — от короля до наемника — рвутся к власти, плетут интриги и готовы 
                вонзить нож в спину, есть место и благородству, состраданию и любви. Между тем никто не замечает пробуждение 
                тьмы из легенд далеко на Севере — и лишь Стена защищает живых к югу от нее.
                """,
        genre=["Драма", "Фэнтези", "Боевик", "Мелодрама", "Приключения"],
        release_year=2011,
    ),
)
storage.create_movies(
    MovieDescriptionCreate(
        slug="ostrov_proklyatyh",
        title="Остров проклятых",
        description="""
                Два американских судебных пристава отправляются на один из островов в штате Массачусетс, чтобы расследовать 
                исчезновение пациентки клиники для умалишенных преступников. При проведении расследования им придется 
                столкнуться с паутиной лжи, обрушившимся ураганом и смертельным бунтом обитателей клиники.
                """,
        genre=["Драма", "Триллер", "Детектив"],
        release_year=2009,
    ),
)
storage.create_movies(
    MovieDescriptionCreate(
        slug="interstellar",
        title="Интерстеллар",
        description="""
                Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису, коллектив 
                исследователей и учёных отправляется сквозь червоточину (которая предположительно соединяет области 
                пространства-времени через большое расстояние) в путешествие, чтобы превзойти прежние ограничения для 
                космических путешествий человека и найти планету с подходящими для человечества условиями.
                """,
        genre=["Драма", "Фантастика", "Приключения"],
        release_year=2014,
    ),
)
