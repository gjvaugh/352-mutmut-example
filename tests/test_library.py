import unittest
from unittest.mock import Mock
from library import library
from library.patron import Patron
import json

class TestLibrary(unittest.TestCase):

    def setUp(self):
        library.Library_DB = Mock()
        library.Books_API  = Mock()
        patron = Mock()
        self.lib = library.Library()

        self.patron = patron
        self.test_data={}
        self.read ={}
        self.patronId = 1
        self.patronFname = "Joe"
        self.patronLname = "Lin"
        self.patronAage = 20

        # self.books_data = [{'title': 'Learning Python', 'ebook_count': 3}, {'title': 'Learning Python (Learning)', 'ebook_count': 1}, {'title': 'Learning Python', 'ebook_count': 1}, {'title': 'Learn to Program Using Python', 'ebook_count': 1}, {'title': 'Aprendendo Python', 'ebook_count': 1}, {'title': 'Python Basics', 'ebook_count': 1}]
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())

        with open('tests_data/json_data.txt','r') as f:
            self.test_data = json.loads(f.read())['docs'][0]


    def test_is_ebook_true(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertTrue(self.lib.is_ebook('learning python'))
    def test_is_ebook_false(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertFalse(self.lib.is_ebook('lnearning pytho'))

    def test_get_ebooks_count(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertEqual(self.lib.get_ebooks_count("learning python"), 8)


    def test_is_book_by_author_true(self):

        book_name =  self.test_data['title']
        book_author= self.test_data['author_name']
        self.lib.api.books_by_author= Mock(return_value = [book_name])

        self.assertTrue(self.lib.is_book_by_author(book_author,book_name))

    def test_is_book_by_author_false(self):
        book_name = self.test_data['title']
        book_author= "stranger"
        self.lib.api.books_by_author= Mock(return_value = [])
        self.assertFalse(self.lib.is_book_by_author(book_author,book_name))

    def test_get_languages_for_book_true(self):
        book_name = self.test_data['title']
        sol = set()
        sol.update(('eng',))
        self.lib.api.get_book_info = Mock(return_value=[self.test_data])
        self.assertEqual(self.lib.get_languages_for_book(book_name),sol)

    def test_get_languages_for_book_false(self):
        book_name = self.test_data['title']
        sol = set()
        self.lib.api.get_book_info = Mock(return_value=[])
        self.assertEqual(self.lib.get_languages_for_book(book_name),sol)

    def test_register_patron_valid(self):

        self.lib.db.insert_patron = Mock(return_value = self.patronId)
        self.assertEqual(self.lib.register_patron(self.patronFname,self.patronLname,self.patronAage,self.patronId),self.patronId)

    def test_register_patron_invalid(self):
        self.lib.db.insert_patron = Mock(return_value = None)
        self.assertIsNone(self.lib.register_patron(self.patronFname,self.patronLname,self.patronAage,self.patronId),self.patronId)


    def test_is_patron_registered_true(self):
        self.lib.db.retrieve_patron = Mock(return_value=self.patron)
        self.patron.get_memberID = Mock(return_value = self.patronId)
        self.assertTrue(self.lib.is_patron_registered(self.patron))

    def test_is_patron_registered_false(self):
        self.lib.db.retrieve_patron = Mock(return_value = None)
        self.patron.get_memberID = Mock(return_value = self.patronId)
        self.assertFalse(self.lib.is_patron_registered(self.patron))

    def test_borrow_book(self):
        # book_title = self.test_data['title']
        book_title = self.test_data['title']
        add_borrowed_book = Mock()
        update_patron = Mock()

        self.patron.add_borrowed_book = add_borrowed_book
        self.lib.db.update_patron = update_patron

        self.patron.add_borrowed_book(Mock())
        self.lib.db.update_patron(Mock())

        add_borrowed_book.assert_called()
        update_patron.assert_called()

        self.patron.add_borrowed_book = Mock(return_value = None)
        self.lib.db.update_patron = Mock(return_value = None)
        self.assertIsNone(self.lib.borrow_book(book_title,self.patron))


    def test_return_borrowed_book(self):
        book_title = self.test_data['title']
        return_borrowed_book  = Mock()
        update_patron = Mock()


        self.patron.return_borrowed_book = return_borrowed_book
        self.lib.db.update_patron = update_patron

        return_borrowed_book(Mock())
        update_patron(Mock())

        self.patron.return_borrowed_book.assert_called()
        self.lib.db.update_patron.assert_called()

        self.patron.return_borrowed_book = Mock(return_value = None)
        self.assertIsNone(self.lib.return_borrowed_book(book_title,self.patron))

    def test_is_book_borrowed_true(self):

        book_title = self.test_data['title'].lower()
        self.patron.get_borrowed_books = Mock(return_value=[book_title])
        self.assertTrue(self.lib.is_book_borrowed(book_title, self.patron))



    def test_is_book_borrowed_false(self):
        book_title = self.test_data['title'].lower()
        self.patron.get_borrowed_books = Mock(return_value = [])
        self.assertFalse(self.lib.is_book_borrowed(book_title, self.patron))