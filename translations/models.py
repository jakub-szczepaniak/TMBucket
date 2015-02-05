from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class TM(models.Model):

    def get_absolute_url(self):
        return reverse('view_tms', args=[self.id])

class TransUnit(models.Model):
    source = models.TextField(default='')
    target = models.TextField(default='')
    tm = models.ForeignKey(TM, default=None)

