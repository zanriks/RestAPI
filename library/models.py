from django.db import models

# Create your models here.

class Book(models.Model):
    BOOK_TYPE_CHOICES = [
        ('textbook', 'Учебник'),
        ('fiction', 'Художественная литература'),
    ]

    title = models.CharField(max_length=100, verbose_name = "Название")
    author = models.CharField(max_length=100, verbose_name = "Автор книги")
    year = models.IntegerField(verbose_name = "Год издания")
    genre = models.CharField(max_length=100, verbose_name = "Жанр")
    category = models.CharField(max_length=100, verbose_name = "Категория")
    publisher = models.CharField(max_length=100, verbose_name = "Издательство")
    cover = models.ImageField(upload_to='covers/', null=True, blank=True, verbose_name = "Обложка")
    file = models.FileField(upload_to='books/', null=True, blank=True, verbose_name = "Фай книги")
    book_type = models.CharField(
        max_length=20,
        choices=BOOK_TYPE_CHOICES,
        default='fiction',
        verbose_name="Тип книги"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author', 'year', 'publisher'],
                name='unique_book_edition'
            )
        ]

    def __str__(self):
        return f"{self.title} ({self.author}, {self.year})"


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField()
    date_of_birth = models.DateField()
    date_of_death = models.DateField()

    def __str__(self):
        return f"{self.first_name} ({self.last_name})"