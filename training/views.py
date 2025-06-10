from django.http import HttpResponse
from django.shortcuts import render
from .models import WorkoutTemplate

def workout_template_list(request):
    my_templates = WorkoutTemplate.objects.filter(name__in=["Pull A", "Pull B", "Push A", "Push B"])
    example_templates = WorkoutTemplate.objects.exclude(name__in=["Pull A", "Pull B", "Push A", "Push B"])

    # Przygotuj dane dla JS jako lista słowników
    templates_data = []

    for t in my_templates.union(example_templates):
        templates_data.append({
            'id': t.id,
            'name': t.name,
            'description': t.description,
            'exercises': [],  # dodaj ćwiczenia jeśli masz model ćwiczeń
        })

    return render(request, 'training/template_list.html', {
        'my_templates': my_templates,
        'example_templates': example_templates,
        'my_templates_count': my_templates.count(),
        'example_templates_count': example_templates.count(),
        'templates_data_json': templates_data,
    })


def start_workout(request, template_id):
    # Tu później dodasz logikę tworzenia sesji treningowej
    return HttpResponse(f"Rozpoczęto trening z szablonu {template_id}")
