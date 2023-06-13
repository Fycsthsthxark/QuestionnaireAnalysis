from django.db import models


# Create your models here.
class QuestionnaireRecords(models.Model):
    """
    问卷记录表
    """

    uid = models.CharField(verbose_name='记录ID', max_length=255, null=False, primary_key=True)
    problemList = models.TextField(verbose_name='答题记录', null=False)

    class Meta:
        db_table = 'QuestionnaireRecords'
        verbose_name = '问卷记录表'
