from django import template

register = template.Library()

@register.filter
def is_selected(value, arg):
    """
    Compare if the value equals the argument after converting to string
    """
    return str(value) == str(arg) 