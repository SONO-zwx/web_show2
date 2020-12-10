from django.db import models

# Create your models here.
class WechatInfo(models.Model):
    msg = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wechat_info'
