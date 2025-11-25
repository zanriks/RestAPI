from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'books_count', 'created_at']
    search_fields = ['name', 'country']
    list_filter = ['country', 'created_at']

    def books_count(self, obj):
        return obj.books.count()

    books_count.short_description = 'Количество книг'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publication_year', 'book_type', 'publisher']
    list_filter = ['book_type', 'genre', 'category', 'publication_year']
    search_fields = ['title', 'author__name', 'publisher']
    readonly_fields = ['created_at', 'updated_at']