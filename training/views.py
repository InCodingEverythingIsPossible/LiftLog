import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import WorkoutTemplate, Exercise


def workout_template_list(request):

    user = request.user

    my_templates = WorkoutTemplate.objects.filter(user=user)
    example_templates = WorkoutTemplate.objects.filter(user__isnull=True)

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


@csrf_exempt
@login_required
def create_template_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    try:
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description', '')
        exercise_ids = data.get('exercise_ids', [])  # match key sent from JS

        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)

        # Create new WorkoutTemplate linked to the current user
        new_template = WorkoutTemplate.objects.create(
            user=request.user,
            name=name,
            description=description,
        )

        # Add exercises if provided
        if exercise_ids:
            exercises = Exercise.objects.filter(id__in=exercise_ids)
            new_template.exercises.set(exercises)

        return JsonResponse({
            'success': True,
            'template': {
                'id': new_template.id,
                'name': new_template.name,
                'description': new_template.description,
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def start_workout(request, template_id):
    template = get_object_or_404(WorkoutTemplate, id=template_id)
    return render(request, 'training/start_workout.html', {'template': template})
