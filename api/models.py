from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, )
    slug = models.SlugField(default=None, unique=True, max_length=200)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-id"]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(
        unique=True, max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-id"]
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(
        Genre, related_name="genre",
        blank=True)
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
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=True, null=True)
    pub_date = models.DateField(auto_now_add=True)

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
        return str(self.score)


class Comment(models.Model):
    text = models.TextField()
    pub_date = models.DateField('Дата публикации', auto_now_add=True)

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


GROUPS = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class ProfileManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('role', 'user')
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Profile(AbstractUser):
    username = models.CharField(max_length=30, blank=True, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=200, blank=True)
    role = models.CharField(max_length=20,
                            default='user',
                            choices=GROUPS)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ProfileManager()


class Confirm(models.Model):
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(max_length=10)
