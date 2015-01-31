from django.db import models

# Create your models here.
class TransUnit(models.Model):
    source = models.TextField(default='')
    target = models.TextField(default='')
