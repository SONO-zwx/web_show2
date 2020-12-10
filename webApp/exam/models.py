from django.db import models

# Create your models here.
class ExamAnswerMain(models.Model):
    name = models.TextField(blank=True, null=True)
    answer_date = models.DateField(blank=True, null=True)
    exam_name_id = models.TextField(blank=True, null=True)
    exam_grade = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exam_answer_main'


class Shopname(models.Model):
    shopname = models.TextField(blank=True, null=True)
    superior = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shopname'


class ExamName(models.Model):
    name = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    superior = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exam_name'



class ExamOption(models.Model):
    exam_name_id = models.TextField(blank=True, null=True)
    topic_id = models.TextField(blank=True, null=True)
    option_id = models.TextField(blank=True, null=True)
    option_body = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exam_option'


class ExamTopic(models.Model):
    exam_name_id = models.TextField(blank=True, null=True)
    topic_id = models.TextField(blank=True, null=True)
    topic_body = models.TextField(blank=True, null=True)
    topic_answer = models.TextField(blank=True, null=True)
    goal = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exam_topic'


class ExamUsersAnswer(models.Model):
    answer_main_id = models.TextField(blank=True, null=True)
    exam_name_id = models.TextField(blank=True, null=True)
    topic_id = models.TextField(blank=True, null=True)
    users_answer = models.TextField(blank=True, null=True)
    topic_answer = models.TextField(blank=True, null=True)
    goal = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exam_users_answer'