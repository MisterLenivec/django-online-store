from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Cupon(models.Model):
    code = models.CharField(max_length=50, unique=True,
                            verbose_name="Код купона")
    valid_from = models.DateTimeField(verbose_name="Действителен с")
    valid_to = models.DateTimeField(verbose_name="Действителен до")
    discount = models.IntegerField(validators=[MinValueValidator(0),
                                               MaxValueValidator(100)],
                                   verbose_name="Размер скидки")
    active = models.BooleanField(verbose_name="Активен")

    class Meta:
        ordering = ('active',)
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'

    def __str__(self):
        return self.code
