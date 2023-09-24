from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    """
    Класс для ведения блога
    """
    blog_title = models.CharField(max_length=150, verbose_name='Заголовок')
    blog_text = models.TextField(verbose_name='Содержимое')
    blog_preview = models.ImageField(upload_to='catalog/', verbose_name='Превью', **NULLABLE)
    blog_slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)
    blog_date_creation = models.DateField(auto_now=False, auto_now_add=True, verbose_name='Дата публикации')
    blog_is_active = models.BooleanField(default=True, verbose_name='Опубликовано')
    blog_views_count = models.IntegerField(default=0, verbose_name='Просмотры')

    blog_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   verbose_name='владелец', **NULLABLE)

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.blog_title}'

    class Meta:
        verbose_name = 'Статья'  # Настройка для наименования одного объекта
        verbose_name_plural = 'Статьи'  # Настройка для наименования набора объектов
        ordering = ('blog_title',)  # сортировка по наименованию
