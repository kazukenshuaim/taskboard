from django.urls import path
from .views import (
    TaskListView, TaskDetailView,
    TaskCreateView, TaskUpdateView, TaskDeleteView,
    TaskStatusUpdateView,
    CategoryListView, CategoryCreateView, CategoryDeleteView,
)

app_name = 'tasks'

urlpatterns = [
    # タスク
    path('', TaskListView.as_view(), name='task_list'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('<int:pk>/status/', TaskStatusUpdateView.as_view(), name='task_status_update'),
    # カテゴリ
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
]