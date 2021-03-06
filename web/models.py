from django.db import models
from django.contrib.auth.hashers import make_password


class User(models.Model):
    choices = (
        ('admin', 2),
        ('vip', 1),
        ('default', 0)
    )

    name = models.CharField(max_length=20, unique=True)
    user_password = models.CharField(max_length=200)
    role = models.CharField(choices=choices, default='default', max_length=10)

    @property
    def password(self):
        return self.user_password

    @password.setter
    def password(self, value):
        self.user_password = make_password(value)


class Movies(models.Model):
    name = models.CharField(max_length=30, unique=True)

