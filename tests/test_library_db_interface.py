import unittest
from library.patron import Patron
from unittest.mock import Mock, call, patch,MagicMock
from library import library_db_interface
class TestLibbraryDBInterface(unittest.TestCase):

    def setUp(self):
        library_db_interface.TinyDB = Mock()
        #library_db_interface.Patron = Mock()
        library_db_interface.Query = Mock()

        self.db_interface = library_db_interface.Library_DB()

    def test_insert_patron_not_in_db(self):
        patron_mock = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=None)
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        self.db_interface.db.insert = Mock(return_value=10)
        self.assertEqual(self.db_interface.insert_patron(patron_mock), 10)

    def test_insert_patron_in_db(self):
        patron_mock = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=1)
        self.assertEqual(self.db_interface.insert_patron(patron_mock), None)

    def test_insert_not_patron(self):
        self.assertEqual(self.db_interface.insert_patron(None),None)

    def test_get_patron_count(self):
        mock_db = MagicMock()
        mock_db.all.return_value = []
        self.db_interface.db = mock_db
        self.assertEqual(self.db_interface.get_patron_count(), 0)

    def test_get_all_patrons(self):

        mock_db = MagicMock()
        mock_db.all.return_value = []
        self.db_interface.db = mock_db
        self.assertEqual(self.db_interface.get_all_patrons(), [])


    def test_update_patron(self):
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        db_update_mock = Mock()
        self.db_interface.db.update = db_update_mock
        self.db_interface.update_patron(Mock())
        db_update_mock.assert_called()

    def test_update_patron_not_patron(self):
        self.assertIsNone(self.db_interface.update_patron(None))

    def test_close_db(self):
        with patch('tinydb.TinyDB') as mock_db:

            mock_db.close = True
            self.assertIsNone(self.db_interface.close_db())


    def test_convert_patron_to_db_format(self):
        patron_mock = Mock()
        get_fname_mock = Mock()
        get_lname_mock = Mock()
        get_age_mock = Mock()
        get_memberID_mock = Mock()
        get_borrowed_books_mock = Mock()

        patron_mock.get_fname = get_fname_mock
        patron_mock.get_lname = get_lname_mock
        patron_mock.get_age = get_age_mock
        patron_mock.get_memberID = get_memberID_mock
        patron_mock.get_borrowed_books = get_borrowed_books_mock
        self.db_interface.convert_patron_to_db_format(patron_mock)
        get_fname_mock.assert_called()
        get_lname_mock.assert_called()
        get_age_mock.assert_called()
        get_memberID_mock.assert_called()
        get_borrowed_books_mock.assert_called()

    def test_retrieve_patron_none(self):
        id = 1
        query = Mock()
        mock_db = MagicMock()
        mock_db.search.return_value = None
        self.db_interface.db = mock_db
        self.assertEqual(self.db_interface.retrieve_patron(id), None)

    def test_retrieve_patron(self):


        data = {'fname': 'Joe', 'lname': 'Lin', 'age': 12, 'memberID': 1}
        #patron object
        patron = Patron('Joe','Lin',12,1)
        #Mock db.search which return a list of dict
        self.db_interface.db.search  = Mock(return_value = [data])
        self.assertEqual(self.db_interface.retrieve_patron(1), patron)