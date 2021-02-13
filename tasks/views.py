from django.shortcuts import render, redirect
from .models import *
from .forms import *
import pytz

from django.utils.safestring import mark_safe
import json
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required


from .permissions import *

from .decorators import *

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)

            return redirect('tasks:login')

    context = {'form':form}
    return render(request, 'tasks/register.html', context)


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username OR password is incorrect')


    context = {}
    return render(request, 'tasks/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('tasks:login')

#from .tasks import send_email_task
# Create your views here.
@login_required(login_url='tasks:login')
def index(request):
    user = request.user
    user_tasks = Task.objects.filter(author=user)
    permitted_tasks = get_permitted_tasks(user)
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = user
            task.save()
            return redirect('/')

    context = {'form':form,'user_tasks':user_tasks,'permitted_tasks':permitted_tasks}
    return render(request, 'tasks/index.html', context)


@login_required(login_url='tasks:login')
@author_or_reader
def detail(request, pk):
    task = Task.objects.get(id=pk)

    comments = task.comments.all()
    context = {'task':task,'comments':comments}
    return render(request, 'tasks/detail.html', context)


@login_required(login_url='tasks:login')
@author
def update(request, pk):
    task = Task.objects.get(id=pk)

    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        
        if form.is_valid():
            form.save()
            return redirect('/')
           

    context ={'form': form}

    return render(request, 'tasks/update.html', context)


@login_required(login_url='tasks:login')
@author
def delete(request, pk):
    task = Task.objects.get(id=pk)

    if request.method == 'POST':
	    task.delete()
	
    return redirect('/')


@login_required(login_url='tasks:login')
@author
def share(request, pk):
    form = ShareForm()
    task = Task.objects.get(id=pk)
   
    if request.method == 'POST':
        form = ShareForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data.get('comment')
            user = form.user_to_share
            assign_task_permission(user, task, comment)

            return redirect('/')

    context ={'form':form}

    return render(request, 'tasks/share.html', context)