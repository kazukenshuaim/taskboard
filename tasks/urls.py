from django.urls import path
from .views import (
    TaskListView, TaskDetailView,
    TaskCreateView, TaskUpdateView, TaskDeleteView,
    TaskStatusUpdateView,
)

app_name = 'tasks'

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('<int:pk>/status/', TaskStatusUpdateView.as_view(), name='task_status_update'),
]