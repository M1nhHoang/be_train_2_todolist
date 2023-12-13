from django.urls import path
from .views import *

app_name = 'task'
urlpatterns = [
	path('', TaskView.as_view(), name='main_page'),
    path('details/<int:task_id>', task_details, name='task_details'),
]