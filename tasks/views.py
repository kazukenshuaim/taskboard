from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Category, Task
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from .forms import TaskForm
from django.db.models import Q
from django.contrib import messages


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        queryset = Task.objects.filter(created_by=self.request.user)

        keyword = self.request.GET.get('q', '').strip()
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(description__icontains=keyword)
            )

        status = self.request.GET.get('status', '')
        if status:
            queryset = queryset.filter(status=status)

        category_id = self.request.GET.get('category', '')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(created_by=self.request.user)
        context['status_choices'] = Task.STATUS_CHOICES
        # 現在の検索条件をテンプレートに渡す（フォームの入力値を維持するため）
        context['current_q'] = self.request.GET.get('q', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['current_category'] = self.request.GET.get('category', '')
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        # 自分のタスクだけアクセス可能にする（他人のタスク URL に直アクセスすると 404）
        return Task.objects.filter(created_by=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # カテゴリの選択肢をログインユーザーのものだけに絞る
        form.fields['category'].queryset = self.request.user.categories.all()
        return form
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f'タスク「{form.instance.title}」を作成しました。')
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'

    def get_success_url(self):
        return reverse_lazy('tasks:task_detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['category'].queryset = self.request.user.categories.all()
        return form

    def form_valid(self, form):
        messages.success(self.request, f'タスク「{form.instance.title}」を更新しました。')
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task_list')

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, f'タスク「{self.object.title}」を削除しました。')
        return super().form_valid(form)


class TaskStatusUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, created_by=request.user)
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
            messages.success(request, f'ステータスを「{task.get_status_display()}」に変更しました。')
        return redirect('tasks:task_detail', pk=pk)


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'tasks/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(created_by=self.request.user)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = 'tasks/category_form.html'
    success_url = reverse_lazy('tasks:category_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'tasks/category_confirm_delete.html'
    success_url = reverse_lazy('tasks:category_list')

    def get_queryset(self):
        return Category.objects.filter(created_by=self.request.user)