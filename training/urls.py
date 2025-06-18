from django.urls import path
from . import views

urlpatterns = [
    path('', views.workout_template_list, name='workout_template_list'),
    path('start/<int:template_id>/', views.start_workout, name='start_workout'),
    path('api/create_template/', views.create_template_api, name='create_template_api'),
    path('api/save_workout/', views.save_workout_api, name='save_workout_api'),
]