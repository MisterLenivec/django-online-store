import os
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True,
                            verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True)  # db_index=True
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('lenivastore:product_list_by_category', args=[self.slug])


def get_upload_path(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return os.path.join('images/', filename)


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='products',
        verbose_name="Категория",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.TextField(blank=True, verbose_name="Описание")  # Empty value
    features = models.TextField(blank=True, verbose_name="Характеристики")  # Empty value
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name="Цена")
    available = models.BooleanField(default=True, verbose_name="Наличие")
    stock = models.PositiveIntegerField(verbose_name="Количество")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    image = models.ImageField(upload_to=get_upload_path, blank=True,
                              verbose_name="Изображение товара")

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('lenivastore:product_detail', args=[self.id, self.slug])

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.brand_name)
    #     super(Brand, self).save(*args, **kwargs)
