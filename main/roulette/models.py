from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    users = models.ManyToManyField(User, null=True, blank=True)
    is_actual = models.BooleanField(default=True)


class Cell(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=10)
    weight = models.IntegerField()
    game = models.ForeignKey(Game, null=True, blank=True, on_delete=models.SET_NULL)
    is_actual = models.BooleanField(default=True)
