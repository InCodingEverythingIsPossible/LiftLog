from django.http import HttpResponse
from django.shortcuts import render
from .models import WorkoutTemplate


def workout_template_list(request):
    # My templates
    my_templates = WorkoutTemplate.objects.filter(name__in=["Pull A", "Pull B", "Push A", "Push B"])

    # Example templates
    example_templates = WorkoutTemplate.objects.exclude(name__in=["Pull A", "Pull B", "Push A", "Push B"])

    return render(request, 'training/template_list.html', {
        'my_templates': my_templates,
        'example_templates': example_templates,
        'my_templates_count': my_templates.count(),
        'example_templates_count': example_templates.count(),
    })


def start_workout(request, template_id):
    # Tu później dodasz logikę tworzenia sesji treningowej
    return HttpResponse(f"Rozpoczęto trening z szablonu {template_id}")
