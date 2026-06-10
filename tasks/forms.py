from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_date', 'category', 'assigned_to']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),   # ブラウザの日付ピッカーを使う
            'description': forms.Textarea(attrs={'rows': 4}),
        }
