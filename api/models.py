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
    # rating
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
    # author ниже
    score = models.IntegerField(
        validators=[MaxValueValidator(1), MinValueValidator(10)])
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


class Categories(models.Model):
    name = models.PositiveSmallIntegerField(
        choices=(
            (1, "Фильм"),
            (2, "Книга"),
            (3, "Музыка"),
        )
    )
    slug = models.PositiveSmallIntegerField(
        choices=(
            (1, "movie"),
            (2, "book"),
            (3, "music"),
        )
    )

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    rating = models.PositiveSmallIntegerField(
        default=None,
        choices=(
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (8, 8),
            (9, 9),
            (10, 10),
        ),
    )
    description = models.TextField(max_length=500, default=None)
    genre = models.ForeignKey(
            Genres,
            models.SET_NULL,
            blank=True,
            null=True,
            related_name="titles"
            )
    category = models.ForeignKey(
            Categories,
            models.SET_NULL,
            blank=True,
            null=True,
            related_name="titles"
            )

    def __str__(self):
        return self.name
