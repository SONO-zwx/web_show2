from django.db import models

# Create your models here.
class Shopname(models.Model):
    shopname = models.TextField(blank=True, null=True)
    superior = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shopname'


class Mouthinfo(models.Model):
    starttime = models.DateField(blank=True, null=True)
    endtime = models.DateField(blank=True, null=True)
    shopname = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mouthinfo'
