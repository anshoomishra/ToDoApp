from django.urls import path
from task.views import TaskListCreateView
urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
]