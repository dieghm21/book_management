from django.urls import path
from .views import BookListCreateView, BookDetailView, AveragePriceView, RegisterUserView, ObtainAuthTokenView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', ObtainAuthTokenView.as_view(), name='login'),
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<str:book_id>/', BookDetailView.as_view(), name='book-detail'),
    path('books/average-price/<int:year>/', AveragePriceView.as_view(), name='average-price'),

]
