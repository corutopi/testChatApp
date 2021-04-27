from django.db import models


# Create your models here.


class User(models.Model):
    user_id = models.CharField(max_length=16, primary_key=True)
    user_passwd = models.CharField(max_length=200)


class AppToken(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    app_token = models.CharField(max_length=200)
    ttl = models.DateTimeField('date published')
