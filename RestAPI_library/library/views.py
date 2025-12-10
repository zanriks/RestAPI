from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Author, Book
from .serializers import AuthorSerializer, BookListSerializer, BookDetailSerializer
from .permissions import IsAdminOrReadOnly


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'country']
    ordering_fields = ['name', 'created_at']

    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        author = self.get_object()
        books = author.books.all()
        serializer = BookListSerializer(books, many=True)
        return Response(serializer.data)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author__name', 'genre', 'category']
    filterset_fields = ['book_type', 'genre', 'category', 'author']
    ordering_fields = ['title', 'publication_year', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return BookDetailSerializer


    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        book = self.get_object()
        if not book.book_file:
            return Response(
                {'error': 'Файл книги недоступен'},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response({
            'message': f'Файл книги "{book.title}" доступен для скачивания',
            'file_url': request.build_absolute_uri(book.book_file.url)
        })

    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_books = Book.objects.count()
        total_authors = Author.objects.count()
        books_by_type = Book.objects.values('book_type').annotate(count=Count('id'))
        return Response({
            'total_books': total_books,
            'total_authors': total_authors,
            'books_by_type': list(books_by_type)
        })