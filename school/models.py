from django.db import models


class Category(models.Model):
    name = models.CharField('назва', max_length=32, unique=True)
    salary = models.DecimalField('ставка', max_digits=5, decimal_places=2)

    def __str__(self):
        return f'<Category: {self.name}>'

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['salary']


class Style(models.Model):
    name = models.CharField('стиль', max_length=64)
    description = models.TextField('опис', blank=True, null=True)
    photo = models.ImageField(upload_to='styles/', blank=True, null=True)
    slug = models.SlugField(max_length=32)

    def __str__(self):
        return f'<Style: {self.name}>'

    class Meta:
        verbose_name = 'Стиль'
        verbose_name_plural = 'Стилі'
        ordering = ['name']


class Teacher(models.Model):
    first_name = models.CharField('ім’я', max_length=64)
    last_name = models.CharField('прізвище', max_length=64)
    middle_name = models.CharField('по-батькові', max_length=64)
    nickname = models.CharField('псевдонім', max_length=64, blank=True, default=f'{first_name} {last_name}')
    photo = models.ImageField(upload_to='teachers/', blank=True)
    slug = models.SlugField(max_length=50)
    # It is often useful to automatically prepopulate a SlugField based on the value of some other value. You can
    # do this automatically in the admin using prepopulated_fields.
    category = models.ForeignKey(Category, on_delete=models.SET_NULL)
    styles = models.ManyToManyField(
        Style,
        verbose_name='стилі',
        related_name='teachers',
        related_query_name='teacher'
    )

    def __str__(self):
        return f'<Teacher: {self.nickname}>'

    class Meta:
        verbose_name = 'Педагог'
        verbose_name_plural = 'Педагоги'
        ordering = ['nickname']
