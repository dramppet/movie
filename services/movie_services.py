from db.connection import read_query, insert_query, update_query


def create_movie(title: str, director: str, release_year: int):

    sql = """
        INSERT INTO movies (title, director, release_year)
        VALUES (?, ?, ?)
    """

    movie_id = insert_query(sql, (title, director, release_year))

    return get_movie_by_id(movie_id)


def get_all_movies(title: str | None = None, sort_by_rating: bool = False):

    sql = "SELECT * FROM movies"
    params = []

    if title:
        sql += " WHERE title LIKE ?"
        params.append(f"%{title}%")

    if sort_by_rating:
        sql += " ORDER BY rating DESC"

    return read_query(sql, tuple(params))


def get_movie_by_id(movie_id: int):

    sql = "SELECT * FROM movies WHERE id = ?"

    result = read_query(sql, (movie_id,))

    if result:
        return result[0]

    return None


def update_movie(movie_id: int, title=None, director=None, release_year=None):

    fields = []
    params = []

    if title:
        fields.append("title = ?")
        params.append(title)

    if director:
        fields.append("director = ?")
        params.append(director)

    if release_year:
        fields.append("release_year = ?")
        params.append(release_year)

    if not fields:
        return False

    sql = f"""
        UPDATE movies
        SET {', '.join(fields)}
        WHERE id = ?
    """

    params.append(movie_id)

    return update_query(sql, tuple(params))


def delete_movie(movie_id: int):

    sql = "DELETE FROM movies WHERE id = ?"

    return update_query(sql, (movie_id,))