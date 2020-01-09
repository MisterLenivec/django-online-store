from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import io
from django.core.files.storage import default_storage as storage

from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name="Пользователь")
    phone = PhoneNumberField(null=False, blank=True, verbose_name="Телефон")
    image = models.ImageField(default='default.jpg',
                              upload_to='profile_pics',
                              verbose_name="Изображение")

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img_read = storage.open(self.image.name, 'r')
        img = Image.open(img_read)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            in_mem_file = io.BytesIO()
            img.convert('RGB').save(in_mem_file, format='JPEG')
            img_write = storage.open(self.image.name, 'w+')
            img_write.write(in_mem_file.getvalue())
            img_write.close()

        img_read.close()
