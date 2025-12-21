from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['genre', 'category']
    search_fields = ['title', 'author__name']

    def create(self, request, *args, **kwargs):
        # Только админ может добавлять книги
        if not request.user.is_staff:
            return Response(
                {"detail": "Только администратор может добавлять книги."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)