from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from pymongo import MongoClient
import json

class UserRegistrationTests(TestCase):
    """
    Test suite for the user registration API endpoint.
    """
    def setUp(self):
        # Initialize the test client and define the registration endpoint URL
        self.client = Client()
        self.register_url = '/api/register/'

    def test_register_user_success(self):
        """
        Test registering a new user with valid data.
        Expects a 201 CREATED response and a token in the response.
        """
        response = self.client.post(self.register_url, {
            "username": "testuser",
            "password": "testpassword"
        }, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.json())

    def test_register_user_existing_username(self):
        """
        Test registering a user with an already existing username.
        Expects a 400 BAD REQUEST response with an error message.
        """
        User.objects.create_user(username="testuser", password="testpassword")
        response = self.client.post(self.register_url, {
            "username": "testuser",
            "password": "newpassword"
        }, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.json())

class UserLoginTests(TestCase):
    """
    Test suite for the user login API endpoint.
    """
    def setUp(self):
        # Initialize the test client and define the login endpoint URL
        self.client = Client()
        self.login_url = '/api/login/'
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_login_success(self):
        """
        Test logging in with valid credentials.
        Expects a 200 OK response and a token in the response.
        """
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "testpassword"
        }, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.json())

    def test_login_invalid_credentials(self):
        """
        Test logging in with invalid credentials.
        Expects a 401 UNAUTHORIZED response with an error message.
        """
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "wrongpassword"
        }, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.json())

class BookAPITests(TestCase):
    """
    Test suite for the book management API.
    """
    def setUp(self):
        """
        Set up the test environment:
        - Create a test user and generate an auth token.
        - Connect to the MongoDB database and insert sample book data.
        """
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        # Configure MongoDB connection
        self.mongo_client = MongoClient("mongodb+srv://diegoacostahm:Zr0kp9ETJ0buT01l@book-management.wt80f.mongodb.net/?retryWrites=true&w=majority&appName=book-management")
        self.db = self.mongo_client["book_management_db"]
        self.collection = self.db["books"]

        # Insert sample books into the MongoDB collection
        self.books = [
            {"title": "Book 1", "author": "Author 1", "published_date": "2023-01-01", "genre": "Fiction", "price": 15.99},
            {"title": "Book 2", "author": "Author 2", "published_date": "2022-01-01", "genre": "Fantasy", "price": 20.99},
        ]
        self.collection.insert_many(self.books)

    def tearDown(self):
        """
        Clean up after each test:
        - Delete all book records from MongoDB.
        - Close the MongoDB connection.
        """
        self.collection.delete_many({})
        self.mongo_client.close()

    def test_get_books(self):
        """
        Test retrieving the list of books.
        Expects a 200 OK response with a paginated list of books.
        """
        response = self.client.get('/api/books/', **self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 2)  # Paginated response

    def test_create_book(self):
        """
        Test creating a new book with valid data.
        Expects a 201 CREATED response.
        """
        book_data = {
            "title": "Book 3",
            "author": "Author 3",
            "published_date": "2021-01-01",
            "genre": "Sci-Fi",
            "price": 18.99
        }
        response = self.client.post('/api/books/', json.dumps(book_data), content_type='application/json', **self.headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_book(self):
        """
        Test updating an existing book's data.
        Expects a 200 OK response.
        """
        book = self.collection.find_one({"title": "Book 1"})
        book_id = str(book["_id"])
        updated_data = {"title": "Updated Book 1"}

        response = self.client.put(f'/api/books/{book_id}/', json.dumps(updated_data), content_type='application/json', **self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        """
        Test deleting an existing book.
        Expects a 204 NO CONTENT response.
        """
        book = self.collection.find_one({"title": "Book 2"})
        book_id = str(book["_id"])

        response = self.client.delete(f'/api/books/{book_id}/', **self.headers)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
