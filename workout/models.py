from django.db import models
from django.conf import settings
from workout_templates.models import Exercise


class Workout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Workout by {self.user.username} on {self.date.strftime('%Y-%m-%d %H:%M')}"


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.exercise.name if self.exercise else 'Unknown Exercise'} - {self.workout}"


class WorkoutSet(models.Model):
    workout_exercise = models.ForeignKey(WorkoutExercise, on_delete=models.CASCADE, related_name='sets')
    kg = models.FloatField(default=0)
    reps = models.PositiveIntegerField(default=0)
    done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.kg}kg x {self.reps} reps - {'Done' if self.done else 'Not Done'}"
