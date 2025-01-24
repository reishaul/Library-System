import unittest
from unittest.mock import patch, MagicMock
from LibrarySystem import LibrarySystem


class TestLibrarySystem(unittest.TestCase):

    def setUp(self):
        self.library = LibrarySystem()

    @patch('CSV.read_csv')
    @patch('CSV.write_csv')
    def test_register_user_success(self, mock_write_csv, mock_read_csv):
        self.library.users = []
        mock_read_csv.return_value = []
        self.library.register_user("testuser", "testpassword")
        self.assertEqual(len(self.library.users), 1)
        self.assertEqual(self.library.users[0]['username'], "testuser")
        mock_write_csv.assert_called()

    @patch('CSV.read_csv')
    def test_register_user_fail_user_exists(self, mock_read_csv):
        mock_read_csv.return_value = [{'username': 'testuser', 'password': 'hashedpassword'}]
        with self.assertRaises(ValueError):
            self.library.register_user("testuser", "testpassword")

    @patch('CSV.read_csv')
    def test_authenticate_user_success(self, mock_read_csv):
        mock_read_csv.return_value = [{'username': 'testuser', 'password': self.library.hash_password("testpassword")}]
        result = self.library.authenticate_user("testuser", "testpassword")
        self.assertTrue(result)

    @patch('CSV.read_csv')
    def test_authenticate_user_fail(self, mock_read_csv):
        self.library.users = []
        mock_read_csv.return_value = [{'username': 'testuser', 'password': self.library.hash_password("wrongpassword")}]
        result = self.library.authenticate_user("testuser", "testpassword")
        self.assertFalse(result)

    @patch('CSV.write_csv')
    def test_add_book_success(self, mock_write_csv):
        self.library.books = []
        win_mock = MagicMock()
        self.library.add_book("Test Book", "Test Author", "2023", "Fiction", "5", win_mock)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0]['title'], "Test Book")
        mock_write_csv.assert_called()

    @patch('CSV.read_csv')
    @patch('CSV.write_csv')
    def test_remove_book_success(self, mock_write_csv, mock_read_csv):
        mock_read_csv.return_value = [{'title': 'Test Book', 'author': 'Test Author', 'copies': '5'}]
        self.library.books = mock_read_csv.return_value
        self.library.remove_book("Test Book")
        self.assertEqual(len(self.library.books), 0)
        mock_write_csv.assert_called()

    @patch('CSV.read_csv')
    def test_remove_book_not_found(self, mock_read_csv):
        mock_read_csv.return_value = [{'title': 'Other Book', 'author': 'Other Author', 'copies': '5'}]
        self.library.books = mock_read_csv.return_value
        with patch('Obserever.notify') as mock_notify:
            self.library.remove_book("Test Book")
            mock_notify.assert_called_with("Error", "Book not found.")



    @patch('CSV.read_csv')
    def test_handle_searched_books_by_year_invalid_input(self, mock_read_csv):

        self.library.books = []
        mock_read_csv.return_value = [{'title': 'Test Book', 'author': 'Test Author', 'year': '2023', 'genre': 'Fiction'}]
        self.library.books = mock_read_csv.return_value


        with patch('Obserever.notify') as mock_notify:
            result = self.library.handle_searched_books(2, "invalid_year", MagicMock())
            mock_notify.assert_called_with("Error", "Invalid year format for book ")
            self.assertEqual(len(result), 0)

    @patch('CSV.read_csv')
    @patch('CSV.write_csv')
    def test_loan_book_success(self, mock_write_csv, mock_read_csv):
        mock_read_csv.return_value = [{'title': 'Test Book', 'author': 'Test Author', 'available_copies': '5', 'copies': '5', 'popularity': '0'}]
        self.library.books = mock_read_csv.return_value
        result = self.library.loan_book("Test Book")
        self.assertEqual(result, "success")
        self.assertEqual(self.library.books[0]['available_copies'], '4')
        mock_write_csv.assert_called()

    @patch('CSV.read_csv')
    def test_loan_book_no_copies(self, mock_read_csv):
        mock_read_csv.return_value = [{'title': 'Test Book', 'author': 'Test Author', 'available_copies': '0', 'copies': '5', 'popularity': '0'}]
        self.library.books = mock_read_csv.return_value
        result = self.library.loan_book("Test Book")
        self.assertEqual(result, "no_copies")

if __name__ == "__main__":
    unittest.main()
