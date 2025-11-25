from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    biography = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='authors/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Book(models.Model):
    BOOK_TYPES = [
        ('fiction', 'Художественная литература'),
        ('textbook', 'Учебник'),
        ('scientific', 'Научная литература'),
        ('other', 'Другое'),
    ]

    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publication_year = models.IntegerField(
        validators=[MinValueValidator(1000), MaxValueValidator(9999)]
    )
    genre = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    book_type = models.CharField(max_length=20, choices=BOOK_TYPES, default='fiction')
    edition = models.IntegerField(default=1)  # Для учебников — номер издания
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    book_file = models.FileField(upload_to='books/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    pages = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['title', 'author', 'publication_year', 'publisher']
        ordering = ['title']

    def __str__(self):
        return f"{self.title} - {self.author.name} ({self.publication_year})"