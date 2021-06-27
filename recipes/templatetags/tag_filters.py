from django import template

register = template.Library()


@register.filter
def get_filter_tags(request, tag):
    new_request = request.GET.copy()

    tags_list = request.GET.getlist('tags')

    if tag in tags_list:
        tags_list.remove(tag)
        new_request.setlist('tags', tags_list)
    else:
        new_request.appendlist('tags', tag)
    return new_request.urlencode()
