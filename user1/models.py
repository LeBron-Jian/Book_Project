from django.db import models

# Create your models here.
from django.utils import timezone

# 作者详情
class AuthorDetail(models.Model):
    age = models.IntegerField()
    addr = models.TextField()

# 出版社类
class Publisher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

# 书类
class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    publish_date = models.DateTimeField(default=timezone.now())

    # 书只能关联一个出版社，外键通常建在多的那一边
    publisher = models.ForeignKey(to='Publisher', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# 作者类
class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16)

    # 多对多
    books = models.ManyToManyField(to='Book', related_name='authors')

    detail = models.OneToOneField(to='AuthorDetail', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



# 登录注册的用户信息
class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16)
    pwd = models.CharField(max_length=32)