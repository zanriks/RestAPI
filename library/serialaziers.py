from rest_framework import serializers
from .models import Book, Author

class BookSerializer(serializers.ModelSerializer):
    model = Book
    fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    model = Author
    fields = '__all__'