from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    shopname = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    limits = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class Shopname(models.Model):
    shopname = models.TextField(blank=True, null=True)
    superior = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shopname'


class Limits(models.Model):
    shopname = models.TextField(blank=True, null=True)
    limits = models.TextField(blank=True, null=True)
    superior = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'limits'