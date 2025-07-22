from django.db import models
from django.conf import settings


class Exercise(models.Model):
    EQUIPMENT_CHOICES = [
        ('Barbell', 'Barbell'),
        ('Dumbbell', 'Dumbbell'),
        ('Machine', 'Machine'),
        ('Cable', 'Cable'),
        ('Bodyweight', 'Bodyweight'),
        ('Kettlebell', 'Kettlebell'),
        ('Other', 'Other'),
    ]

    MUSCLE_CHOICES = [
        ('Chest', 'Chest'),
        ('Back', 'Back'),
        ('Legs', 'Legs'),
        ('Arms', 'Arms'),
        ('Shoulders', 'Shoulders'),
        ('Core', 'Core'),
    ]

    name = models.CharField(max_length=100)
    primary_muscle = models.CharField(
        max_length=100,
        choices=MUSCLE_CHOICES,
        default='Chest'
    )
    equipment = models.CharField(
        max_length=50,
        choices=EQUIPMENT_CHOICES,
        default='Barbell'
    )

    def __str__(self):
        return f"{self.name} ({self.primary_muscle}, {self.equipment})"


class WorkoutTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='templates_dashboard'
    )

    def __str__(self):
        return self.name


class WorkoutExerciseTemplate(models.Model):
    template = models.ForeignKey(WorkoutTemplate, on_delete=models.CASCADE, related_name='workout_exercises_template')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.template.name} - {self.exercise.name}"


class WorkoutExerciseSetTemplate(models.Model):
    template_exercise = models.ForeignKey(WorkoutExerciseTemplate, on_delete=models.CASCADE,
                                          related_name='workout_exercise_sets_template')
    kg = models.FloatField(default=0)
    reps = models.PositiveIntegerField(default=0)
    rest_timer = models.CharField(max_length=10, default="00:00")  # format mm:ss

    def __str__(self):
        return f"{self.kg}kg x {self.reps} reps ({self.rest_timer})"
