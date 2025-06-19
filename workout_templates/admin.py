from django.contrib import admin
from .models import Exercise, WorkoutTemplate, WorkoutExerciseTemplate, WorkoutExerciseSetTemplate

admin.site.register(Exercise)
admin.site.register(WorkoutTemplate)
admin.site.register(WorkoutExerciseTemplate)
admin.site.register(WorkoutExerciseSetTemplate)
