from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
	class Meta:
		model = Task
		fields = ["task_name", "note", "start_date", "end_date"]
		
