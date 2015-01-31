from django.db import models

# Create your models here.
class TM(models.Model):
    pass

class TransUnit(models.Model):
    source = models.TextField(default='')
    target = models.TextField(default='')
    tm = models.ForeignKey(TM, default=None)

