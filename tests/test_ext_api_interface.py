import unittest
from library. ext_api_interface import Books_API
from unittest.mock import Mock
import requests
import json

class TestExtApiInterface(unittest.TestCase):
    def setUp(self):
        self.api = Books_API()
        self.book = "learning python"
        self.author = "Lutz"
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())
        with open('tests_data/json_data.txt', 'r') as f:
            self.json_data = json.loads(f.read())

    def test_make_request_True(self):
        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value = Mock(status_code = 200, **attr))
        self.assertEqual(self.api.make_request(""), dict())

    def test_make_request_False(self):
        requests.get = Mock(return_value=Mock(status_code=100))
        self.assertEqual(self.api.make_request(""), None)

    def test_make_request_error(self):
        requests.get = Mock(side_effect=requests.ConnectionError)
        self.assertEqual(self.api.make_request(""), None)

    def test_is_book_available_true(self):
        self.api.make_request = Mock(return_value=self.json_data)
        self.assertTrue(self.api.is_book_available(self.book))

    def test_is_book_available_false(self):
        self.api.make_request = Mock(return_value="")
        self.assertFalse(self.api.is_book_available(self.book))

    def test_books_by_author_exists(self):
        self.api.make_request = Mock(return_value=self.json_data)
        self.assertNotEqual(self.api.books_by_author(self.author), [])

    def test_books_by_author_does_not_exist(self):
        self.api.make_request = Mock(return_value="")
        self.assertEqual(self.api.books_by_author(self.author), [])

    def test_get_book_info_exists(self):
        self.api.make_request = Mock(return_value=self.json_data)
        self.assertNotEqual(self.api.get_book_info(self.book), [])

    def test_get_book_info_does_not_exist(self):
        self.api.make_request = Mock(return_value="")
        self.assertEqual(self.api.get_book_info(self.book), [])

    def test_get_ebooks_json_format(self):
        self.api.make_request = Mock(return_value=self.json_data)
        self.assertEqual(self.api.get_ebooks(self.book), self.books_data)

    def test_get_ebooks_not_json_format(self):
        self.api.make_request = Mock(return_value="")
        self.assertEqual(self.api.get_ebooks(self.book), [])
