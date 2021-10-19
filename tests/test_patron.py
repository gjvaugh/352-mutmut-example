import unittest
from library.patron import Patron
from library.patron import InvalidNameException

class TestPatron(unittest.TestCase):

    def setUp(self):
        self.test_patron = Patron("Bob", "Jenkins", 29, "abc123")
        self.book = "Autobiography of Bob Jenkins"

    def test_invalid_fname(self):
        self.assertRaises(InvalidNameException, Patron, "123", "Miller", 29, "asdf")

    def test_invalid_lname(self):
        self.assertRaises(InvalidNameException, Patron, "Frank", "456", 29, "asdf")

    def test_add_book_not_borrowed(self):
        self.test_patron.add_borrowed_book(self.book)
        self.assertEqual(len(self.test_patron.get_borrowed_books()), 1)

    def test_add_book_already_borrowed(self):
        self.test_patron.add_borrowed_book(self.book)
        self.test_patron.add_borrowed_book(self.book)
        self.assertEqual(len(self.test_patron.get_borrowed_books()), 1)

    def test_get_borrowed_books(self):
        self.test_patron.add_borrowed_book(self.book)
        self.assertEqual(self.test_patron.get_borrowed_books()[0], self.book.lower())

    def test_return_borrowed_book_in_library(self):
        self.test_patron.add_borrowed_book(self.book)
        self.test_patron.return_borrowed_book(self.book)
        self.assertEqual(len(self.test_patron.get_borrowed_books()), 0)

    def test_return_borrowed_book_not_in_library(self):
        self.test_patron.add_borrowed_book(self.book)
        self.test_patron.return_borrowed_book("Programming for Dummies")
        self.assertEqual(len(self.test_patron.get_borrowed_books()), 1)

    def test_eq_equal(self):
        self.assertTrue(self.test_patron.__eq__(self.test_patron))

    def test_eq_not_equal(self):
        other_patron = Patron("Billy", "Smith", 30, "xyz789")
        self.assertFalse(self.test_patron.__eq__(other_patron))

    def test_ne_equal(self):
        self.assertFalse(self.test_patron.__ne__(self.test_patron))

    def test_ne_not_equal(self):
        other_patron = Patron("Billy", "Smith", 30, "xyz789")
        self.assertTrue(self.test_patron.__ne__(other_patron))

    def test_get_fname(self):
        self.assertEqual(self.test_patron.get_fname(), "Bob")

    def test_get_lname(self):
        self.assertEqual(self.test_patron.get_lname(), "Jenkins")

    def test_get_age(self):
        self.assertEqual(self.test_patron.get_age(), 29)

    def test_get_memberID(self):
        self.assertEqual(self.test_patron.get_memberID(), "abc123")


