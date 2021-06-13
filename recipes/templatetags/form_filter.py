from django import template
from django.utils.html import strip_tags

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter()
def remove_li(value):
    new_value = value.replace('<li>', '').replace('</li>', '\n')
    return strip_tags(new_value)
