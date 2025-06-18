from django.contrib import admin
from .models import WorkoutTemplate, Exercise, TemplateExercise, ExerciseSet, WorkoutExercise, WorkoutSet, Workout

admin.site.register(WorkoutTemplate)
admin.site.register(Exercise)
admin.site.register(TemplateExercise)
admin.site.register(ExerciseSet)
admin.site.register(WorkoutExercise)
admin.site.register(WorkoutSet)
admin.site.register(Workout)
