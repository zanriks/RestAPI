from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        constraints = [
            models.UniqueConstraint(
                fields=['first_name', 'last_name'],
                name='unique_author_name'
            )
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Publisher(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название издательства")

    class Meta:
        verbose_name = "Издательство"
        verbose_name_plural = "Издательства"

    def __str__(self):
        return self.name

class Book(models.Model):
    BOOK_TYPE_CHOICES = [
        ('textbook', 'Учебник'),
        ('fiction', 'Художественная литература'),
    ]

    title = models.CharField(max_length=100, verbose_name = "Название")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name = 'books', verbose_name = "Автор книги")
    year = models.IntegerField(verbose_name = "Год издания", validators = [MinValueValidator(1000), MaxValueValidator(9999)])
    genre = models.CharField(max_length=100, verbose_name = "Жанр")
    category = models.CharField(max_length=100, verbose_name = "Категория")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, verbose_name = "Издательство")
    cover = models.ImageField(upload_to='covers/', null=True, blank=True, verbose_name = "Обложка")
    file = models.FileField(upload_to='books/', null=True, blank=True, verbose_name = "Фай книги")
    book_type = models.CharField(
        max_length=20,
        choices=BOOK_TYPE_CHOICES,
        default='fiction',
        verbose_name="Тип книги"
    )

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author', 'year', 'publisher'],
                name='unique_book_edition'
            )
        ]

    def __str__(self):
        return f"{self.title} ({self.author}, {self.year})"