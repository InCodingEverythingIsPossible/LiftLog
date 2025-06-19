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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='workout_templates'
    )

    def __str__(self):
        return self.name


class TemplateExercise(models.Model):
    template = models.ForeignKey(WorkoutTemplate, on_delete=models.CASCADE, related_name='template_exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.template.name} - {self.exercise.name}"


class ExerciseSet(models.Model):
    template_exercise = models.ForeignKey(TemplateExercise, on_delete=models.CASCADE, related_name='sets')
    kg = models.FloatField(default=0)
    reps = models.PositiveIntegerField(default=0)
    rest_timer = models.CharField(max_length=10, default="00:00")  # format mm:ss

    def __str__(self):
        return f"{self.kg}kg x {self.reps} reps ({self.rest_timer})"
