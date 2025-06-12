from django.db import models
from django.conf import settings


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    sets = models.IntegerField(default=3)
    primary_muscle = models.CharField(
        max_length=100,
        choices=[
            ('Chest', 'Chest'),
            ('Back', 'Back'),
            ('Legs', 'Legs'),
            ('Arms', 'Arms'),
            ('Shoulders', 'Shoulders'),
            ('Core', 'Core'),
        ],
        default='Chest'
    )

    def __str__(self):
        return self.name


class WorkoutTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    exercises = models.ManyToManyField(Exercise, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='workout_templates'
    )

    def __str__(self):
        return self.name
