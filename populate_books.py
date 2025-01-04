import os
import django

# Configurar Django para ejecutar este script
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_management.settings')
django.setup()

from django.conf import settings

BOOK_COLLECTION = settings.BOOK_COLLECTION

data = [
    {"title": "Book 1", "author": "Author 1", "published_date": "2023-01-01", "genre": "Fiction", "price": 15.99},
    {"title": "Book 2", "author": "Author 2", "published_date": "2022-06-15", "genre": "Non-Fiction", "price": 20.99},
    {"title": "Book 3", "author": "Author 3", "published_date": "2023-09-10", "genre": "Fiction", "price": 10.49},
    {"title": "Book 4", "author": "Author 4", "published_date": "2021-03-05", "genre": "Science", "price": 25.00},
    {"title": "Book 5", "author": "Author 5", "published_date": "2020-11-11", "genre": "History", "price": 18.75},
]

BOOK_COLLECTION.insert_many(data)
print("Books inserted successfully!")
