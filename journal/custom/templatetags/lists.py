from django import template

register = template.Library()

def in_list(value,arg):
   return value in arg

register.filter(in_list)
