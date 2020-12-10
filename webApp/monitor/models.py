from django.db import models

# Create your models here.
class Cameralist(models.Model):
    cameraname = models.TextField(blank=True, null=True)
    shopnameid = models.TextField(blank=True, null=True)
    superior = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cameralist'

class Picturessoninfo(models.Model):
    dates = models.DateField(blank=True, null=True)
    times = models.TimeField(blank=True, null=True)
    pictures = models.TextField(blank=True, null=True)
    okpictures = models.TextField(blank=True, null=True)
    isok = models.IntegerField(blank=True, null=True)
    ispunish = models.IntegerField(blank=True, null=True)
    pubish = models.TextField(blank=True, null=True)
    pubishuser = models.TextField(blank=True, null=True)
    pubishmanay = models.FloatField(blank=True, null=True)
    isokname = models.TextField(blank=True, null=True)
    isokdatatime = models.DateTimeField(blank=True, null=True)
    isokremark = models.TextField(blank=True, null=True)
    mainid = models.IntegerField(blank=True, null=True)
    userid = models.IntegerField(blank=True, null=True)
    cameralistid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'picturessoninfo'


class Picturesmaininfo(models.Model):
    shopnameid = models.TextField(blank=True, null=True)
    superior = models.TextField(blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    oknumber = models.IntegerField(blank=True, null=True)
    nonumber = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'picturesmaininfo'


class Punish(models.Model):
    project = models.TextField(blank=True, null=True)
    number = models.FloatField(blank=True, null=True)
    staffname = models.CharField(max_length=20, blank=True, null=True)
    standard = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    corporation = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    datatimes = models.DateTimeField(blank=True, null=True)
    shopname = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'punish'


class Punishimg(models.Model):
    img_url = models.ImageField(max_length=100, blank=True, null=True)
    for_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'punishimg'


class Performance(models.Model):
    project = models.TextField(blank=True, null=True)
    particulars = models.TextField(blank=True, null=True)
    post = models.TextField(blank=True, null=True)
    corporation = models.TextField(blank=True, null=True)
    fenzhi = models.IntegerField(blank=True, null=True)
    isus = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'performance'
