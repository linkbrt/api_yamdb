from django.db import models

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
    rating = models.PositiveSmallIntegerField(default=None,
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