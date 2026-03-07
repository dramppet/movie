import unittest
from unittest.mock import patch, Mock
from fastapi import HTTPException

from services.movie_services import (
    create_movie,
    get_movies,
    get_movie_id,
    update_movie,
    delete_movie,
    validate_release_year
)


class TestMovieService(unittest.TestCase):

    @patch("services.movie_services.read_query")
    def test_get_movies_returns_list(self, mock_read):

        mock_read.return_value = [
            {
                "id": 1,
                "title": "Inception",
                "director": "Christopher Nolan",
                "release_year": 2010,
                "rating": 8.8
            }
        ]

        result = get_movies()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Inception")
        mock_read.assert_called_once()


class TestCreateMovie(unittest.TestCase):

    @patch("services.movie_services.insert_query")
    @patch("services.movie_services.validate_release_year")
    @patch("services.movie_services.validate_title")
    def test_create_movie_success(self, mock_title, mock_year, mock_insert):

        mock_insert.return_value = 1

        movie = Mock()
        movie.title = "Interstellar"
        movie.director = "Christopher Nolan"
        movie.release_year = 2014

        result = create_movie(movie)

        self.assertEqual(result["id"], 1)
        self.assertEqual(result["title"], "Interstellar")

        mock_insert.assert_called_once()


class TestGetMovieById(unittest.TestCase):

    @patch("services.movie_services.read_query")
    def test_get_movie_found(self, mock_read):

        mock_read.return_value = [
            {"id": 1, "title": "Inception", "director": "Nolan", "release_year": 2010, "rating": 8.8}
        ]

        result = get_movie_id(1)

        self.assertEqual(result["id"], 1)
        mock_read.assert_called_once()

    @patch("services.movie_services.read_query")
    def test_get_movie_not_found(self, mock_read):

        mock_read.return_value = []

        with self.assertRaises(HTTPException):
            get_movie_id(1)


class TestUpdateMovie(unittest.TestCase):

    @patch("services.movie_services.update_query")
    @patch("services.movie_services.validate_release_year")
    @patch("services.movie_services.validate_title")
    @patch("services.movie_services.get_movie_id")
    def test_update_movie_success(self, mock_get, mock_title, mock_year, mock_update):

        mock_get.return_value = {
            "id": 1,
            "title": "Old",
            "director": "Old Director",
            "release_year": 2000,
            "rating": 7
        }

        movie = Mock()
        movie.title = "New Title"
        movie.director = "New Director"
        movie.release_year = 2010

        result = update_movie(1, movie)

        self.assertEqual(result["title"], "New Title")
        mock_update.assert_called_once()


class TestDeleteMovie(unittest.TestCase):

    @patch("services.movie_services.update_query")
    def test_delete_movie_success(self, mock_update):

        mock_update.return_value = 1

        result = delete_movie(1)

        self.assertEqual(result["message"], "Movie deleted")

    @patch("services.movie_services.update_query")
    def test_delete_movie_not_found(self, mock_update):

        mock_update.return_value = 0

        with self.assertRaises(HTTPException):
            delete_movie(1)


class TestValidateYear(unittest.TestCase):

    def test_validate_release_year_valid(self):

        validate_release_year(2000)

    def test_validate_release_year_invalid(self):

        with self.assertRaises(HTTPException):
            validate_release_year(1700)


if __name__ == "__main__":
    unittest.main()