from .views import ListAllTasksApi, DetailUpdateDeleteTaskApi, ListUserTasksApi, CreateTaskApp
from django.urls import path

urlpatterns = [
    path('', ListAllTasksApi.as_view()),
    path('<int:pk>/', DetailUpdateDeleteTaskApi.as_view(), name='task_detail'),
    path('my-tasks/', ListUserTasksApi.as_view()),
    path('create/', CreateTaskApp.as_view(), name='task_create'),
]