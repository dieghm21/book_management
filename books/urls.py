from django.urls import path
from rest_framework import permissions
from .views import BookListCreateView, BookDetailView, AveragePriceView, RegisterUserView, ObtainAuthTokenView
# from rest_framework_yasg import openapi
# from rest_framework_yasg.views import get_schema_view

# Swagger schema view
# schema_view = get_schema_view(
#    openapi.Info(
#       title="Book Management API",
#       default_version='v1',
#       description="API documentation for the Book Management system.",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email=""),
#       license=openapi.License(name=""),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', ObtainAuthTokenView.as_view(), name='login'),
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<str:book_id>/', BookDetailView.as_view(), name='book-detail'),
    path('books/average-price/<int:year>/', AveragePriceView.as_view(), name='average-price'),
    # path('swagger/', schema_view.as_view(), name='swagger-docs')

]
