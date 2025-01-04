from django.db import models

# books/models.py
class Book:
    def __init__(self, title, author, published_date, genre, price):
        self.title = title
        self.author = author
        self.published_date = published_date
        self.genre = genre
        self.price = price

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "published_date": self.published_date,
            "genre": self.genre,
            "price": self.price,
        }

