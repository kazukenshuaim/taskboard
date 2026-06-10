from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('tasks:task_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # 登録後に自動ログイン
        return response
