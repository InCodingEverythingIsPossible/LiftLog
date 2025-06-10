from django.urls import path
from . import views

urlpatterns = [
    path('', views.workout_template_list, name='template_list'),
    path('start/<int:template_id>/', views.start_workout, name='start_workout'),
]