# serializers.py
from rest_framework import serializers
from .models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = [
            'id', 'name', 'biography', 'birth_date', 'death_date',
            'country', 'photo', 'books_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_books_count(self, obj):
        return obj.books.count()


class BookListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author_name', 'publication_year', 'genre',
            'category', 'book_type', 'cover_image', 'created_at'
        ]


class BookDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        source='author',
        write_only=True
    )

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'author_id', 'publication_year', 'genre',
            'category', 'publisher', 'book_type', 'edition', 'cover_image',
            'book_file', 'description', 'isbn', 'pages', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        title = data.get('title')
        author = data.get('author')
        publication_year = data.get('publication_year')
        publisher = data.get('publisher')

        # Проверка уникальности комбинации
        queryset = Book.objects.filter(
            title=title,
            author=author,
            publication_year=publication_year,
            publisher=publisher
        )
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "Книга с такой комбинацией названия, автора, года выпуска и издательства уже существует."
            )

        # Валидация номера издания для учебников
        if data.get('book_type') == 'textbook':
            edition = data.get('edition', 1)
            if edition <= 0:
                raise serializers.ValidationError(
                    "Номер издания для учебника должен быть положительным числом."
                )

        return data