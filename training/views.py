from django.http import HttpResponse
from django.shortcuts import render
from .models import WorkoutTemplate, Exercise


def workout_template_list(request):
    my_templates = WorkoutTemplate.objects.filter(name__in=["Pull A", "Pull B", "Push A", "Push B"])
    example_templates = WorkoutTemplate.objects.exclude(name__in=["Pull A", "Pull B", "Push A", "Push B"])

    # Prepare data for JS as a list of dictionaries
    templates_data = []
    for t in my_templates.union(example_templates):
        templates_data.append({
            'id': t.id,
            'name': t.name,
            'description': t.description,
            'exercises': [
                {
                    'name': e.name,
                    'sets': e.sets,
                    'primary_muscle': e.primary_muscle
                } for e in t.exercises.all()
            ],
        })

    # New block - pass all exercises
    exercises = Exercise.objects.all()
    exercises_data = [
        {
            'id': ex.id,
            'name': ex.name,
            'primary_muscle': ex.primary_muscle,
        }
        for ex in exercises
    ]

    return render(request, 'training/template_list.html', {
        'my_templates': my_templates,
        'example_templates': example_templates,
        'my_templates_count': my_templates.count(),
        'example_templates_count': example_templates.count(),
        'templates_data_json': templates_data,
        'exercises_data_json': exercises_data,
    })


def start_workout(request, template_id):
    # Later add the logic for creating a training session
    return HttpResponse(f"Workout started {template_id}")
