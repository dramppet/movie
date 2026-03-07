import unittest
from unittest.mock import patch, Mock
from fastapi import HTTPException

from services.user_service import (
    get_by_username,
    register,
    login,
    promote_to_admin,
    demote_admin
)

class TestRegister(unittest.TestCase):

    @patch("services.user_service.create_user")
    @patch("services.user_service.hash_pass")
    @patch("services.user_service.get_users_count")
    @patch("services.user_service.get_by_username")
    def test_register_success(self, mock_get, mock_count, mock_hash, mock_create):
        mock_get.return_value = None
        mock_count.return_value = 1
        mock_hash.return_value = "hashed_password"

        user = Mock()
        user.username = "test"
        user.password = "123"

        result = register(user)

        self.assertEqual(result["message"], "User registered successfully")
        mock_create.assert_called_once()

    @patch("services.user_service.get_by_username")
    def test_register_existing_user(self, mock_get):
        mock_get.return_value = {"username": "test"}

        user = Mock()
        user.username = "test"
        user.password = "123"

        with self.assertRaises(HTTPException):
            register(user)


class TestLogin(unittest.TestCase):

    @patch("services.user_service.create_jwt")
    @patch("services.user_service.check_pass")
    @patch("services.user_service.get_by_username")
    def test_login_success(self, mock_get, mock_check, mock_jwt):
        mock_get.return_value = {
            "username": "test",
            "password_hash": "hash",
            "role_id": 2
        }
        mock_check.return_value = True
        mock_jwt.return_value = "token123"

        form = Mock()
        form.username = "test"
        form.password = "123"

        result = login(form)

        self.assertEqual(result["access_token"], "token123")

    @patch("services.user_service.get_by_username")
    def test_login_user_not_found(self, mock_get):
        mock_get.return_value = None

        form = Mock()
        form.username = "test"
        form.password = "123"

        with self.assertRaises(HTTPException):
            login(form)

    @patch("services.user_service.check_pass")
    @patch("services.user_service.get_by_username")
    def test_login_wrong_password(self, mock_get, mock_check):
        mock_get.return_value = {
            "username": "test",
            "password_hash": "hash",
            "role_id": 2
        }
        mock_check.return_value = False

        form = Mock()
        form.username = "test"
        form.password = "wrong"

        with self.assertRaises(HTTPException):
            login(form)


class TestPromoteAdmin(unittest.TestCase):

    @patch("services.user_service.update_query")
    @patch("services.user_service.get_by_id")
    def test_promote_success(self, mock_get, mock_update):
        mock_get.return_value = {"id": 2, "role_id": 2}

        result = promote_to_admin(2)

        self.assertEqual(result["message"], "User promoted to ADMIN")
        mock_update.assert_called_once()

    @patch("services.user_service.get_by_id")
    def test_promote_user_not_found(self, mock_get):
        mock_get.return_value = None

        with self.assertRaises(HTTPException):
            promote_to_admin(2)

    @patch("services.user_service.get_by_id")
    def test_promote_already_admin(self, mock_get):
        mock_get.return_value = {"id": 2, "role_id": 1}

        with self.assertRaises(HTTPException):
            promote_to_admin(2)


class TestDemoteAdmin(unittest.TestCase):

    @patch("services.user_service.update_query")
    @patch("services.user_service.get_by_id")
    def test_demote_success(self, mock_get, mock_update):
        mock_get.return_value = {"id": 2, "role_id": 1}

        result = demote_admin(2)

        self.assertEqual(result["message"], "Admin rights removed")
        mock_update.assert_called_once()

    @patch("services.user_service.get_by_id")
    def test_demote_user_not_found(self, mock_get):
        mock_get.return_value = None

        with self.assertRaises(HTTPException):
            demote_admin(2)

    @patch("services.user_service.get_by_id")
    def test_demote_super_user(self, mock_get):
        mock_get.return_value = {"id": 1, "role_id": 1}

        with self.assertRaises(HTTPException):
            demote_admin(1)


if __name__ == "__main__":
    unittest.main()