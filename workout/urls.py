from django.urls import path
from . import views

app_name = 'workout'

urlpatterns = [
    # Start a workout based on a selected template
    path('start/<int:template_id>/', views.start_workout, name='start_workout'),

    # API endpoint to save workout progress
    path('api/save/', views.save_workout_api, name='save_workout'),
]