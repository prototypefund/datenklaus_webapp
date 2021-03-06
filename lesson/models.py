from django.db import models
# Create your models here.
from django.db.models import CASCADE, SET_NULL

from student.models import Student
from teacher.models import Room


class SliderCardModel(models.Model):
    student = models.ForeignKey(Student, on_delete=CASCADE)
    room = models.ForeignKey(Room, on_delete=CASCADE)
    state = models.IntegerField()
    selected_value = models.IntegerField(null=True)


class LessonStateModel(models.Model):
    student = models.ForeignKey(Student, on_delete=SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=CASCADE)
    state = models.IntegerField()
    previous_state = models.IntegerField(null=True)
    choice = models.TextField(null=True)
