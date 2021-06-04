from django.db import models

from users.models import User


class Tag(models.Model):
    value = models.CharField('Значение', max_length=50, null=True)
    style = models.CharField('Стиль для шаблона', max_length=50, null=True)
    title = models.CharField('Имя для шаблона', max_length=50, null=True)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField('Название ингредиента', max_length=50)
    unit = models.CharField('Мера', max_length=50, default='шт.',)
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
    tag = models.ManyToManyField(Tag, related_name='recipes')
    cooking_time = models.PositiveSmallIntegerField()
    description = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('-pub_date', )

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
