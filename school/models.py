from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField('назва', max_length=32, unique=True)
    salary = models.DecimalField('ставка', max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['-salary']


class Style(models.Model):
    name = models.CharField('стиль', max_length=64)
    description = models.TextField('опис', blank=True, null=True)
    photo = models.ImageField(upload_to='styles/', blank=True, null=True)
    slug = models.SlugField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Стиль'
        verbose_name_plural = 'Стилі'
        ordering = ['name']


class Teacher(models.Model):
    first_name = models.CharField('ім’я', max_length=64)
    last_name = models.CharField('прізвище', max_length=64)
    middle_name = models.CharField('по-батькові', max_length=64, blank=True, null=True)
    nickname = models.CharField('псевдонім', max_length=64, blank=True)
    photo = models.ImageField(upload_to='teachers/', blank=True, verbose_name='фото')
    slug = models.SlugField(max_length=50, blank=True, verbose_name='слаг')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='категорія')
    styles = models.ManyToManyField(
        Style,
        verbose_name='стилі',
        related_name='teachers',
        related_query_name='teacher'
    )

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = f'{self.first_name} {self.last_name}'
        if not self.slug:
            self.slug = slugify(f'{self.first_name} {self.last_name}')
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('teacher_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'Педагог'
        verbose_name_plural = 'Педагоги'
        ordering = ['nickname']
