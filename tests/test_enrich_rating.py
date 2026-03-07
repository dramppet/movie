import unittest
from unittest.mock import patch, Mock

from services.rating_service import enrich_movie_rating


class TestEnrichMovieRating(unittest.TestCase):

    @patch("services.rating_service.update_query")
    @patch("services.rating_service.requests.get")
    @patch("services.rating_service.API_KEY", "fake_key")
    def test_enrich_rating_success(self, mock_get, mock_update):

        mock_response = Mock()
        mock_response.json.return_value = {
            "Response": "True",
            "imdbRating": "8.8"
        }
        mock_response.raise_for_status.return_value = None

        mock_get.return_value = mock_response

        enrich_movie_rating(1, "Inception")

        mock_update.assert_called_once()

    @patch("services.rating_service.requests.get")
    @patch("services.rating_service.API_KEY", "fake_key")
    def test_no_rating_found(self, mock_get):

        mock_response = Mock()
        mock_response.json.return_value = {
            "Response": "False"
        }
        mock_response.raise_for_status.return_value = None

        mock_get.return_value = mock_response

        enrich_movie_rating(1, "Unknown")

    @patch("services.rating_service.API_KEY", None)
    def test_missing_api_key(self):

        enrich_movie_rating(1, "Inception")

    @patch("services.rating_service.requests.get")
    @patch("services.rating_service.API_KEY", "fake_key")
    def test_api_exception(self, mock_get):

        mock_get.side_effect = Exception("API error")

        enrich_movie_rating(1, "Inception")


if __name__ == "__main__":
    unittest.main()