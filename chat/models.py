from django.db import models


# Create your models here.


class User(models.Model):
    user_name = models.CharField(max_length=16, primary_key=True)
    passwd = models.CharField(max_length=200)


class AppToken(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    app_token = models.CharField(max_length=200)
    ttl = models.DateTimeField('date published')
