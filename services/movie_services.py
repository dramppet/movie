from db.connection import read_query, insert_query, update_query
from fastapi import HTTPException
from models.movie_models import MovieUpdate

def create_movie(movie):

    sql = """
    INSERT INTO movies(title,director,release_year)
    VALUES (?,?,?)
    """
    
    validate_title(movie.title)
    validate_release_year(movie.release_year)
    

    movie_id = insert_query(sql, (
        movie.title,
        movie.director,
        movie.release_year
    ))
    
    if not movie_id:
        raise HTTPException(500, "Movie could not be created")

    return {
        "id": movie_id,
        "title": movie.title,
        "director": movie.director,
        "release_year": movie.release_year,
        "rating": None
    }


def get_movies(title=None, sort=None, order="DESC", limit=20, offset=0):
    sql = "SELECT * FROM movies WHERE 1=1"
    params = []

    if title:
        sql += " AND title LIKE ?"
        params.append(f"%{title}%")

    allowed_sort_columns = ["rating", "title", "year", "id"]
    
    if sort in allowed_sort_columns:
        direction = "ASC" if order.upper() == "ASC" else "DESC"
        sql += f" ORDER BY {sort} {direction}"

    sql += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    return read_query(sql, tuple(params))

def get_movie_id(movie_id):

    sql = "SELECT * FROM movies WHERE id=?"

    result = read_query(sql, (movie_id,))

    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")

    return result[0]

def update_movie(movie_id: int, movie: MovieUpdate):

    existing = get_movie_id(movie_id)
    validate_title(movie.title)
    validate_release_year(movie.release_year)
    

    title = movie.title if movie.title is not None else existing["title"]
    director = movie.director if movie.director is not None else existing["director"]
    release_year = movie.release_year if movie.release_year is not None else existing["release_year"]

    sql = """
    UPDATE movies
    SET title=?, director=?, release_year=?
    WHERE id=?
    """
    
    if release_year <= 1888:
        raise HTTPException(status_code=400, detail="Releasy year must by gt 1888")

    update_query(sql, (title, director, release_year, movie_id))

    return {
        "id": movie_id,
        "title": title,
        "director": director,
        "release_year": release_year,
        "rating": existing["rating"]
    }
    
def delete_movie(movie_id):

    sql = "DELETE FROM movies WHERE id=?"
    
    affected = update_query(sql, (movie_id,))
    
    if affected == 0:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return {"message": "Movie deleted"}

def validate_title(title: str):

    sql = """
    SELECT title FROM movies WHERE title = ?
    """

    existings = read_query(sql, (title,))

    if existings:
        raise HTTPException(
            status_code=409,
            detail=f"Film with title {title} already exists"
        )
    
def validate_release_year(release_year: int):

    if release_year < 1888 or release_year > 2026:
        raise HTTPException(
            status_code=400,
            detail=f"Movie year {release_year} must be between 1888 and 2026"
        )