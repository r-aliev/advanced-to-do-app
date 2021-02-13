from django.shortcuts import redirect, get_object_or_404
from .models import Task

from django.core.exceptions import PermissionDenied

from tasks.permissions import has_view_task_permission


def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('/')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func


def author_or_reader(view_func):
    def wrapper_func(request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        user = request.user

        if user == task.author or has_view_task_permission(user, task):
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied()

    return wrapper_func


def author(view_func):
    def wrapper_func(request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        if request.user == task.author:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied()
    return wrapper_func

