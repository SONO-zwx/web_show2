from django.db import models


# Create your models here.
class Wasteuser(models.Model):
    username = models.TextField(blank=True, null=True)
    cashpledge = models.TextField(blank=True, null=True)
    expirydate = models.DateField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wasteuser'


class Wastesubsidiary(models.Model):
    wastepro = models.CharField(max_length=10, blank=True, null=True)
    starttime = models.DateField(blank=True, null=True)
    endtime = models.DateField(blank=True, null=True)
    datetimes = models.DateField(blank=True, null=True)
    wasteuser = models.TextField(blank=True, null=True)
    number = models.FloatField(blank=True, null=True)
    zhimanay = models.FloatField(blank=True, null=True)
    shopname = models.TextField(blank=True, null=True)
    shenremarks = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    responsibleperson = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wastesubsidiary'


class Wastepro(models.Model):
    project = models.CharField(max_length=10, blank=True, null=True)
    unit = models.FloatField(blank=True, null=True)
    units = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wastepro'


class Shopname(models.Model):
    shopname = models.TextField(blank=True, null=True)
    superior = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shopname'


class Wastesdealinfo(models.Model):
    wastepro = models.CharField(max_length=10, blank=True, null=True)
    number = models.FloatField(blank=True, null=True)
    zhimanay = models.FloatField(blank=True, null=True)
    forid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wastesdealinfo'


class WasteImg(models.Model):
    img_url = models.ImageField(upload_to='wastephotos/', max_length=100, blank=True, null=True)
    for_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'waste_img'


class Wasteusermanay(models.Model):
    name = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    manay = models.TextField(blank=True, null=True)
    for_id = models.TextField(blank=True, null=True)
    datatimes = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wasteusermanay'


class Newcategory(models.Model):
    one = models.TextField(blank=True, null=True)
    two = models.TextField(blank=True, null=True)
    isapprover = models.TextField(blank=True, null=True)
    superior = models.TextField(blank=True, null=True)
    classname = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'newcategory'


class UserRight(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    proinfo = models.TextField(blank=True, null=True)
    tablename = models.TextField(blank=True, null=True)
    conductor = models.TextField(blank=True, null=True)
    rightname = models.TextField(blank=True, null=True)
    lastuser_right = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_right'
