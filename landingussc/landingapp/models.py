from django.db import models
from django.contrib.auth.models import User


class DataFragment(models.Model):
    script = models.TextField()
    explanation = models.TextField()
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    score = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.script


class Script(models.Model):
    code = models.TextField()

    def __str__(self):
        return self.code