from django.db import models

# Create your models here.
class Account(models.Model):
    shopname = models.TextField(blank=True, null=True)
    account = models.TextField(blank=True, null=True)
    types = models.TextField(blank=True, null=True)
    effect = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    isuse = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account'


class Gongaccount(models.Model):
    account = models.TextField(blank=True, null=True)
    types = models.TextField(blank=True, null=True)
    effect = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    shopname = models.TextField(blank=True, null=True)
    isuse = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gongaccount'


class Shopname(models.Model):
    shopname = models.TextField(blank=True, null=True)
    superior = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shopname'


class Receipts(models.Model):
    iszi = models.CharField(max_length=2, blank=True, null=True)
    types = models.TextField(blank=True, null=True)
    paymentaccout = models.TextField(blank=True, null=True)
    paymenttyoe = models.TextField(blank=True, null=True)
    shopname = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    allprice = models.FloatField(blank=True, null=True)
    responsibleperson = models.TextField(blank=True, null=True)
    finance = models.TextField(blank=True, null=True)
    generalmanager = models.TextField(blank=True, null=True)
    dates = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    zhichupaymentaccout = models.TextField(blank=True, null=True)
    zhidates = models.DateField(blank=True, null=True)
    zhitype = models.TextField(blank=True, null=True)
    yuzhi = models.TextField(blank=True, null=True)
    ergeneralmanager = models.TextField(blank=True, null=True)
    erremarks = models.TextField(blank=True, null=True)
    userid = models.TextField(blank=True, null=True)
    jietype = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'receipts'


class Dealproject(models.Model):
    projectname = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    issure = models.IntegerField()
    receiptsid = models.TextField(blank=True, null=True)
    types = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dealproject'


class CertificateImg(models.Model):
    img_url = models.ImageField(upload_to='photos/', max_length=100, blank=True, null=True)
    for_id = models.TextField(blank=True, null=True)
    onloadinfo = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'certificate_img'


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


class Category(models.Model):
    one = models.TextField(blank=True, null=True)
    two = models.TextField(blank=True, null=True)
    isapprover = models.TextField(blank=True, null=True)
    superior = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class Newcategory(models.Model):
    one = models.TextField(blank=True, null=True)
    two = models.TextField(blank=True, null=True)
    isapprover = models.TextField(blank=True, null=True)
    superior = models.TextField(blank=True, null=True)
    classname = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'newcategory'


class Waicaidealinfo(models.Model):
    brand = models.CharField(max_length=20, blank=True, null=True)
    motorcycle = models.TextField(blank=True, null=True)
    productname = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    unit = models.FloatField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    manay = models.FloatField(blank=True, null=True)
    forid = models.TextField(blank=True, null=True)
    jiesuan_status = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'waicaidealinfo'


class Waicaiinfo(models.Model):
    shopname = models.TextField(blank=True, null=True)
    gongaccount = models.TextField(blank=True, null=True)
    ordernumber = models.TextField(blank=True, null=True)
    brand = models.CharField(max_length=20, blank=True, null=True)
    motorcycle = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    forid = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    jiesuan_status = models.TextField(blank=True, null=True)
    tijiaodata = models.DateField(blank=True, null=True)
    zhidates = models.DateField(blank=True, null=True)
    sansong = models.FloatField(blank=True, null=True)
    allprice = models.FloatField(blank=True, null=True)
    yunfei = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'waicaiinfo'


class Vinimg(models.Model):
    img_url = models.ImageField(upload_to='vinimg/', blank=True, null=True)  # 指定图片上传路径，即media/photos/
    for_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vinimg'

class Carinfoimg(models.Model):
    img_url = models.ImageField(upload_to='carinfoimg/', blank=True, null=True)  # 指定图片上传路径，即media/photos/
    for_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carinfoimg'


class Kindsimg(models.Model):
    img_url = models.ImageField(upload_to='kindsimg/', blank=True, null=True)  # 指定图片上传路径，即media/photos/
    for_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kindsimg'


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



class Income(models.Model):
    dates = models.TextField(blank=True, null=True)
    shopname = models.TextField(blank=True, null=True)
    payment_account = models.TextField(blank=True, null=True)
    payment_term = models.TextField(blank=True, null=True)
    allprice = models.FloatField(blank=True, null=True)
    submitremark = models.TextField(blank=True, null=True)
    approverinfo = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    order_type = models.TextField(blank=True, null=True)
    finance = models.TextField(blank=True, null=True)
    zhidates = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'income'


class IncomeDealproject(models.Model):
    project_name = models.TextField(blank=True, null=True)
    explains = models.TextField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    for_id = models.IntegerField(blank=True, null=True)
    order_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'income_dealproject'


class IncomeImg(models.Model):
    img_url = models.ImageField(upload_to='IncomeImg/', blank=True, null=True)
    for_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'income_img'


class Commentreturn(models.Model):
    shopname = models.TextField(blank=True, null=True)
    dates = models.TextField(blank=True, null=True)
    consignee = models.TextField(blank=True, null=True)
    operator = models.TextField(blank=True, null=True)
    company = models.TextField(blank=True, null=True)
    people = models.TextField(blank=True, null=True)
    license_plate = models.TextField(blank=True, null=True)
    submitremark = models.TextField(blank=True, null=True)
    approverinfo = models.TextField(blank=True, null=True)
    allprice = models.FloatField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    order_type = models.TextField(blank=True, null=True)
    finance = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commentreturn'


class CommentreturnDealproject(models.Model):
    order_num = models.TextField(blank=True, null=True)
    product_name = models.TextField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    for_id = models.IntegerField(blank=True, null=True)
    order_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commentreturn_dealproject'


class CommentreturnImg(models.Model):
    img_url = models.ImageField(upload_to='CommentreturnImg/', blank=True, null=True)
    for_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'commentreturn_img'


class Invoice(models.Model):
    dates = models.TextField(blank=True, null=True)
    shopname = models.TextField(blank=True, null=True)
    agent = models.TextField(blank=True, null=True)
    collection_method = models.TextField(blank=True, null=True)
    customer_name = models.TextField(blank=True, null=True)
    phone = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    approverinfo = models.TextField(blank=True, null=True)
    order_type = models.TextField(blank=True, null=True)
    finance = models.TextField(blank=True, null=True)
    zhidates = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoice'


class InvoiceDealproject(models.Model):
    company_name = models.TextField(blank=True, null=True)
    duty_paragraph = models.TextField(blank=True, null=True)
    invoice_type = models.TextField(db_column='Invoice_type', blank=True, null=True)  # Field name made lowercase.
    invoice_amount = models.FloatField(blank=True, null=True)
    for_id = models.IntegerField(blank=True, null=True)
    order_type = models.TextField(blank=True, null=True)
    site = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoice_dealproject'


class InvoiceImg(models.Model):
    img_url = models.ImageField(upload_to='InvoiceImg/', blank=True, null=True)
    for_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoice_img'
