from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)

    class Meta:
        ordering = ["-id"]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ["-id"]
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.DateField()
    description = models.TextField()
    genre = models.ManyToManyField(
        Genre, related_name="genre")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name="category")

    class Meta:
        ordering = ["-id"]
        verbose_name = 'Название'
        verbose_name_plural = 'Названия'

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateField(auto_now_add=True)
    score = models.IntegerField(
        validators=[MaxValueValidator(1), MinValueValidator(10)])
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="user")
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name="title")
    review = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='review')

    class Meta:
        ordering = ["-id"]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.author, self.text


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="author"
        )

    class Meta:
        ordering = ["-id"]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментирии'

    def __str__(self):
        return self.text
