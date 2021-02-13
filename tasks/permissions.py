from .models import *
from django.contrib.auth.models import User

def assign_task_permission(user, task, comment):
    if user == task.author:
        return
    

    #check if permission already exists
    try:
        existing_permission = TaskPermission.objects.get(task=task, reader=user)
    except TaskPermission.DoesNotExist:
        TaskPermission.objects.create(
            task = task, 
            reader = user,
            comment = comment
        )
    else:
        if comment is True: #in the case if want to update and add comment permission
            if existing_permission.comment is False: #if doesn't have comment permission yet
                existing_permission.comment = comment
                existing_permission.save()
        elif comment is False:
            if existing_permission.comment is True:
                existing_permission.comment = comment
                existing_permission.save()


def has_view_task_permission(user, task):
    if user == task.author:
        return True
    try:
        task_permission = TaskPermission.objects.get(reader=user, task=task)
    except TaskPermission.DoesNotExist:
        return False
    else: #if nothing went wrong
        return True

def has_comment_task_permission(user, task):
    if user == task.author:
        return True

    try:
        task_permission = TaskPermission.objects.get(reader=user, task=task)
    except TaskPermission.DoesNotExist:
        return False

    return task_permission.comment

# for edit comment button
def has_edit_comment_permission(user, comment):
    return comment.author == user

# for delete comment button
def has_delete_comment_permission(user, comment, task):
    return comment.author == user or task.author == user

def get_permitted_tasks(user):
    return user.permitted_tasks.all()