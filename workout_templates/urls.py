from django.urls import path
from . import views

urlpatterns = [
    path('', views.workout_template_list, name='workout_template_list'),
    path('api/create_template/', views.create_template_api, name='create_template_api'),
]
