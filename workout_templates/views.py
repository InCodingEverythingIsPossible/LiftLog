import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .models import Exercise, WorkoutTemplate, WorkoutExerciseTemplate, WorkoutExerciseSetTemplate
import logging


def workout_template_list(request):
    user = request.user

    my_templates = WorkoutTemplate.objects.filter(user=user)
    example_templates = WorkoutTemplate.objects.filter(user__isnull=True)

    templates_data = []

    # Loop through all templates (user's and example ones)
    for t in my_templates.union(example_templates):
        exercises_list = []

        # Loop through each WorkoutExerciseTemplate related to the template
        for te in t.workout_exercises_template.select_related('exercise').prefetch_related('sets'):
            # Collect set data for each WorkoutExerciseTemplate
            sets_data = [
                {
                    'kg': s.kg,
                    'reps': s.reps,
                    'rest': s.rest_timer
                }
                for s in te.sets.all()
            ]

            # Prepare exercise entry with sets
            exercises_list.append({
                'name': te.exercise.name,
                'primary_muscle': te.exercise.primary_muscle,
                'sets': sets_data
            })

        # Prepare full template dictionary for JS
        templates_data.append({
            'id': t.id,
            'name': t.name,
            'description': t.description,
            'exercises': exercises_list,
        })

    # Pass all available exercises for the exercise picker in the UI
    exercises = Exercise.objects.all()

    muscle_choices = Exercise.MUSCLE_CHOICES
    equipment_choices = Exercise.EQUIPMENT_CHOICES

    exercises_data = [
        {
            'id': ex.id,
            'name': ex.name,
            'primary_muscle': ex.primary_muscle,
        }
        for ex in exercises
    ]

    return render(request, 'workout_templates/template_list.html', {
        'my_templates': my_templates,
        'example_templates': example_templates,
        'my_templates_count': my_templates.count(),
        'example_templates_count': example_templates.count(),
        'templates_data_json': templates_data,
        'exercises_data_json': exercises_data,
        'muscle_choices': muscle_choices,
        'equipment_choices': equipment_choices,
    })


logger = logging.getLogger(__name__)


@csrf_exempt
@login_required
def create_template_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    try:
        data = json.loads(request.body)
        logger.info(f"Received data: {data}")

        name = data.get('name')
        description = data.get('description', '')
        exercises_data = data.get('exercises', [])

        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)

        new_template = WorkoutTemplate.objects.create(
            user=request.user,
            name=name,
            description=description,
        )

        for ex_data in exercises_data:
            exercise_id = ex_data.get('exerciseId')
            sets = ex_data.get('sets', [])

            try:
                exercise = Exercise.objects.get(id=exercise_id)
            except Exercise.DoesNotExist:
                logger.warning(f"Exercise not found: {exercise_id}")
                continue

            template_exercise = WorkoutExerciseTemplate.objects.create(
                template=new_template,
                exercise=exercise
            )

            for set_data in sets:
                logger.info(f"Creating ExerciseSet: {set_data}")
                WorkoutExerciseSetTemplate.objects.create(
                    template_exercise=template_exercise,
                    kg=set_data.get('kg', 0),
                    reps=set_data.get('reps', 0),
                    rest_timer=set_data.get('rest', '00:00')
                )

        return JsonResponse({
            'success': True,
            'template': {
                'id': new_template.id,
                'name': new_template.name,
                'description': new_template.description,
            }
        })

    except Exception as e:
        logger.error(f"Error in create_template_api: {e}")
        return JsonResponse({'error': str(e)}, status=500)


@require_POST
@login_required
def create_exercise_api(request):
    name = request.POST.get('name')
    primary_muscle = request.POST.get('primary_muscle')
    equipment = request.POST.get('equipment')

    # Validation
    if not name or not primary_muscle or not equipment:
        return JsonResponse({'error': 'Missing required fields.'}, status=400)

    exercise = Exercise.objects.create(
        name=name,
        primary_muscle=primary_muscle,
        equipment=equipment
    )

    return JsonResponse({
        'id': exercise.id,
        'name': exercise.name,
        'primary_muscle': exercise.primary_muscle,
        'equipment': exercise.equipment,
    })
