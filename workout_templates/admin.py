from django.contrib import admin
from .models import WorkoutTemplate, Exercise, TemplateExercise, ExerciseSet

admin.site.register(WorkoutTemplate)
admin.site.register(Exercise)
admin.site.register(TemplateExercise)
admin.site.register(ExerciseSet)
