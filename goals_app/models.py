from django.conf import settings
from django.db import models

from datetime import date


class GoalTemplate(models.Model):
    todo = models.CharField(max_length=100)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateField(default=date.today)
    finish_date = models.DateField()
    is_achieved = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return self.todo


class Goal(GoalTemplate):
    reason = models.CharField(max_length=200)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, related_name='goals'
    )


class Subtask(GoalTemplate):
    goal = models.ForeignKey(
        Goal, on_delete=models.CASCADE, related_name='subtasks'
    )


class CategoryManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)

    objects = CategoryManager()
