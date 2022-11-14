from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Scope(models.Model):

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    articles = models.ManyToManyField(Article, through='ArticleScopes', verbose_name='Выбор статьи')
    name = models.CharField(max_length=200, verbose_name='Имя тега')

    def __str__(self):
        return self.name


class ArticleScopes(models.Model):

    class Meta:
        verbose_name = 'Тематика статьи'
        verbose_name_plural = ' Тематики статьи'
        ordering = ['-is_main', 'tag']

    article = models.ForeignKey(Article, related_name='scopes', on_delete=models.CASCADE)
    tag = models.ForeignKey(Scope, related_name='scopes', on_delete=models.CASCADE, verbose_name='РАЗДЕЛ')
    is_main = models.BooleanField(verbose_name='ОСНОВНОЙ', )

