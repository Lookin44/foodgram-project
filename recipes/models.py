from django.db import models

from users.models import User


class Tag(models.Model):
    TAG_OPTIONS = {
        'breakfast': ['orange', 'Завтрак'],
        'lunch': ['green', 'Обед'],
        'dinner': ['purple', 'Ужин'],
    }

    TAG_CHOICES = [
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('dinner', 'Ужин'),
    ]
    title = models.CharField(
        unique=True,
        max_length=20,
        choices=TAG_CHOICES,
        verbose_name='tag name'
    )

    def __str__(self):
        return self.title

    @property
    def color(self):
        return self.TAG_OPTIONS[self.title][0]

    @property
    def name(self):
        return self.TAG_OPTIONS[self.title][1]


class Ingredient(models.Model):
    title = models.CharField(max_length=50)
    unit = models.CharField(max_length=50, default='шт.',)
    count = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes')
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='recipes/')
    ingredients = models.ManyToManyField(Ingredient)
    tag = models.ManyToManyField(Tag)
    cooking_time = models.PositiveSmallIntegerField()
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Follow(models.Model):

    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'author'],
                                               name='unique_follows')]

    def __str__(self):
        return f'{self.user.name}, {self.author.name}'


class Favorites(models.Model):

    user = models.ForeignKey(
        User,
        related_name='menu',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='user_menu',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='unique_menu')]
