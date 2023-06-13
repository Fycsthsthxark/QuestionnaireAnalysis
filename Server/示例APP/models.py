from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.dateUtil import getNowTimeStamp, getSpecifyTimeStamp


# Create your models here.


class User(AbstractUser):
    """
    用户表
    """
    
    # username 在继承的父类里，无需重复定义

    uid = models.CharField(verbose_name='用户ID', max_length=255, null=False, primary_key=True)
    email = models.EmailField(verbose_name='邮箱', null=True, unique=True)
    bindCode = models.CharField(verbose_name='监护码', max_length=255, null=False, unique=True)
    gender = models.CharField(verbose_name='性别', max_length=255, null=True, default='男')
    birthday = models.CharField(verbose_name='出生日期', max_length=255, null=True,
                                default=getSpecifyTimeStamp(2023, 1, 1))
    creatTimeStamp = models.CharField(verbose_name='创建时间', max_length=255, null=True, default=getNowTimeStamp())
    headSculpture = models.ImageField(verbose_name='头像', null=True, upload_to="userHeadSculptures/",
                                      default=r"userHeadSculptures/default.png")

    class Meta:
        db_table = 'User'
        verbose_name = '用户表'
