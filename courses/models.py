from django.conf import settings as django_settings
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

class Course(models.Model):
    title = models.CharField(verbose_name='titles', blank=False)
    price = models.DecimalField(verbose_name='prices', max_digits=9, decimal_places=2)
    author = models.CharField(verbose_name='authors')
    image = models.ImageField(verbose_name='images', storage=django_settings.IMAGES_STORAGE)
    link = models.URLField(verbose_name='links')


class CompletedCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
