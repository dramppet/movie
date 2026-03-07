import requests
import os
import logging

from db.connection import update_query

logger = logging.getLogger(__name__)

API_KEY = os.getenv("OMDB_API_KEY")


def enrich_movie_rating(movie_id: int, title: str):

    if not API_KEY:
        logger.error("OMDB_API_KEY is missing from environment variables")
        return

    try:
        logger.info(f"Fetching rating for movie: {title}")

        response = requests.get(
            "http://www.omdbapi.com/",
            params={"t": title, "apikey": API_KEY},
            timeout=10
        )

        response.raise_for_status()

        data = response.json()
        print(data)

        if data.get("Response") == "True":

            rating = data.get("imdbRating")

            if rating and rating != "N/A":

                rating = float(rating)

                sql = """
                UPDATE movies
                SET rating = ?
                WHERE id = ?
                """

                update_query(sql, (rating, movie_id))

                logger.info(f"Rating updated for movie {movie_id}: {rating}")
            print("OMDB RESPONSE:", data)

        else:
            logger.warning(f"No rating found for movie: {title}")

    except Exception as e:
        logger.error(f"Rating enrichment failed for '{title}': {e}")