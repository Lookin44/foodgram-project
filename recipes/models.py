from django.db import models

from users.models import User


class Tag(models.Model):
    value = models.CharField(verbose_name='Значение',
                             max_length=50, null=True)
    style = models.CharField(verbose_name='Стиль для шаблона',
                             max_length=50, null=True)
    name = models.CharField(verbose_name='Имя в шаблона',
                            max_length=50, null=True)

    def __str__(self):
        return self.value


class Ingredient(models.Model):
    title = models.CharField(verbose_name='Имя ингредиента',
                             max_length=200)
    dimension = models.CharField(verbose_name='Единица измерения',
                                 max_length=50)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['title', 'dimension'],
            name='unique_recipe_ingredient')]

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='recipes')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True,
                                    db_index=True)
    title = models.CharField(verbose_name='Название рецепта',
                             max_length=200)
    image = models.ImageField(verbose_name='Фото рецепта',
                              upload_to='recipes/',
                              null=True)
    description = models.TextField(verbose_name='Описание рецепта')
    tags = models.ManyToManyField(Tag,
                                  verbose_name='Тэги рецепта',
                                  related_name='recipes')
    ingredients = models.ManyToManyField(Ingredient,
                                         verbose_name='Ингредиенты рецепта',
                                         through='Amount',
                                         through_fields=('recipe',
                                                         'ingredient')
                                         )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        null=True
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class Amount(models.Model):
    recipe = models.ForeignKey(Recipe,
                               verbose_name='Рецепта',
                               on_delete=models.CASCADE,
                               related_name='recipe_amount')
    ingredient = models.ForeignKey(Ingredient,
                                   verbose_name='Ингредиенты рецепта',
                                   on_delete=models.CASCADE,
                                   related_name='ingredients')
    quantity = models.IntegerField(verbose_name='Количество ингредиента')

    def __str__(self):
        return self.ingredient.title


class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe,
                               verbose_name='Избранный рецепт',
                               on_delete=models.CASCADE,
                               related_name='favorite_recipes')
    user = models.ForeignKey(User,
                             verbose_name='Юзер добавивший рецепт в избранное',
                             on_delete=models.CASCADE,
                             related_name='favorites')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['recipe', 'user'],
                                               name='UniqueFavorite')]

    def __str__(self):
        return self.recipe.title


class Subscription(models.Model):
    user = models.ForeignKey(User,
                             verbose_name='Подписчик',
                             on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User,
                               verbose_name='Автор рецептов',
                               on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'author'],
                                               name='UniqueSubscription')]

    def __str__(self):
        return f'{self.user} подписан на {self.author}'


class ShopList(models.Model):
    user = models.ForeignKey(User,
                             verbose_name='Чья корзина',
                             on_delete=models.CASCADE,
                             related_name='shop_list')
    recipe = models.ForeignKey(Recipe,
                               verbose_name='Рецепты в корзине',
                               on_delete=models.CASCADE,
                               related_name='shop_list')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'recipe'],
                                               name='UniqueShopList')]

    def __str__(self):
        return self.recipe.title
