from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.core.validators import RegexValidator
from django.utils.text import slugify


class ProfileManager(BaseUserManager):
    '''Detach from default Django username field'''
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
        """Regular user parameters"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('role', 'user')
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """SuperUser parameters"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Role(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class Profile(AbstractUser):
    username = models.CharField(max_length=30,
                                blank=True, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=200, blank=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = ProfileManager()

    def __str__(self) -> str:
        return self.email

    @property
    def is_moder(self) -> bool:
        return self.role == Role.MODERATOR

    @property
    def is_admin(self) -> bool:
        return self.role == Role.ADMIN or self.is_staff or self.is_superuser


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True,
                            verbose_name='Наименование')
    slug = models.SlugField(unique=True, max_length=200,
                            verbose_name='Ссылка')

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Наименование')
    slug = models.SlugField(
        unique=True, max_length=100, blank=True,
        null=True, verbose_name='Ссылка')

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Title(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование')
    year = models.IntegerField(
                default=current_year(),
                validators=[MinValueValidator(1900), max_value_current_year],
                blank=True, null=True,
                verbose_name='Год')
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre, related_name='genre', blank=True, verbose_name='Жанр')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='category',
        verbose_name='Категория')

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'Название'
        verbose_name_plural = 'Названия'


class Review(models.Model):
    text = models.TextField()
    score = models.IntegerField(
        validators=[
            MinValueValidator(1, message='Введите число не меньше 1'),
            MaxValueValidator(10, message='Введите число не больше 10')],
        blank=True, null=True)
    pub_date = models.DateField(auto_now_add=True, db_index=True)

    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE,
        related_name="reviews")
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name="reviews")

    def __str__(self) -> str:
        return f'{self.author} написал {self.text} на {self.title}.'\
               f'{self.author} оценил {self.title} на {self.score}.'\
               f'{self.pub_date}.'

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    text = models.TextField()
    pub_date = models.DateField(
        'Дата публикации', auto_now_add=True, db_index=True)

    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE,
        related_name="comments")
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name="comments")
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name="comments")

    def __str__(self) -> str:
        return f'{self.author} написал {self.text} на {self.review}.'\
               f'{self.pub_date}.'

    class Meta:
        ordering = ["-pub_date"]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментариев'
