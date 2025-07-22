from django.urls import path
from . import views

urlpatterns = [
    path('', views.templates_dashboard, name='templates_dashboard'),
    path('api/create_template/', views.create_template_api, name='create_template_api'),
    path('api/create-exercise/', views.create_exercise_api, name='create_exercise_api'),
]
