# Generated by Django 5.2.2 on 2025-06-19 22:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout_templates', '0008_remove_workoutexercise_workout_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='templateexercise',
            name='exercise',
        ),
        migrations.RemoveField(
            model_name='templateexercise',
            name='template',
        ),
        migrations.CreateModel(
            name='WorkoutExerciseTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout_templates.exercise')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workout_exercises_template', to='workout_templates.workouttemplate')),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutExerciseSetTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kg', models.FloatField(default=0)),
                ('reps', models.PositiveIntegerField(default=0)),
                ('rest_timer', models.CharField(default='00:00', max_length=10)),
                ('template_exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workout_exercise_sets_template', to='workout_templates.workoutexercisetemplate')),
            ],
        ),
        migrations.DeleteModel(
            name='ExerciseSet',
        ),
        migrations.DeleteModel(
            name='TemplateExercise',
        ),
    ]
