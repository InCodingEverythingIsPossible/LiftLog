from django.db import models


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

    def __str__(self):
        return self.name
