from django import template


register = template.Library()

@register.filter(name='subtractss')
def subtractss(value, arg):
    return value - arg