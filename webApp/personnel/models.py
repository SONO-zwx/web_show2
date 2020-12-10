from django.db import models


class Staffs(models.Model):
    staff_name = models.CharField(max_length=10, blank=True, null=True)
    shopname = models.CharField(db_column='ShopName', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    post = models.CharField(max_length=10, blank=True, null=True)
    stafftype = models.CharField(max_length=20, blank=True, null=True)
    idtypes = models.CharField(db_column='IDtypes', max_length=20, blank=True,
                               null=True)  # Field name made lowercase.
    idcard = models.CharField(db_column='IDcard', max_length=20, blank=True,
                              null=True)  # Field name made lowercase.
    idcardstart = models.CharField(db_column='IDcardstart', max_length=20, blank=True,
                                   null=True)  # Field name made lowercase.
    idcardend = models.CharField(db_column='IDcardend', max_length=20, blank=True,
                                 null=True)  # Field name made lowercase.
    gex = models.CharField(max_length=1, blank=True, null=True)
    nationality = models.CharField(max_length=10, blank=True, null=True)
    marstatus = models.CharField(max_length=10, blank=True, null=True)
    cardno = models.CharField(db_column='CardNo', max_length=20, blank=True,
                              null=True)  # Field name made lowercase.
    nation = models.CharField(max_length=10, blank=True, null=True)
    politicsstatus = models.CharField(max_length=10, blank=True, null=True)
    nativeplace = models.CharField(max_length=10, blank=True, null=True)
    censustypes = models.CharField(max_length=10, blank=True, null=True)
    censuslocation = models.CharField(max_length=10, blank=True, null=True)
    staffhome = models.CharField(max_length=100, blank=True, null=True)
    dateofbirth = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    dateonboard = models.DateField(blank=True, null=True)
    workingage = models.TextField(blank=True, null=True)
    contractexpirationdate = models.DateField(db_column='Contractexpirationdate', blank=True,
                                              null=True)  # Field name made lowercase.
    unsubmittedinformation = models.TextField(db_column='Unsubmittedinformation', blank=True,
                                              null=True)  # Field name made lowercase.
    openingbank = models.TextField(blank=True, null=True)
    bankid = models.TextField(blank=True, null=True)
    corporation = models.TextField(blank=True, null=True)
    office = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    departure_date = models.DateField(db_column='Departure_date', blank=True,
                                      null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'staffs'


class Shopname(models.Model):
    shopname = models.TextField(blank=True, null=True)
    superior = models.TextField(blank=True, null=True)
    types = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shopname'


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


class Users(models.Model):
    username = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    shopname = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    limits = models.TextField(blank=True, null=True)
    superior = models.TextField(blank=True, null=True)
    oneapprover = models.TextField(blank=True, null=True)
    twoapprover = models.TextField(blank=True, null=True)
    submit = models.TextField(blank=True, null=True)
    isuse = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


