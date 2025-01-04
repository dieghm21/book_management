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


BOOK_COLLECTION = settings.BOOK_COLLECTION

class BookListCreateView(APIView):
    """Crear y listar libros."""
    permission_classes = [IsAuthenticated]
    def get(self, request):
       # Obtener todos los libros de la base de datos
       books = list(BOOK_COLLECTION.find())
       for book in books:
           book["_id"] = str(book["_id"])  # Convertir ObjectId a string
       # Configurar la paginación
       paginator = PageNumberPagination()
       paginator.page_size = 5  
       paginated_books = paginator.paginate_queryset(books, request)
       # Responder con los datos paginados
       return paginator.get_paginated_response(paginated_books)

    def post(self, request):
        data = request.data
        result = BOOK_COLLECTION.insert_one(data)
        return Response({"id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)


class BookDetailView(APIView):
    """Obtener, actualizar o eliminar un libro específico."""
    permission_classes = [IsAuthenticated]
    def get(self, request, book_id):
        print(book_id)
        book = BOOK_COLLECTION.find_one({"_id": ObjectId(book_id)})
        if book:
            book["_id"] = str(book["_id"])
            return Response(book)
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, book_id):
        data = request.data
        result = BOOK_COLLECTION.update_one(
            {"_id": ObjectId(book_id)}, {"$set": data}
        )
        if result.matched_count:
            return Response({"message": "Book updated"})
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, book_id):
        try:
            result = BOOK_COLLECTION.delete_one({"_id": ObjectId(book_id)})
            if result.deleted_count == 0:
                return Response({"error": "Libro no encontrado."}, status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AveragePriceView(APIView):
    """Calcular el precio promedio de los libros por año."""
    permission_classes = [IsAuthenticated]
    def get(self, request, year):
        pipeline = [
            {"$match": {"published_date": {"$regex": f"^{year}"}}},
            {"$group": {"_id": None, "average_price": {"$avg": "$price"}}},
        ]
        result = list(BOOK_COLLECTION.aggregate(pipeline))
        if result:
            return Response({"year": year, "average_price": result[0]["average_price"]})
        return Response({"year": year, "average_price": 0.0})
    
class RegisterUserView(APIView):
    """
    API para registrar un nuevo usuario.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "El nombre de usuario y la contraseña son obligatorios."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "El usuario ya existe."}, status=400)

        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"message": "Usuario creado exitosamente.", "token": token.key}, status=201)


class ObtainAuthTokenView(APIView):
    """
    API para obtener el token de autenticación.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        from django.contrib.auth import authenticate

        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            return Response({"error": "Credenciales inválidas."}, status=401)

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=200)
