from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.generic.base import TemplateView
from django.core import serializers
from django.utils import timezone
from .models import *
from .forms import *

from datetime import datetime
import json
import urllib


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def task_details(request, task_id):
    if is_ajax(request):
        if task_id is not None:
            task = Task.objects.filter(pk=task_id)[0]
            return JsonResponse({"success": True, "data": {
                'id': task_id,
                'task_name': task.task_name,
                'note': task.note,
                'start_date': task.start_date,
                'end_date': task.end_date,
                'create_at': task.create_at.date(),
                'is_completed': task.is_completed,
                'update_at': task.update_at.date() if task.update_at is not None else None
            }}, status=200)
        else:
            return JsonResponse(
                {"success": False, "message": "Can't find id"}, status=400)
    else:
        return JsonResponse(
            {"success": False, "message": "Not an ajax request"}, status=400)


class TaskView(View):
    template_name = 'todolist/index.html'
    form_class = TaskForm

    def get(self, request):
        tasks = Task.objects.all().order_by("completed_on", "-create_at").values('id',
                                                                                 'task_name', 'start_date', 'end_date', 'completed_on', 'is_completed')
        tasks_ls = []
        current_date = datetime.now().date()
        for task in tasks:
            if task['completed_on'] is not None:
                date = (current_date - task['completed_on'].date()).days
                time_status = 'Completed on: ' + \
                    str(task['completed_on'].date())
                time_remaining = str('a' if date == 0 else date) + " days ago"
            elif current_date < task['start_date']:
                date = (task['start_date'] - current_date).days
                time_status = 'Start on: ' + str(task['start_date'])
                time_remaining = str('a' if date == 0 else date) + " days"
            elif current_date >= task['start_date'] and current_date <= task['end_date']:
                date = (task['end_date'] - current_date).days
                time_status = 'End on: ' + str(task['end_date'])
                time_remaining = str('a' if date == 0 else date) + " days left"
            else:
                date = (current_date - task['end_date']).days
                time_status = 'Expired'
                time_remaining = str('a' if date == 0 else date) + " days ago"

            tasks_ls.append({
                'id': task['id'],
                'task_name': task['task_name'],
                'time_status': time_status,
                'time_remaining': time_remaining,
                'is_completed': task['completed_on']
            })

        if not is_ajax(request):
            return render(
                request, self.template_name, context={
                    'tasks': tasks_ls})
        else:
            return JsonResponse({'data': tasks_ls}, safe=False, status=200)

    def post(self, request):
        form = self.form_class(request.POST)
        print(form)
        if is_ajax(request):
            if form.is_valid():
                try:
                    form.save()
                except ValidationError as var1:
                    return JsonResponse(
                        {"success": False, "message": var1.message}, status=400)
                return JsonResponse({"success": True}, status=200)
            return JsonResponse(
                {"success": False, "message": "Not a valid form"}, status=400)
        else:
            return JsonResponse(
                {"success": False, "message": "Not an ajax request"}, status=400)

    def put(self, request, *args, **kwargs):
        if is_ajax(request):
            print(request.body)
            data = {
                var2[0]: var2[1] for var2 in (
                    var1.split('=') for var1 in request.body.decode('utf-8').split('&'))}

            if data.get("task_id"):
                try:
                    task = Task.objects.get(pk=data.get("task_id"))
                    task.task_name = urllib.parse.unquote_plus( # type: ignore
                        data.get("task_name"))
                    task.note = urllib.parse.unquote_plus( # type: ignore
                        data.get("note"))
                    task.start_date = data.get("start_date")  # type: ignore
                    task.end_date = data.get("end_date")  # type: ignore
                    task.save()
                except BaseException:
                    return JsonResponse(
                        {"success": True, "message": "Your items null or has more than one"}, status=500)
            else:
                return JsonResponse(
                    {"success": False, "message": "Can't find id"}, status=400)
            return JsonResponse({"success": True}, status=200)
        else:
            return JsonResponse(
                {"success": False, "message": "Not an ajax request"}, status=400)

    def patch(self, request):
        if is_ajax(request):
            data = json.loads(request.body.decode('utf-8'))
            current_date = timezone.now()

            # Update task status
            if data.get("task_status") is not None:
                try:
                    task = Task.objects.get(pk=data.get("task_id"))
                    task.is_completed = data.get("task_status")
                    task.completed_on = current_date if data.get(
                        "task_status") else None
                    task.save()
                except BaseException:
                    return JsonResponse(
                        {"success": True, "message": "Your items null or has more than one"}, status=500)

                return JsonResponse(
                    {"success": True, "completed_on": current_date}, status=200)
        else:
            return JsonResponse(
                {"success": False, "message": "Not an ajax request"}, status=400)

    def delete(self, request):
        if is_ajax(request):
            data = json.loads(request.body.decode('utf-8'))
            if data.get("task_id") is not None:
                try:
                    Task.objects.get(pk=data.get("task_id")).delete()
                except BaseException:
                    return JsonResponse(
                        {"success": True, "message": "Your items null or has more than one"}, status=500)

                return JsonResponse({"success": True}, status=200)
            else:
                return JsonResponse(
                    {"success": False, "message": "Can't find id"}, status=400)
        else:
            return JsonResponse(
                {"success": False, "message": "Not an ajax request"}, status=400)
