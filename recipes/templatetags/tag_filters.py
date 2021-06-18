from django import template

from recipes.utils import get_all_tags

register = template.Library()


@register.filter
def get_filter_tags(request, tag):
    new_request = request.GET.copy()

    if not request.GET.getlist('tags'):
        tags_list = get_all_tags()
    else:
        tags_list = new_request.getlist('tags')
    if tag.value in tags_list:
        tags_list.remove(tag.value)
        new_request.setlist('tags', tags_list)
    else:
        new_request.appendlist('tags', tag.value)
    return new_request.urlencode()
