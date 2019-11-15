from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name="Пользователь")
    phone = PhoneNumberField(null=False, blank=False, unique=True,
                             verbose_name="Телефон")
    image = models.ImageField(default='default.jpg',
                              upload_to='profile_pics',
                              verbose_name="Изображение")

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,  *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
