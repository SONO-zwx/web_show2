from django.db import models

# Create your models here.
class MirrorInfo(models.Model):
    shopname = models.TextField(blank=True, null=True)
    datetimes = models.DateTimeField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mirror_info'
