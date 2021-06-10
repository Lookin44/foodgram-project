from django.db import models

from users.models import User


class Tag(models.Model):
    value = models.CharField('Значение', max_length=50, null=True)
    style = models.CharField('Стиль для шаблона', max_length=50, null=True)
    name = models.CharField('Имя для шаблона', max_length=50, null=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    title = models.CharField(max_length=200)
    dimension = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='recipes')
    ingredients = models.ManyToManyField(
        Ingredient, through='Amount', through_fields=('recipe', 'ingredient')
    )
    cooking_time = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class Amount(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_amount'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='ingredients'
    )
    quantity = models.FloatField()

    def __str__(self):
        return self.ingredient.title


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite_recipes',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    def __str__(self):
        return self.recipe.title


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    def __str__(self):
        return self.user.username

    def follower(self):
        return self.user.username

    def following(self):
        return self.author.username


class ShopList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shop_list"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shop_list'
    )

    def __str__(self):
        return self.recipe.title
