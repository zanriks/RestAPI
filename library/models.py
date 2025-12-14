from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.IntegerField()
    genre = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    publisher = models.BooleanField()
    cover = models.ImageField(upload_to='cover', null=True, blank=True)
    file = models.FileField(upload_to='file', null=True, blank=True)

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