from hmsSite.models import School,Faculty,Project

from django import template

register = template.Library()

@register.simple_tag
def get_schools():
	s = School.objects.all()
	return s

@register.simple_tag
def get_faculties():
	f = Faculty.objects.all()
	return f