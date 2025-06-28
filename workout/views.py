from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from templates_dashboard.models import Exercise, WorkoutTemplate
from workout.models import Workout, WorkoutExercise, WorkoutExerciseSet

import json


def start_workout(request, template_id):
    template = get_object_or_404(WorkoutTemplate, id=template_id)
    return render(request, 'workout/workout_session.html', {'template': template})


@csrf_exempt
@login_required
def save_workout_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=400)

    try:
        data = json.loads(request.body)
        exercises = data.get('exercises', [])

        # Create a new Workout object
        workout = Workout.objects.create(user=request.user, date=timezone.now())

        for item in exercises:
            exercise_id = item.get('exercise_id')
            sets_data = item.get('sets', [])

            try:
                exercise = Exercise.objects.get(id=exercise_id)
            except Exercise.DoesNotExist:
                continue  # skip invalid exercises

            # Create WorkoutExercise
            workout_ex = WorkoutExercise.objects.create(
                workout=workout,
                exercise=exercise
            )

            for s in sets_data:
                kg = s.get('kg', 0)
                reps = s.get('reps', 0)
                done = s.get('done', False)

                # Create WorkoutSet
                WorkoutExerciseSet.objects.create(
                    workout_exercise=workout_ex,
                    kg=kg,
                    reps=reps,
                    done=done
                )

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
