from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(default=name, unique=True, max_length=200)

    class Meta:
        ordering = ["-id"]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(default=name, unique=True, max_length=100, blank=True, null=True)

    class Meta:
        ordering = ["-id"]
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(blank=True, null=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=True, null=True,
    )
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(
        Genre, related_name="genre",
        blank=True, null=True)
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
    # author ниже
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateField(auto_now_add=True)

    # связь с моделями для удаления
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="reviews")
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name="reviews")

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.author, self.text


class Comment(models.Model):
    text = models.TextField()
    # author ниже
    pub_date = models.DateField('Дата публикации', auto_now_add=True)

    # связь с моделями для удаления
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="comments")
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name="comments")
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name="comments")

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментариев'

    def __str__(self):
        return self.text
