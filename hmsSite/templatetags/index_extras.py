from hmsSite.models import Project
from django import template

register = template.Library()

@register.simple_tag
def get_all_projects_initial():

    def approved_filter(object):
        return object.approved

    filterd_objects = filter(approved_filter,Project.objects.all())
    p = list(filterd_objects)
    return p