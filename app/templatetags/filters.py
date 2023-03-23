from django import template

register = template.Library()

@register.filter(name='minus')
def minus(value, arg):
    a = value - arg
    return a  

@register.filter(name='multiply')
def multiply(value, arg):
    a = value * arg
    return a