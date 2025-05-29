from django.db import models

# Create your models here.


class APIkey(models.Model):
    key = models.CharField(max_length=255)


class Login(models.Model):
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username
