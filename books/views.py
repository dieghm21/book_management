from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.conf import settings
import pymongo
from bson import ObjectId
from django.contrib.auth.models import User
# from rest_framework_yasg.utils import swagger_auto_schema
# from rest_framework_yasg import openapi

BOOK_COLLECTION = settings.BOOK_COLLECTION

class BookListCreateView(APIView):
    """
    View to list and create books.
    - GET: Retrieves all books with pagination.
    - POST: Allows the creation of a new book.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Retrieve a paginated list of all books.
        - Converts MongoDB's ObjectId to a string.
        - Uses pagination to limit results to 5 books per page.
        """
        books = list(BOOK_COLLECTION.find())
        for book in books:
            book["_id"] = str(book["_id"])  # Convert ObjectId to string for response
        # Set up pagination
        paginator = PageNumberPagination()
        paginator.page_size = 5  # Limit number of results per page
        paginated_books = paginator.paginate_queryset(books, request)
        # Return paginated response
        return paginator.get_paginated_response(paginated_books)

    def post(self, request):
        """
        Create a new book in the database.
        Expects book data in the request body and returns the created book's ID.
        """
        data = request.data
        result = BOOK_COLLECTION.insert_one(data)  # Insert book data into MongoDB
        return Response({"id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)


class BookDetailView(APIView):
    """
    View to retrieve, update, or delete a specific book by ID.
    - GET: Retrieve details of a specific book by its ID.
    - PUT: Update a specific book by its ID.
    - DELETE: Delete a specific book by its ID.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, book_id):
        """
        Retrieve a specific book by its ID.
        If found, return the book's details; otherwise, return a 404 error.
        """
        print(book_id)
        book = BOOK_COLLECTION.find_one({"_id": ObjectId(book_id)})
        if book:
            book["_id"] = str(book["_id"])  # Convert ObjectId to string for response
            return Response(book)
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, book_id):
        """
        Update a specific book by its ID.
        If the book exists, update it with the provided data.
        """
        data = request.data
        result = BOOK_COLLECTION.update_one(
            {"_id": ObjectId(book_id)}, {"$set": data}
        )
        if result.matched_count:
            return Response({"message": "Book updated"})
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, book_id):
        """
        Delete a specific book by its ID.
        If the book is found, delete it; otherwise, return a 404 error.
        """
        try:
            result = BOOK_COLLECTION.delete_one({"_id": ObjectId(book_id)})
            if result.deleted_count == 0:
                return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AveragePriceView(APIView):
    """
    View to calculate the average price of books published in a specific year.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, year):
        """
        Calculate the average price of books published in a specific year.
        - Aggregates the data in MongoDB to compute the average.
        - Expects the year to be passed in the URL.
        """
        pipeline = [
            {"$match": {"published_date": {"$regex": f"^{year}"}}},  # Filter by year
            {"$group": {"_id": None, "average_price": {"$avg": "$price"}}},  # Compute average price
        ]
        result = list(BOOK_COLLECTION.aggregate(pipeline))
        if result:
            return Response({"year": year, "average_price": result[0]["average_price"]})
        return Response({"year": year, "average_price": 0.0})


class RegisterUserView(APIView):
    """
    API view to register a new user.
    Allows users to sign up with a username and password.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Register a new user with a username and password.
        - If the user already exists, returns a 400 error.
        - If successful, creates the user and returns a 201 response with a token.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists."}, status=400)

        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"message": "User successfully created.", "token": token.key}, status=201)


class ObtainAuthTokenView(APIView):
    """
    API view to obtain an authentication token.
    Allows users to authenticate and receive a token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Authenticate a user and return an authentication token.
        - If credentials are valid, returns a 200 response with the token.
        - If invalid, returns a 401 error.
        """
        from django.contrib.auth import authenticate

        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            return Response({"error": "Invalid credentials."}, status=401)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=200)
