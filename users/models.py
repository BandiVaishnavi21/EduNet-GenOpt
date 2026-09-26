from django.db import models


class User(models.Model):

    user_name = models.CharField(max_length=100)

    password = models.CharField(max_length=128)

    mobile_number = models.CharField(max_length=15)

    place = models.CharField(max_length=100)

    def __str__(self):
        return self.user_name