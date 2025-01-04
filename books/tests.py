from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from pymongo import MongoClient
import json

class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = '/api/register/'

    def test_register_user_success(self):
        response = self.client.post(self.register_url, {
            "username": "testuser",
            "password": "testpassword"
        }, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.json())

    def test_register_user_existing_username(self):
        User.objects.create_user(username="testuser", password="testpassword")
        response = self.client.post(self.register_url, {
            "username": "testuser",
            "password": "newpassword"
        }, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.json())

class UserLoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = '/api/login/'
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "testpassword"
        }, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.json())

    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "wrongpassword"
        }, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.json())

class BookAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

        # Configurar conexión a MongoDB
        self.mongo_client = MongoClient("mongodb+srv://diegoacostahm:Zr0kp9ETJ0buT01l@book-management.wt80f.mongodb.net/?retryWrites=true&w=majority&appName=book-management")
        self.db = self.mongo_client["book_management_db"]
        self.collection = self.db["books"]

        # Insertar datos de prueba
        self.books = [
            {"title": "Book 1", "author": "Author 1", "published_date": "2023-01-01", "genre": "Fiction", "price": 15.99},
            {"title": "Book 2", "author": "Author 2", "published_date": "2022-01-01", "genre": "Fantasy", "price": 20.99},
        ]
        self.collection.insert_many(self.books)

    def tearDown(self):
        self.collection.delete_many({})
        self.mongo_client.close()

    def test_get_books(self):
        response = self.client.get('/api/books/', **self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 2)  # Paginated response

    def test_create_book(self):
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
        book = self.collection.find_one({"title": "Book 1"})
        book_id = str(book["_id"])
        updated_data = {"title": "Updated Book 1"}

        response = self.client.put(f'/api/books/{book_id}/', json.dumps(updated_data), content_type='application/json', **self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        book = self.collection.find_one({"title": "Book 2"})
        book_id = str(book["_id"])

        response = self.client.delete(f'/api/books/{book_id}/', **self.headers)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
