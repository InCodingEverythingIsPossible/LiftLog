from django.db import models


class WorkoutTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    workout_template = models.ForeignKey(WorkoutTemplate, related_name='exercises', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    sets = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name
