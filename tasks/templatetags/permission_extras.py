from django import template
from tasks.permissions import *

register = template.Library()

@register.filter
def can_comment(user, task):
    return has_comment_task_permission(user, task)


@register.filter
def can_edit_comment(user, comment):
    return has_edit_comment_permission(user, comment)


@register.simple_tag
def can_delete_comment(user, comment, task):
    return has_delete_comment_permission(user, comment, task)