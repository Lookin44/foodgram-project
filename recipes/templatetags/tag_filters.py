from django import template

register = template.Library()


@register.filter(name='get_filter_tags')
def get_filter_tags(request, tag):
    new_request = request.GET.copy()
    if not request.GET.getlist('tags'):
        tags_list = ['breakfast', 'lunch', 'dinner']
    else:
        tags_list = new_request.getlist('tags')
    if tag.value in tags_list:
        tags_list.remove(tag.value)
        new_request.setlist('tags', tags_list)
    else:
        new_request.appendlist('tags', tag.value)
    return new_request.urlencode()
